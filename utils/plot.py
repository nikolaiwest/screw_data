import streamlit as st

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet
from utils.configuration import Configuration
from utils.observation import Observation


def plot_single_observation(Obs: Observation, show_linear_basis: bool) -> None:
    """Plotting function to display a single Obervation using Bokeh.

    Parameters
    ---
    Obs : Observation
        Object to desribe a single screw driving run
    show_lienar_basis : bool
        Adds the linear basis of the Observation to the plot

    Returns
    ---
    None
        Creates a bokeh chart on page that displays a single Observation
    """
    # set attributes
    plot_observation = figure(
        title="Generated screwing path: exemplary display of a single screw driving run with the currently selected parameters.",
        x_axis_label="Angle of rotation [°]",
        y_axis_label="Torque [Nm]",
    )
    # define observation data
    data_observation = ColumnDataSource(
        data=dict(
            x_values=list(Obs.x_values),
            y_values=list(Obs.y_values),
            names=[f"P{i}" for i in range(len(Obs.x_steps.values()))],
        )
    )
    # plot data
    plot_observation.line(
        x="x_values",
        y="y_values",
        source=data_observation,
        color="blue",
        legend_label="Observation",
    )
    # show base line
    if show_linear_basis:
        plot_observation = plot_linear_basis(plot_observation, Obs)
    # add legend
    plot_observation.legend.location = "top_left"
    # display chart in page
    st.bokeh_chart(figure=plot_observation, use_container_width=True)


def plot_multiple_observations(
    observations: "list[Observation]",
    Config: Configuration,
    plot_title: str = "Add custom Title",
    use_default_color: bool = True,
) -> None:
    """Plotting function to display a single Obervation using Bokeh.

    Parameters
    ---
    observations : list[Observation]
        Nested list of all observations to plot
    Config : Configuration
        Config file that was used to create the observations
    plot_title :str
        Adds a custon title to the final plot

    Returns
    ---
    None
        Creates a bokeh chart on page that displays multiple Observations
    """
    # set default attributes for the new figure
    plot_observation = figure(
        title=plot_title,
        x_axis_label="Angle of rotation [°]",
        y_axis_label="Torque [Nm]",
    )
    # loop all observations
    for observation in observations:

        # add a linear basis for each anomaly according to type
        if Config.show_linear_basis_observation:
            # type 1
            if observation.apply_type_1_anomaly:
                data_anomaly = ColumnDataSource(
                    data=dict(
                        x_steps=list(observation.x_steps.values()),
                        y_steps=list(observation.y_steps.values()),
                    )
                )
                # dashed line for linear interpolation
                plot_observation.line(
                    x="x_steps",
                    y="y_steps",
                    source=data_anomaly,
                    line_width=0.5,
                    line_alpha=0.5,
                    legend_label="Linear basis of each observation",
                    color="grey",
                )
                plot_observation.circle(
                    x="x_steps",
                    y="y_steps",
                    source=data_anomaly,
                    color="grey",
                    line_width=1,
                )
                plot_observation.legend.location = "top_left"

        # define the observation data of all values
        data_observation = ColumnDataSource(
            data=dict(
                x_values=list(observation.x_values),
                y_values=list(observation.y_values),
            )
        )
        # get color
        plot_color = "blue"
        if not use_default_color:
            if observation.obs_type[:-2] == "anomaly_type_":
                plot_color = "red"
            if observation.obs_type == "ok":
                plot_color = "green"
        # plot observation data
        plot_observation.line(
            x="x_values",
            y="y_values",
            source=data_observation,
            color=plot_color,
            line_width=1.5,
            line_alpha=0.3,
        )

    # add the linear baseline from the config
    if Config.show_linear_basis:
        plot_observation = plot_linear_basis(plot_observation, Config)

    # display chart in page
    st.bokeh_chart(figure=plot_observation, use_container_width=True)


def plot_linear_basis(
    plot_observation: figure, Config: Configuration, line_color: str = "green"
) -> None:
    """Plotting function that adds the linear basis to an existing bokeh figure from a Configuration

    Parameters
    ---
    plot_observation : figure
        Existing bokeh figure to which the base line is added
    Obs : Observation
        Observation object as reference for the baseline
    line_color : str
        Sets the color for the dashed interpolation line (default='green')

    Returns
    ---
    None
        Creates a bokeh chart on page that displays multiple Observations
    """
    data_baseline = ColumnDataSource(
        data=dict(
            x_steps=list(Config.x_steps.values()),
            y_steps=list(Config.y_steps.values()),
            names=[f"P{i}" for i in range(len(Config.x_steps.values()))],
        )
    )
    # white foundation line for linear interpolation
    plot_observation.line(
        x="x_steps",
        y="y_steps",
        source=data_baseline,
        line_width=4,
        line_alpha=0.75,
        color="white",
    )
    # dashed line for linear interpolation
    plot_observation.line(
        x="x_steps",
        y="y_steps",
        source=data_baseline,
        line_dash="dashed",
        line_width=3,
        legend_label="Linear basis of the baseline",
        color=line_color,
    )
    plot_observation.legend.location = "top_left"
    # marker points
    plot_observation.circle(
        x="x_steps", y="y_steps", source=data_baseline, color=line_color, line_width=5
    )
    # lable points
    points = LabelSet(
        x="x_steps",
        y="y_steps",
        text="names",
        x_offset=-20,
        y_offset=20,
        source=data_baseline,
        render_mode="canvas",
    )
    plot_observation.add_layout(points)
    return plot_observation
