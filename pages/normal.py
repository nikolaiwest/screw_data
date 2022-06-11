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
from utils.plot import plot_multiple_observations


def run(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Function to run the menu page "Normal" that consists of a sidebar and the main page."""

    # display sidebar
    normal_sb(Config, parameter, info_text)

    # create a group of new OK observations according to the Configuration
    Obs = []
    for _ in range(int(Config.number_of_ok_to_plot)):
        Obs.append(Observation(Config, obs_type="obs"))

    # display 'normal' page
    normal(Obs, Config, info_text)

    # update the config file
    update_config(Config)


def normal_sb(Config: Configuration, parameter: dict, info_text: dict) -> None:

    st.sidebar.subheader("Settings for the Normal Observations (OK)")

    # SIDEBAR 1st EXPANDER
    with st.sidebar.expander("Adjust the total number of OK observations:"):
        normal_sb_amount(Config, parameter, info_text)
    # SIDEBAR 2nd EXPANDER
    with st.sidebar.expander(
        "Adjust the horizontal offset to randomize observations: ⇔"
    ):
        normal_sb_horizontal(Config, parameter, info_text)
    # SIDEBAR 3rd EXPANDER
    with st.sidebar.expander("Adjust the vertial offset to randomize observations: ⇕"):
        normal_sb_vertical(Config, parameter, info_text)

    # show linear basis
    show_linear_basis(Config)
    show_linear_basis_observation(Config)


def normal_sb_amount(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises a sidebar expander to adjust the number of OK observations to create.

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
    Config.number_of_ok = st.number_input(
        label="Number of OK observations to create",
        min_value=parameter["amounts"]["number_of_ok_min"],
        max_value=parameter["amounts"]["number_of_ok_max"],
        value=parameter["amounts"]["number_of_ok_val"],
        step=parameter["amounts"]["number_of_ok_stp"],
    )

    Config.number_of_ok_to_plot = st.number_input(
        label="Number of OK observations to plot",
        min_value=parameter["amounts"]["number_of_ok_to_plot_min"],
        max_value=parameter["amounts"]["number_of_ok_to_plot_max"],
        value=parameter["amounts"]["number_of_ok_to_plot_val"],
        step=parameter["amounts"]["number_of_ok_to_plot_stp"],
    )


def normal_sb_horizontal(
    Config: Configuration, parameter: dict, info_text: dict
) -> None:
    """Visualises a sidebar expander to adjust the horizontal offset of all OK (and nOK) observations to create.

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
    # Checkbox
    Config.offset_hori_apply = bool_to_numeric(
        st.checkbox(
            label="Apply random horizontal offset to selected points",
            value=Config.offset_hori_apply,
        )
    )
    # adjust parameter to specify the offset
    if Config.offset_hori_apply:
        # select points to apply andom vertical offset to
        Config.offset_hori_selected_points = st.multiselect(
            label="Select points to offset horizontally",
            options=[f"P{i}" for i in range(len(list(Config.x_steps.values())))],
            default=Config.offset_hori_selected_points,
        )
        # select distribution to create the offset
        (
            Config.offset_hori_selected_type,
            Config.offset_hori_normal_stadev,
            Config.offset_hori_uniform_range,
            Config.offset_hori_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["randomize_horizontal_offset"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=3,
        )
    Config.offset_hori_equalize = bool_to_numeric(
        st.checkbox(
            label="Apply the same offset to all selected points",
            value=Config.offset_hori_equalize,
        )
    )


def normal_sb_vertical(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises a sidebar expander to adjust the vertial offset of all OK (and nOK) observations to create.

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
    # Checkbox
    Config.offset_vert_apply = bool_to_numeric(
        st.checkbox(label="Apply random vertical offset to selected points", value=1)
    )
    # adjust parameter to specify the offset
    if Config.offset_vert_apply:
        # select points to apply andom vertical offset to
        Config.offset_vert_selected_points = st.multiselect(
            label="Select points to offset vertically",
            options=[f"P{i}" for i in range(len(list(Config.x_steps.values())))],
            default=Config.offset_vert_selected_points,
        )
        # select distribution to create the offset
        (
            Config.offset_vert_selected_type,
            Config.offset_vert_normal_stadev,
            Config.offset_vert_uniform_range,
            Config.offset_vert_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["randomize_vertical_offset"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=4,
        )
    Config.offset_vert_equalize = bool_to_numeric(
        st.checkbox(
            label="Apply the same offset to all selected points",
            value=Config.offset_vert_equalize,
            key=21,
        )
    )


def normal(
    observations: "list[Observation]", Config: Configuration, info_text: dict
) -> None:
    """Visualises the current Configuration on the normal page using the selected count of observations to display.

    Parameters
    ---
    Baseline : Observation
        Single observation according to current configuration
    Config : Configuration
        Details of the current configuration
    info_text : dict
        Dictionary with information texts
    """  # display static page elements
    st.header("Generation of Normal Observations (OK)")
    st.subheader(
        "Visualization of a subset of screw-runs according to the selected Configuration"
    )
    # plot the subset of normal observations
    plot_multiple_observations(observations=observations, Config=Config)
    # add explanation
    with st.expander("Normal Observations: Further Explanation"):
        st.write("add explanation")
