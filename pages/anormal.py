import streamlit as st

from utils.observation import Observation
from utils.configuration import (
    Configuration,
    bool_to_numeric,
    get_distribution,
    show_linear_basis,
    show_linear_basis_observation,
)
from utils.plot import plot_multiple_observations
from utils.load import get_image


def run(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Function to run the menu page "Anormal" that consists of a sidebar and the main page."""
    # display sidebar
    anormal_sb(Config, parameter, info_text)
    # display page
    anormal(Config, parameter, info_text)


def anormal_sb(Config: Configuration, parameter: dict, info_text: dict) -> None:
    # display static sidebar subheader
    st.sidebar.subheader("Settings for the Anormal Observations (nOK)")
    # SIDEBAR 1st EXPANDER
    with st.sidebar.expander("Anomaly Type 1: Leap in the Tightening Phase"):
        anormal_sb_type_1(Config, parameter, info_text)
    # SIDEBAR 2nd EXPANDER
    with st.sidebar.expander("Anomaly Type 2: Leap during the Final Tightening"):
        anormal_sb_type_2(Config, parameter, info_text)
    # SIDEBAR 3rd EXPANDER
    with st.sidebar.expander("Anomaly Type 3: Hard Screw Run with Steeper Slope"):
        anormal_sb_type_3(Config, parameter, info_text)
    # SIDEBAR 4th EXPANDER
    with st.sidebar.expander("Anomaly Type 4: Soft Screw Run with Flatter Slope"):
        anormal_sb_type_4(Config, parameter, info_text)
    # show linear basis
    show_linear_basis(Config)
    show_linear_basis_observation(Config)


def anormal_sb_type_1(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises a sidebar expander to adjust all parameter of type 1 anomalies.

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
        None
    """
    # checkbox to ask for the generation of the Type 1 anomalies
    Config.anomaly_type_1_generate = bool_to_numeric(
        st.checkbox(
            label="Generate Type 1 Anomalies in the Final Dataset",
            value=parameter["anomalies_type_1"]["generate"],
        )
    )

    # adjust all parameter to specify the Type 1 anomalies
    if Config.anomaly_type_1_generate:
        # input amounts for both generation and visualization
        st.write("**Adjust the Total Number of Type 1 Anomalies to ...**")
        col1, col2 = st.columns(2)
        Config.anomaly_type_1_generate_amount = col1.number_input(
            label="... generate in the dataset",
            min_value=parameter["anomalies_type_1"]["generate_amount_min"],
            max_value=parameter["anomalies_type_1"]["generate_amount_max"],
            value=parameter["anomalies_type_1"]["generate_amount_val"],
            step=parameter["anomalies_type_1"]["generate_amount_stp"],
            help=info_text["anomalies"]["amount"],
        )
        Config.anomaly_type_1_generate_amount_to_plot = col2.number_input(
            label="... visualize as reference",
            min_value=parameter["anomalies_type_1"]["generate_amount_to_plot_min"],
            max_value=parameter["anomalies_type_1"]["generate_amount_to_plot_max"],
            value=parameter["anomalies_type_1"]["generate_amount_to_plot_val"],
            step=parameter["anomalies_type_1"]["generate_amount_to_plot_stp"],
            help=info_text["anomalies"]["amount_to_plot"],
        )

        # image header
        st.markdown("""---""")
        st.subheader("Ajust all Parameter of the Type 1 Anomalies:")
        # display image of the anomaly type
        st.image(
            get_image("anomaly_type_01_parameter.png"),
            caption="Schematic Representation of the Course of a Type 1 Anomaly",
            width=300,
            use_column_width="auto",
        )

        # define the limits between which type 1 anomalies are generated
        st.markdown("""---""")
        st.write("**Adjust the Limits to create Type 1 Anomalies:**")
        col1, col2 = st.columns([1, 1])
        # get min
        Config.anomaly_type_1_lower_xlimitation = col1.number_input(
            label="Lower limitation [min]",
            min_value=-100.0,
            max_value=float(
                list(Config.x_steps.values())[2]
                - Config.anomaly_type_1_upper_xlimitation
            ),
            value=Config.anomaly_type_1_lower_xlimitation,
            step=1.0,
            help="add a description later",
        )
        # get max
        Config.anomaly_type_1_upper_xlimitation = col2.number_input(
            label="Upper limitation [max]",
            min_value=-100.0,
            max_value=float(
                list(Config.x_steps.values())[1]
                + Config.anomaly_type_1_lower_xlimitation
            ),
            value=Config.anomaly_type_1_upper_xlimitation,
            step=1.0,
            help="add a description later",
        )

        # get HIGHT
        st.markdown("""---""")
        st.write("**Adjust the Hight of the Leap and its distribution:**")
        # get value for hight
        Config.anomaly_type_1_hight = st.number_input(
            label="Select a value for generating the leap (hight)",
            min_value=parameter["anomalies_type_1"]["hight_min"],
            max_value=parameter["anomalies_type_1"]["hight_max"],
            value=parameter["anomalies_type_1"]["hight_val"],
            step=parameter["anomalies_type_1"]["hight_stp"],
        )
        # get distribution for hight
        (
            Config.anomaly_type_1_hight_selected_type,
            Config.anomaly_type_1_hight_normal_stadev,
            Config.anomaly_type_1_hight_uniform_range,
            Config.anomaly_type_1_hight_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["anomalies_type_1_hight"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=5,
        )

        # get WIDTH
        st.markdown("""---""")
        st.write("**Adjust the Width of the Leap and its distribution:**")
        # get value for width
        Config.anomaly_type_1_width = st.number_input(
            label="Select a value for generating the leap (width)",
            min_value=parameter["anomalies_type_1"]["width_min"],
            max_value=parameter["anomalies_type_1"]["width_max"],
            value=parameter["anomalies_type_1"]["width_val"],
            step=parameter["anomalies_type_1"]["width_stp"],
        )
        # get distribution for width
        (
            Config.anomaly_type_1_width_selected_type,
            Config.anomaly_type_1_width_normal_stadev,
            Config.anomaly_type_1_width_uniform_range,
            Config.anomaly_type_1_width_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["anomalies_type_1_width"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=6,
        )

        # select an offset type to apply [left skewed, right skewed, centered, random]
        st.markdown("""---""")
        st.write("**Adjust the Shape of the Leap:**")
        Config.anomaly_type_1_leap_shape = st.selectbox(
            label="Select the shape of the generated leap",
            options=Config.anomaly_type_1_leap_shapes,
            index=Config.anomaly_type_1_leap_shapes.index(
                Config.anomaly_type_1_leap_shape
            ),
        )


def anormal_sb_type_2(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises a sidebar expander to adjust all parameter of type 2 anomalies.

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
        None
    """
    # select box for generation of the anomaly type
    Config.anomaly_type_2_generate = bool_to_numeric(
        st.checkbox(
            label="Generate Type 2 Anomalies in the Final Dataset",
            value=parameter["anomalies_type_2"]["generate"],
        )
    )

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_2_generate:

        # image header
        st.markdown("""---""")
        st.subheader("Ajust all Parameter of the Type 2 Anomalies:")
        # display image of the anomaly type
        st.image(
            get_image("anomaly_type_02.png"),
            caption="Schematic Representation of the Course of a Type 2 Anomaly",
            width=300,
            use_column_width="auto",
        )

        # input amounts for both generation and visualization
        st.write("**Adjust the Total Number of Type 2 Anomalies to ...**")
        col1, col2 = st.columns(2)

        # input amounts for both generation and visualization
        Config.anomaly_type_2_generate_amount = col1.number_input(
            label="... generate in the data set",
            min_value=parameter["anomalies_type_2"]["generate_amount_min"],
            max_value=parameter["anomalies_type_2"]["generate_amount_max"],
            value=parameter["anomalies_type_2"]["generate_amount_val"],
            step=parameter["anomalies_type_2"]["generate_amount_stp"],
            help=info_text["anomalies"]["amount"],
            key=7,
        )
        Config.anomaly_type_2_generate_amount_to_plot = col2.number_input(
            label="... visualize as reference",
            min_value=parameter["anomalies_type_2"]["generate_amount_to_plot_min"],
            max_value=parameter["anomalies_type_2"]["generate_amount_to_plot_max"],
            value=parameter["anomalies_type_2"]["generate_amount_to_plot_val"],
            step=parameter["anomalies_type_2"]["generate_amount_to_plot_stp"],
            help=info_text["anomalies"]["amount_to_plot"],
        )

        # get HIGHT
        st.markdown("""---""")
        st.write("**Adjust the Hight of the Leap and its distribution:**")
        # get value for hight
        Config.anomaly_type_2_hight = st.number_input(
            label="Select a value for generating the leap (hight)",
            min_value=parameter["anomalies_type_2"]["hight_min"],
            max_value=parameter["anomalies_type_2"]["hight_max"],
            value=parameter["anomalies_type_2"]["hight_val"],
            step=parameter["anomalies_type_2"]["hight_stp"],
            key=8,
        )
        # get distribution for hight
        (
            Config.anomaly_type_2_hight_selected_type,
            Config.anomaly_type_2_hight_normal_stadev,
            Config.anomaly_type_2_hight_uniform_range,
            Config.anomaly_type_2_hight_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["anomalies_type_2_hight"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=9,
        )

        # get WIDTH
        st.markdown("""---""")
        st.write("**Adjust the Width of the Leap and its distribution:**")
        # get value for width
        Config.anomaly_type_2_width = st.number_input(
            label="Select a value for generating the leap (width)",
            min_value=parameter["anomalies_type_2"]["width_min"],
            max_value=parameter["anomalies_type_2"]["width_max"],
            value=parameter["anomalies_type_2"]["width_val"],
            step=parameter["anomalies_type_2"]["width_stp"],
            key=10,
        )
        # get distribution for width
        (
            Config.anomaly_type_2_width_selected_type,
            Config.anomaly_type_2_width_normal_stadev,
            Config.anomaly_type_2_width_uniform_range,
            Config.anomaly_type_2_width_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["anomalies_type_2_width"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=11,
        )


def anormal_sb_type_3(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises a sidebar expander to adjust all parameter of type 3 anomalies.

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
        None
    """
    # select box for generation of the anomaly type
    Config.anomaly_type_3_generate = bool_to_numeric(
        st.checkbox(
            label="Generate Type 3 Anomalies in the Final Dataset",
            value=parameter["anomalies_type_3"]["generate"],
        )
    )

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_3_generate:
        # image header
        st.markdown("""---""")
        st.subheader("Ajust all Parameter of the Type 3 Anomalies:")
        # display image of the anomaly type
        st.image(
            get_image("anomaly_type_03.png"),
            caption="Schematic Representation of the Course of a Type 3 Anomaly",
            width=300,
            use_column_width="auto",
        )

        # input amounts for both generation and visualization
        st.markdown("""---""")
        st.write("**Adjust the Total Number of Type 3 Anomalies to ...**")
        col1, col2 = st.columns(2)
        Config.anomaly_type_3_generate_amount = col1.number_input(
            label="... generate in the dataset",
            min_value=parameter["anomalies_type_3"]["generate_amount_min"],
            max_value=parameter["anomalies_type_3"]["generate_amount_max"],
            value=parameter["anomalies_type_3"]["generate_amount_val"],
            step=parameter["anomalies_type_3"]["generate_amount_stp"],
            help=info_text["anomalies"]["amount"],
            key=12,
        )
        Config.anomaly_type_3_generate_amount_to_plot = col2.number_input(
            label="... visualize as reference",
            min_value=parameter["anomalies_type_3"]["generate_amount_to_plot_min"],
            max_value=parameter["anomalies_type_3"]["generate_amount_to_plot_max"],
            value=parameter["anomalies_type_3"]["generate_amount_to_plot_val"],
            step=parameter["anomalies_type_3"]["generate_amount_to_plot_stp"],
            help=info_text["anomalies"]["amount_to_plot"],
            key=13,
        )

        # input amounts for both generation and visualization
        st.markdown("""---""")
        st.write("**Adjust the two Points to specify the Type 3 Anomalies**")
        col1, col2 = st.columns(2)

        # get input options
        options = [f"P{p}" for p in range(len(Config.x_steps))]
        index_lower_point = options.index(Config.anomaly_type_3_lower_point)
        index_upper_point = options.index(Config.anomaly_type_3_upper_point)

        # get inputs by selectbox
        Config.anomaly_type_3_lower_point = col1.selectbox(
            label="Select lower Point",
            options=options[:-1],
            index=index_lower_point,
            key=14,
            help="add description later",
        )
        Config.anomaly_type_3_upper_point = col2.selectbox(
            label="Select upper Point",
            options=options[int(Config.anomaly_type_3_lower_point[1:]) + 1 :],
            index=0,
            key=15,
            help="add description later",
            disabled=True,
        )

        # get T3 offset
        st.markdown("""---""")
        st.write("**Adjust the Value of the Offset and its distribution:**")
        # get value for offset
        Config.anomaly_type_3_offset = st.number_input(
            label="Select a value for generating the offset (steeper slope)",
            min_value=parameter["anomalies_type_3"]["offset_min"],
            max_value=parameter["anomalies_type_3"]["offset_max"],
            value=parameter["anomalies_type_3"]["offset_val"],
            step=parameter["anomalies_type_3"]["offset_stp"],
            key=16,
        )
        # get distribution for T3 offset
        (
            Config.anomaly_type_3_offset_selected_type,
            Config.anomaly_type_3_offset_normal_stadev,
            Config.anomaly_type_3_offset_uniform_range,
            Config.anomaly_type_3_offset_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["anomalies_type_3_offset"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=17,
        )

        st.markdown("""---""")

        st.checkbox(
            label=f"Apply different distribution to {Config.anomaly_type_3_lower_point} and {Config.anomaly_type_3_upper_point}",
            value=True,
        )
        st.checkbox(
            label=f"Apply offset to neighbors {Config.anomaly_type_3_lower_point} and {Config.anomaly_type_3_upper_point} as well ",
            value=True,
        )


def anormal_sb_type_4(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises a sidebar expander to adjust all parameter of type 4 anomalies.

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
        None
    """
    # select box for generation of the anomaly type
    Config.anomaly_type_4_generate = bool_to_numeric(
        st.checkbox(
            label="Generate Type 4 Anomalies in the Final Dataset",
            value=parameter["anomalies_type_4"]["generate"],
        )
    )

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_4_generate:
        # display image of the anomaly type
        st.image(
            get_image("anomaly_type_04.png"),
            caption="Schematic Representation of the Course of a Type 4 Anomaly",
            width=300,
            use_column_width="auto",
        )

        # input amounts for both generation and visualization
        st.write("**Adjust the Total Number of Type 4 Anomalies to ...**")
        col1, col2 = st.columns(2)
        Config.anomaly_type_4_generate_amount = col1.number_input(
            label="... generate in the dataset",
            min_value=parameter["anomalies_type_4"]["generate_amount_min"],
            max_value=parameter["anomalies_type_4"]["generate_amount_max"],
            value=parameter["anomalies_type_4"]["generate_amount_val"],
            step=parameter["anomalies_type_4"]["generate_amount_stp"],
            help=info_text["anomalies"]["amount"],
            key=18,
        )
        Config.anomaly_type_4_generate_amount_to_plot = col2.number_input(
            label="... visualize as reference",
            min_value=parameter["anomalies_type_4"]["generate_amount_to_plot_min"],
            max_value=parameter["anomalies_type_4"]["generate_amount_to_plot_max"],
            value=parameter["anomalies_type_4"]["generate_amount_to_plot_val"],
            step=parameter["anomalies_type_4"]["generate_amount_to_plot_stp"],
            help=info_text["anomalies"]["amount_to_plot"],
            key=19,
        )

        # input amounts for both generation and visualization
        st.write("**Adjust the two Points to specify the Type 4 Anomalies**")
        col1, col2 = st.columns(2)

        options = [f"P{p}" for p in range(len(Config.x_steps))]
        index_lower_point = options.index(Config.anomaly_type_4_lower_point)
        index_upper_point = options.index(Config.anomaly_type_4_upper_point)

        Config.anomaly_type_4_lower_point = col1.selectbox(
            label="Select lower Point",
            options=options[:-1],
            index=index_lower_point,
            key=20,
            help="add description later",
        )
        Config.anomaly_type_4_upper_point = col2.selectbox(
            label="Select upper Point",
            options=options[int(Config.anomaly_type_4_lower_point[1:]) + 1 :],
            index=0,
            key=21,
            disabled=True,
            help="add description later",
        )

        # get T4 offset
        st.write("**Adjust the Value of the Offset and its distribution:**")
        # get value for offset
        Config.anomaly_type_4_offset = st.number_input(
            label="Select a value for generating the offset (flatter slope)",
            min_value=parameter["anomalies_type_4"]["offset_min"],
            max_value=parameter["anomalies_type_4"]["offset_max"],
            value=parameter["anomalies_type_4"]["offset_val"],
            step=parameter["anomalies_type_4"]["offset_stp"],
            key=22,
        )
        # get distribution for T4 offset
        (
            Config.anomaly_type_4_offset_selected_type,
            Config.anomaly_type_4_offset_normal_stadev,
            Config.anomaly_type_4_offset_uniform_range,
            Config.anomaly_type_4_offset_weibull_alpha,
        ) = get_distribution(
            default_parameter=parameter["anomalies_type_4_offset"],
            info_text=info_text,
            selection=parameter["distributions"]["list_of_types"],
            key=23,
        )


def anormal(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Visualises the current Configuration on the anormal page using the selected anomaly types.

    Parameters
    ---
    Baseline : Observation
        Single observation according to current configuration
    Config : Configuration
        Details of the current configuration
    info_text : dict
        Dictionary with information texts
    """

    # display header as static page element
    st.header("Generation of Anormal Observations (nOK) of up to four Types")

    if Config.anomaly_type_1_generate:
        plot_anomaly_type_1(Config)

    if Config.anomaly_type_2_generate:
        plot_anomaly_type_2(Config)

    if Config.anomaly_type_3_generate:
        plot_anomaly_type_3(Config)

    if Config.anomaly_type_4_generate:
        plot_anomaly_type_4(Config)


def plot_anomaly_type_1(Config: Configuration):
    st.subheader(
        f"Visualization of a Subset of Type 1 Anomalies: _Leap in the Tightening Phase_"
    )
    Obs_type_1 = []
    for _ in range(int(Config.anomaly_type_1_generate_amount_to_plot)):
        Obs_type_1.append(Observation(Config, obs_type="anomaly_type_01"))
    plot_multiple_observations(
        observations=Obs_type_1,
        Config=Config,
        plot_title=f"Exemplary Visualization of Type 1 Anomalies (n={int(Config.anomaly_type_1_generate_amount_to_plot)})",
    )


def plot_anomaly_type_2(Config: Configuration):
    st.subheader(
        "Visualization of a Subset of Type 2 Anomalies: _Leap during the Final Tightening_"
    )
    Obs_type_2 = []
    for _ in range(int(Config.anomaly_type_2_generate_amount_to_plot)):
        Obs_type_2.append(Observation(Config, obs_type="anomaly_type_02"))
    plot_multiple_observations(
        observations=Obs_type_2,
        Config=Config,
        plot_title=f"Exemplary Visualization of Type 2 Anomalies (n={int(Config.anomaly_type_2_generate_amount_to_plot)}",
    )


def plot_anomaly_type_3(Config: Configuration):
    st.subheader(
        "Visualization of a Subset of Type 3 Anomalies: _Hard Screw Run with Steeper Slope_"
    )
    Obs_type_3 = []
    for _ in range(int(Config.anomaly_type_3_generate_amount_to_plot)):
        Obs_type_3.append(Observation(Config, obs_type="anomaly_type_03"))
    plot_multiple_observations(
        observations=Obs_type_3,
        Config=Config,
        plot_title=f"Exemplary Visualization of Type 3 Anomalies (n={int(Config.anomaly_type_3_generate_amount_to_plot)}",
    )


def plot_anomaly_type_4(Config: Configuration):
    # Type 4
    st.subheader(
        "Visualization of a Subset of Type 4 Anomalies: _Softer Screw Run with Flatter Slope_"
    )
    Obs_type_4 = []
    for _ in range(int(Config.anomaly_type_4_generate_amount_to_plot)):
        Obs_type_4.append(Observation(Config, obs_type="anomaly_type_04"))
    plot_multiple_observations(
        observations=Obs_type_4,
        Config=Config,
        plot_title=f"Exemplary Visualization of Type 4 Anomalies (n={int(Config.anomaly_type_4_generate_amount_to_plot)}",
    )
