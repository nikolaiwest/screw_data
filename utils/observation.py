from random import gauss, uniform, weibullvariate, randint
from numpy import convolve, ones

from typing import Tuple
from utils.configuration import Configuration
from scipy.signal import savgol_filter


def get_slope(p1: int, p2: int) -> float:
    """Simple aux function that returns the slope between two points.

    Parameters
    ----------
    p1 : int
        Coordinates of the first point.
    p2 : int
        Coordinates of the second point.

    Returns
    -------
    float
        Slope between the tow points
    """
    x1, y1 = p1
    x2, y2 = p2
    return (y2 - y1) / (x2 - x1)


class Observation:
    def __init__(self, Config: Configuration, obs_type: str):
        self.obs_type = obs_type
        # x and y steps as dict
        self.x_steps = self.apply_horizontal_offset(Config)
        self.y_steps = self.apply_vertical_offset(Config)
        # x and y step insertion for anomaly_type_01 and anomaly_type_02
        if self.obs_type == "anomaly_type_01":
            self.apply_type_1_anomaly(Config)
        if self.obs_type == "anomaly_type_02":
            self.apply_type_2_anomaly(Config)
        # x and y step distortion for anomaly_type_03 and anomaly_type_04
        if self.obs_type == "anomaly_type_03" or self.obs_type == "anomaly_type_04":
            self.apply_anomaly_incline(Config, obs_type)

        # x and y values as list
        self.y_values = self.get_y(Config)
        self.x_values = self.get_x()

    def get_x(self) -> list:
        """Returns a list that contains the x values of the observation."""
        # creates a list from first x_steps to last x_steps with a stride of one
        first = int(list(self.x_steps.values())[0])
        last = int(list(self.x_steps.values())[-1])
        return [x for x in range(first, last, 1)]

    def get_y(self, Config: Configuration) -> list:
        """Returns a list that containts the y values after trainsformations according to parameter selection."""
        # get a simple linear interpolation based on the steps of y
        y_values = self.apply_linear_interpolation()

        # add a filter to smoothen the interpolation according to selection
        if Config.filter_apply:
            if (
                Config.filter_type_selected == Config.filter_types[0]
            ):  # "Savitzky-Golay-Filter"
                y_values = self.apply_savitzky_golay_filter(y_values, Config)
            if (
                Config.filter_type_selected == Config.filter_types[1]
            ):  # "Discrete Linear Convolution"
                y_values = self.apply_convolve_filter(y_values, Config)

        # apply random scattering to the entire observation
        if Config.rnd_scattering_apply:
            y_values = self.apply_rnd_scattering(y_values, Config)
        # apply additional scattering to the tightening phase
        if Config.rnd_tightening_apply:
            y_values = self.apply_rnd_tighteining(y_values, Config)
        # remove any negative y values and set them to zero
        if Config.remove_neg_y_values:
            y_values = self.remove_neg_y_values(y_values)
        return y_values

    def apply_linear_interpolation(self) -> list:
        """Returns a list that contains the linear interpolation of y values of the observation."""
        y = []
        for idx in range(len(self.y_steps.values()) - 1):
            len_y = self.x_steps[f"x{idx+1}"] - self.x_steps[f"x{idx}"]
            p1 = (self.x_steps[f"x{idx}"], self.y_steps[f"y{idx}"])
            p2 = (self.x_steps[f"x{idx+1}"], self.y_steps[f"y{idx+1}"])
            # check for leap (x1=x2)
            if not p1[0] == p2[0]:
                s = get_slope(p1, p2)
                y_values = [s * x + self.y_steps[f"y{idx}"] for x in range(int(len_y))]
            else:
                y_values = [p2[1] - p1[1] + self.y_steps[f"y{idx}"]]
            y += y_values
        return y

    def apply_savitzky_golay_filter(
        self, y_values: list, Config: Configuration
    ) -> list:
        """Applies a Savitzky-Golay filter to smoothen the y data according to <window_length> and <poly_order>"""
        return list(
            savgol_filter(
                x=y_values,
                window_length=int(Config.filter_sg_window_length),
                polyorder=int(Config.filter_sg_poly_order),
            )
        )

    def apply_convolve_filter(self, y_values: list, Config: Configuration) -> list:
        """Applies discrete linear convolution to smoothen the y data according to <box_pts>"""
        # see: https://numpy.org/doc/stable/reference/generated/numpy.convolve.html
        # append points to prevent sagging in later stages (points are later removed again)
        y_values = y_values + [y_values[-1] for _ in range(Config.filter_conv_box_pts)]
        return convolve(
            y_values,
            (ones(Config.filter_conv_box_pts) / Config.filter_conv_box_pts),
            mode="same",
        )[: -Config.filter_conv_box_pts]

    def apply_rnd_scattering(self, y_values: list, Config: Configuration) -> list:
        # apply random scattering to the entire observation
        if Config.rnd_scattering_selected_type == "Normal":
            return [y + gauss(0, Config.rnd_scattering_normal_stadev) for y in y_values]
        if Config.rnd_scattering_selected_type == "Uniform":
            uniform_range = Config.rnd_scattering_uniform_range / 2
            return [y + uniform(-uniform_range, uniform_range) for y in y_values]
        if Config.rnd_scattering_selected_type == "Weibull":
            return [
                y + weibullvariate(Config.rnd_scattering_weibull_alpha, beta=1.0)
                for y in y_values
            ]

    def apply_rnd_tighteining(self, y_values: list, Config: Configuration) -> list:
        # apply additional scattering to the selected subset of the observation
        upper = Config.rnd_tightening_upper_xlimitation
        lower = Config.rnd_tightening_lower_xlimitation
        if Config.rnd_tightening_selected_type == "Normal":
            return [
                y + gauss(0, Config.rnd_tightening_normal_stadev)
                if (lower < x < upper)
                else y
                for x, y in zip(range(len(y_values)), y_values)
            ]
        if Config.rnd_tightening_selected_type == "Uniform":
            uniform_range = Config.rnd_tightening_uniform_range / 2
            return [
                y + uniform(-uniform_range, uniform_range) if (lower < x < upper) else y
                for x, y in zip(range(len(y_values)), y_values)
            ]
        if Config.rnd_tightening_selected_type == "Weibull":
            return [
                y + weibullvariate(Config.rnd_tightening_weibull_alpha, beta=1.0)
                if (lower < x < upper)
                else y
                for x, y in zip(range(len(y_values)), y_values)
            ]

    def remove_neg_y_values(self, y_values, substitute=0) -> list:
        # remove all negative values and insert zero
        return [y if y > 0 else substitute for y in y_values]

    def apply_horizontal_offset(self, Config: Configuration) -> "dict[str: int]":

        # check if offset needs to be applied
        if not Config.offset_hori_apply or self.obs_type == "baseline":
            return Config.x_steps
        # apply horizontal offset
        else:
            # steps as new dict
            x_steps = {k: Config.x_steps[k] for k in Config.x_steps.keys()}
            # normal
            if Config.offset_hori_selected_type == "Normal":
                # loop over selection
                for point in Config.offset_hori_selected_points:
                    # get gausian offset
                    offset = gauss(0, Config.offset_hori_normal_stadev)
                    # loop over the selected point and all following points to apply the offset
                    for p in range(int(point[-1:]), len(x_steps)):
                        x_steps[f"x{p}"] = int(x_steps[(f"x{p}")] + offset)
            # uniform
            if Config.offset_hori_selected_type == "Uniform":
                # loop over selection
                for point in Config.offset_hori_selected_points:
                    # get uniform offset
                    uniform_range = Config.offset_hori_uniform_range / 2
                    offset = uniform(-uniform_range, uniform_range)
                    # loop over the selected point and all following points to apply the offset
                    for p in range(int(point[-1:]), len(x_steps)):
                        x_steps[f"x{p}"] = int(x_steps[(f"x{p}")] + offset)
            # weibull
            if Config.offset_hori_selected_type == "Weibull":
                # loop over selection
                for point in Config.offset_hori_selected_points:
                    # get weibull offset
                    offset = weibullvariate(Config.offset_hori_weibull_alpha, beta=1.0)
                    # loop over the selected point and all following points to apply the offset
                    for p in range(int(point[-1:]), len(x_steps)):
                        x_steps[f"x{p}"] = int(x_steps[(f"x{p}")] + offset)
            # x_steps now contains the adjusted steps according to the selected offsets
            return x_steps

    def apply_vertical_offset(self, Config: Configuration) -> "dict[str: float]":

        # check if offset needs to be applied
        if not Config.offset_vert_apply or self.obs_type == "baseline":
            return Config.y_steps
        # apply vertical offset
        else:
            import streamlit as st

            # steps as new dict
            y_steps = {k: Config.y_steps[k] for k in Config.y_steps.keys()}
            if Config.offset_vert_selected_type == "Normal":
                for point in Config.offset_vert_selected_points:
                    y_steps[f"y{point[-1:]}"] = float(
                        y_steps[(f"y{point[-1:]}")]
                        + gauss(0, Config.offset_vert_normal_stadev)
                    )
            if Config.offset_vert_selected_type == "Uniform":
                for point in Config.offset_vert_selected_points:
                    uniform_range = Config.offset_vert_uniform_range / 2
                    y_steps[f"y{point[-1:]}"] = float(
                        y_steps[(f"y{point[-1:]}")]
                        + uniform(-uniform_range, uniform_range)
                    )
            if Config.offset_vert_selected_type == "Weibull":
                for point in Config.offset_vert_selected_points:
                    y_steps[f"y{point[-1:]}"] = float(
                        y_steps[(f"y{point[-1:]}")]
                        + weibullvariate(Config.offset_vert_weibull_alpha, beta=1.0)
                    )
            return y_steps

    def apply_type_1_anomaly(self, Config: Configuration) -> None:

        # create three new steps in dict with default value
        temp_len = len(Config.x_steps)
        temp_x_steps = list(self.x_steps.values())
        temp_y_steps = list(self.y_steps.values())
        for p in range(temp_len, temp_len + 3):
            self.x_steps[f"x{p}"] = 1_000
            self.y_steps[f"y{p}"] = 50
        # update the newly created values in reverse order
        for p in range(temp_len - 2, temp_len + 3):
            self.x_steps[f"x{p}"] = temp_x_steps[p - 3]
            self.y_steps[f"y{p}"] = temp_y_steps[p - 3]

        # get width for this observation
        if Config.anomaly_type_1_width_selected_type == "Normal":
            width = int(
                Config.anomaly_type_1_width
                + gauss(0, Config.anomaly_type_1_width_normal_stadev)
            )
        if Config.anomaly_type_1_width_selected_type == "Uniform":
            uniform_range = Config.anomaly_type_1_width_uniform_range / 2
            width = int(
                Config.anomaly_type_1_width + uniform(-uniform_range, uniform_range)
            )
        if Config.anomaly_type_1_width_selected_type == "Weibull":
            width = int(
                Config.anomaly_type_1_width
                + weibullvariate(Config.anomaly_type_1_width_weibull_alpha, beta=1.0)
            )
        # get hight for this observation
        if Config.anomaly_type_1_hight_selected_type == "Normal":
            hight = Config.anomaly_type_1_hight + gauss(
                0, Config.anomaly_type_1_hight_normal_stadev
            )
        if Config.anomaly_type_1_hight_selected_type == "Uniform":
            uniform_range = Config.anomaly_type_1_hight_uniform_range / 2
            hight = Config.anomaly_type_1_hight + uniform(-uniform_range, uniform_range)
        if Config.anomaly_type_1_hight_selected_type == "Weibull":
            hight = Config.anomaly_type_1_hight + weibullvariate(
                Config.anomaly_type_1_hight_weibull_alpha, beta=1.0
            )

        # set x1 and x3 values for new points
        x_steps_min = self.x_steps["x1"] + Config.anomaly_type_1_lower_xlimitation
        x_steps_max = self.x_steps["x2"] - Config.anomaly_type_1_upper_xlimitation
        self.x_steps["x2"] = randint(x_steps_min, x_steps_max - width - 1)
        self.x_steps["x4"] = self.x_steps["x2"] + width
        # set x3 according to selected shape
        if Config.anomaly_type_1_leap_shape == "Centered":
            self.x_steps["x3"] = self.x_steps["x2"] + width / 2
        if Config.anomaly_type_1_leap_shape == "Right-skewed":
            self.x_steps["x3"] = self.x_steps["x2"] + uniform(
                1,
                width / 2 - 1,
            )
        if Config.anomaly_type_1_leap_shape == "Left-skewed":
            self.x_steps["x3"] = self.x_steps["x2"] + uniform(width / 2, width - 1)
        if Config.anomaly_type_1_leap_shape == "Random":
            self.x_steps["x3"] = self.x_steps["x2"] + uniform(1, width - 1)
        # set y values for new points
        self.y_steps["y2"] = self.y_steps["y1"]  # previous y value
        self.y_steps["y3"] = self.y_steps["y3"] + hight
        self.y_steps["y4"] = self.y_steps["y5"]  # following y value

    def apply_type_2_anomaly(self, Config: Configuration) -> None:

        self.x_steps[f"x{Config.init_len}"] = 1_000
        self.y_steps[f"y{Config.init_len}"] = 50

        for p in range(len(self.y_steps) - 1, 4, -1):
            self.y_steps[f"y{p}"] = self.y_steps[f"y{p-1}"]
            self.x_steps[f"x{p}"] = self.x_steps[f"x{p-1}"]

        self.x_steps["x5"] = 320  # randomize
        self.y_steps["y5"] = 25  # randomize

        return self.x_steps, self.y_steps

    def apply_anomaly_incline(self, Config: Configuration, obs_type: str) -> None:
        if obs_type == "anomaly_type_03":
            self.x_steps["x2"] = self.x_steps["x2"] + 20
            self.x_steps["x3"] = self.x_steps["x3"] + 15
            self.x_steps["x4"] = self.x_steps["x4"] - 15
            self.x_steps["x5"] = self.x_steps["x5"] - 20
            self.x_steps["x6"] = self.x_steps["x6"] - 25

            return self.x_steps, self.y_steps
        if obs_type == "anomaly_type_04":

            self.x_steps["x2"] = self.x_steps["x2"] - 15
            self.x_steps["x3"] = self.x_steps["x3"] - 15
            self.x_steps["x4"] = self.x_steps["x4"] + 15
            self.x_steps["x5"] = self.x_steps["x5"] + 15
            self.x_steps["x6"] = self.x_steps["x6"] + 15

            return self.x_steps, self.y_steps
