import streamlit as st

from utils.observation import Observation
from utils.configuration import (
    Configuration,
    get_distribution,
    bool_to_numeric,
    show_linear_basis,
    show_linear_basis_observation,
    update_config,
)
from utils.plot import plot_single_observation


def run(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Function to run the menu page "Baseline" that consists of a sidebar and the main page."""

    # display sidebar
    baseline_sb(Config, parameter, info_text)

    # create new observation according to the selected Configuration
    Baseline = Observation(Config, obs_type="baseline")

    # display 'baseline' page
    baseline(Baseline, Config, info_text)

    # update the config file
    update_config(Config)


def baseline_sb(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Function to display the side bar of the menu page "Baseline".

    Parameters
    ---
    Config : Configuration
        Details of the current configuration
    parameter : dict
        Dictionary with the saved parameter from the parameter.toml file
    info_text : dict
        Dictionary with information texts

    Returns
    ---
    None
    """
    # display subheader for baseline
    st.sidebar.subheader("Preference Selection for Parameter for the Baseline")

    # 1st Sidebar Expander
    with st.sidebar.expander("Adjust the Linear Basis by adding or removing Points"):
        baseline_sb_change_number_of_points(Config)

    # 1st Sidebar Expander
    with st.sidebar.expander(
        "Adjust the values of the Points used as the Linear Basis"
    ):
        baseline_sb_linear_basis(Config, parameter, info_text)

    # 3rd Sidebar Expander
    with st.sidebar.expander("Adjust the Function for Smoothing the Screw Runs"):
        baseline_sb_smoothing_parameter(Config, parameter, info_text)

    # 4th Sidebar Expander
    with st.sidebar.expander(
        "Adjust the Scattering to apply Noise to the entire Screw Run"
    ):
        baseline_sb_scattering_for_entire_run(Config, parameter, info_text)

    # 5th Sidebar Expander
    with st.sidebar.expander(
        "Adjust the additional Scattering during the Tighening Phase"
    ):
        baseline_sb_scattering_for_tighening_phase(Config, parameter, info_text)

    # remove negative values
    remove_neg_y_values(Config)
    # show linear basis
    show_linear_basis(Config)


def baseline_sb_change_number_of_points(Config: Configuration) -> None:
    """Visualises a sidebar expander with all two bottons to add and remove points.

    Parameters
    ---
    Config : Configuration
        Details of the current configuration

    Returns
    ---
    None
    """
    # separate columns für x and y
    col1, col2 = st.columns([1, 1])

    # add a new P(xi, yi)
    if col1.button("Add a new Point"):
        new_idx = len(Config.x_steps)
        Config.x_steps[f"x{new_idx}"] = Config.x_steps.get(f"x{new_idx-1}") + 10
        Config.y_steps[f"y{new_idx}"] = Config.y_steps.get(f"y{new_idx-1}") + 0
    # remove last P(xi, yi)
    if col2.button("Remove the last Point"):
        last_idx = len(Config.x_steps) - 1
        Config.x_steps.pop(f"x{last_idx}")
        Config.y_steps.pop(f"y{last_idx}")


def baseline_sb_linear_basis(
    Config: Configuration, parameter: dict, info_text: dict
) -> None:
    """Visualises a sidebar expander with all information on the linear basis of the Config file.

    Parameters
    ---
    Config : Configuration
        Details of the current configuration
    parameter : dict
        Dictionary with the saved parameter from the parameter.toml file
    info_text : dict
        Dictionary with information texts

    Returns
    ---
    None
    """
    # separate columns für x and y
    col1, col2 = st.columns([1, 1])

    # numeric input for all P(xi, yi)
    for idx in range(len(Config.x_steps)):
        Config.x_steps[f"x{idx}"] = col1.number_input(
            label=f"Rotation at x{idx}",
            min_value=0.0,
            max_value=7200.0,
            value=Config.x_steps[f"x{idx}"],
            help=info_text["basis"]["show_linear_basis_tt"],
            step=None,
        )
        Config.y_steps[f"y{idx}"] = col2.number_input(
            label=f"Torque at y{idx}",
            min_value=0.0,
            max_value=7200.0,
            value=Config.y_steps[f"y{idx}"],
            help=info_text["basis"]["show_linear_basis_tt"],
            step=None,
        )


def baseline_sb_smoothing_parameter(
    Config: Configuration,
    parameter: dict,
    info_text: dict,
) -> None:
    """Visualises a sidebar expander with all information with the parameters for smoothing.

    Parameters
    ---
    Config : Configuration
        Details of the current configuration
    parameter : dict
        Dictionary with parameter configurations
    info_text : dict
        Dictionary with information texts

    Returns
    ---
    None
    """
    # checkbox: apply?
    Config.filter_apply = bool_to_numeric(
        st.checkbox(
            label="Apply a filter to smoothen the interpolation",
            value=Config.filter_apply,
        )
    )

    # show selectbox for filter choice
    if Config.filter_apply:
        Config.filter_type_selected = st.selectbox(
            "Select smoothing method", Config.filter_types, index=0
        )
        # filter parameter according to selction
        if (
            Config.filter_type_selected == Config.filter_types[0]
        ):  #'Savitzky-Golay filter'
            Config.filter_sg_window_length = st.slider(
                label="Adjust the Length of the Smoothing Window",
                min_value=parameter["filter"]["sg_window_length_min"],
                max_value=parameter["filter"]["sg_window_length_max"],
                value=parameter["filter"]["sg_window_length_val"],
                step=parameter["filter"]["sg_window_length_stp"],
                help=info_text["filter"]["sg_window_length_tt"],
            )
            Config.filter_sg_poly_order = st.slider(
                label="Adjust the Polynomial Order",
                min_value=parameter["filter"]["sg_poly_order_min"],
                max_value=parameter["filter"]["sg_poly_order_max"],
                value=parameter["filter"]["sg_poly_order_val"],
                step=parameter["filter"]["sg_poly_order_stp"],
                help=info_text["filter"]["sg_poly_order_tt"],
            )
        if (
            Config.filter_type_selected == Config.filter_types[1]
        ):  #'Discrete linear convolution'
            Config.filter_conv_box_pts = st.slider(
                label="Adjust the box points for interpolation",
                min_value=parameter["filter"]["conv_box_pts_min"],
                max_value=parameter["filter"]["conv_box_pts_max"],
                value=parameter["filter"]["conv_box_pts_val"],
                step=parameter["filter"]["conv_box_pts_stp"],
                help=info_text["filter"]["conv_box_pts_tt"],
            )


def baseline_sb_scattering_for_entire_run(
    Config: Configuration,
    parameter: dict,
    info_text: dict,
) -> None:
    """Visualises a sidebar expander with all information with the parameters for scattering.

    Parameters
    ---
    Config : Configuration
        Details of the current configuration
    parameter : dict
        Dictionary with parameter configurations
    info_text : dict
        Dictionary with information texts
    """
    # checkbox: apply?
    Config.rnd_scattering_apply = bool_to_numeric(
        st.checkbox(
            label="Apply random noise to the entire screw run",
            value=Config.rnd_scattering_apply,
        )
    )
    # apply random scattering to the entire observation
    if Config.rnd_scattering_apply:
        (
            Config.rnd_scattering_selected_type,
            Config.rnd_scattering_normal_stadev,
            Config.rnd_scattering_uniform_range,
            Config.rnd_scattering_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["randomize_scattering"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=1,
        )


def baseline_sb_scattering_for_tighening_phase(
    Config: Configuration,
    parameter: dict,
    info_text: dict,
) -> None:
    """Visualises a sidebar expander with all information with the parameters for scattering.

    Parameters
    ---
    Config : Configuration
        Details of the current configuration
    parameter : dict
        Dictionary with parameter configurations
    info_text : dict
        Dictionary with information texts
    """

    # checkbox: apply?
    Config.rnd_tightening_apply = bool_to_numeric(
        st.checkbox(
            label="Apply additional noise in the tightening phase",
            value=Config.rnd_tightening_apply,
        )
    )
    # apply additional random scattering to the tightening phase
    if Config.rnd_tightening_apply:
        # define range to apply additional scattering
        col1, col2 = st.columns([1, 1])
        Config.rnd_tightening_lower_xlimitation = col1.number_input(
            label="Select lower limitation",
            min_value=float(list(Config.x_steps.values())[0]),
            max_value=Config.rnd_tightening_upper_xlimitation,
            value=Config.rnd_tightening_lower_xlimitation,
            step=1.0,
            help="add a description later",
        )
        Config.rnd_tightening_upper_xlimitation = col2.number_input(
            label="Select upper limitation",
            min_value=Config.rnd_tightening_lower_xlimitation,
            max_value=float(list(Config.x_steps.values())[-1]),
            value=Config.rnd_tightening_upper_xlimitation,
            step=1.0,
            help="add a description later",
        )
        # specify the distribution
        (
            Config.rnd_tightening_selected_type,
            Config.rnd_tightening_normal_stadev,
            Config.rnd_tightening_uniform_range,
            Config.rnd_tightening_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["randomize_tightening"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=2,
        )


def remove_neg_y_values(Config: Configuration) -> None:
    """Simple checkbox to determine if negative y values are to be removed"""
    Config.remove_neg_y_values = bool_to_numeric(
        st.sidebar.checkbox(
            label="Set negative y-values to zero", value=Config.remove_neg_y_values
        )
    )


def baseline(Baseline: Observation, Config: Configuration, info_text: dict) -> None:
    """Visualises the current Configuration on the main page using a single observation as baseline.

    Parameters
    ---
    Baseline : Observation
        Single observation according to current configuration
    Config : Configuration
        Details of the current configuration
    info_text : dict
        Dictionary with information texts
    """
    # display static page elements
    st.header(
        "Generation of a Baseline that Determines the General Shape of all Observations"
    )
    st.subheader("Visualization of the currect shape of the base line")
    # plot the current screw run according to the selected parameters
    plot_single_observation(Baseline, Config.show_linear_basis)
    # check for negative y values
    if any(y < 0 for y in Baseline.y_values):
        st.warning(info_text["information"]["baseline_neg_warning"])
    # add explanation
    with st.expander("Baseline: Further Explanation"):
        st.write(
            "The baseline represents the starting point for generating new observations of screw runs. Both the **normal** observations and the **anormal** \
            observations rely on this baseline. The characteristics of Normal and Abnormal observations can then be adjusted in the following two pages."
        )
        st.write("**Adjust the Linear Basis used in all Observations**")
        st.write(
            "- In order to realize a high adaptability of the screw runs, all observations are based on a few points that are linearly interpolated. \
            The individual points can first be adjusted as the foundation of the interpolation."
        )
        st.write("")

        st.write("**Adjust the Function for Smoothing the Screw Runs**")
        st.write(
            "- In order to realize a natural screw curve, a filter can then be applied to smooth the curve."
        )
        st.write("")

        st.write("**Adjust the Random Scattering to apply Noise**")
        st.write("Finally, two types of scattering can be inserted.")
        st.write(
            "- On the one hand, a general noise can be applied to the entire observation."
        )
        st.write(
            "- On the other hand, additional scattering can be generated in the tightening phase."
        )
        st.write("")
