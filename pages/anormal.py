import streamlit as st

from utils.observation import Observation
from utils.configuration import Configuration, bool_to_numeric, get_distribution, show_linear_basis, show_linear_basis_observation
from utils.plot import plot_multiple_observations
from utils.load import get_image

def run(Config : Configuration, parameter : dict, info_text : dict) -> None:
    '''Function to run the menu page "Anormal" that consists of a sidebar and the main page.'''
    # display sidebar
    anormal_sb(Config, parameter, info_text)
    # display page 
    anormal(Config, parameter, info_text)

def anormal_sb(Config : Configuration, parameter : dict, info_text : dict) -> None:  
    # display static sidebar subheader
    st.sidebar.subheader('Settings for the Anormal Observations (nOK)')
    # SIDEBAR 1st EXPANDER
    with st.sidebar.expander('Anomaly Type 1: Leap in the Tightening Phase'):
        anormal_sb_type_1(Config, parameter, info_text)
    # SIDEBAR 2nd EXPANDER
    with st.sidebar.expander('Anomaly Type 2: Leap during the Final Tightening'):
        anormal_sb_type_2(Config, parameter, info_text)
    # SIDEBAR 3rd EXPANDER
    with st.sidebar.expander('Anomaly Type 3: Hard Screw Run with Steeper Slope'): 
        anormal_sb_type_3(Config, parameter, info_text)
    # SIDEBAR 4th EXPANDER
    with st.sidebar.expander('Anomaly Type 4: Soft Screw Run with Flatter Slope'): 
        anormal_sb_type_4(Config, parameter, info_text)
    # show linear basis
    show_linear_basis(Config)
    show_linear_basis_observation(Config)

def anormal_sb_type_1(
    Config : Configuration, 
    parameter : dict, 
    info_text : dict
    ) -> None:
    '''Visualises a sidebar expander to adjust all parameter of type 1 anomalies. 

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
    '''
    # checkbox for generation of the anomaly type 
    Config.anomaly_type_1_generate = bool_to_numeric(st.checkbox(
        label = 'Generate Type 1 Anomalies in the Final Dataset',
        value = parameter['anomalies_type_1']['generate']))

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_1_generate:

        # input amounts for both generation and visualization
        st.write('**Adjust the Total Number of Type 1 Anomalies to ...**')
        col1, col2 = st.columns(2)
        Config.anomaly_type_1_generate_amount = col1.number_input(
            label='... generate in the dataset',
            min_value = parameter['anomalies_type_1']['generate_amount_min'],
            max_value = parameter['anomalies_type_1']['generate_amount_max'],
            value = parameter['anomalies_type_1']['generate_amount_val'],
            step = parameter['anomalies_type_1']['generate_amount_stp'],
            help = info_text['anomalies']['amount'])
        Config.anomaly_type_1_generate_amount_to_plot = col2.number_input(
            label = '... visualize as reference',
            min_value = parameter['anomalies_type_1']['generate_amount_to_plot_min'],
            max_value = parameter['anomalies_type_1']['generate_amount_to_plot_max'],
            value = parameter['anomalies_type_1']['generate_amount_to_plot_val'],
            step = parameter['anomalies_type_1']['generate_amount_to_plot_stp'], 
            help = info_text['anomalies']['amount_to_plot'])

        # display image of the anomaly type
        st.image(get_image('anomaly_type_01_parameter.png'), 
            caption = 'Schematic Representation of the Course of a Type 1 Anomaly',
            width = 300,
            use_column_width = 'auto')

        # define the limits between which type 1 anomalies are generated
        st.write('**Adjust the Limits to create Type 1 Anomalies:**')
        col1, col2 = st.columns([1, 1])
        # get min
        Config.anomaly_type_1_lower_xlimitation = col1.number_input(
            label='Lower limitation [min]',
            min_value = -100.0,
            max_value = float(list(Config.x_steps.values())[2] - Config.anomaly_type_1_upper_xlimitation),
            value = Config.anomaly_type_1_lower_xlimitation,
            step = 1.0,
            help = 'add a description later')
        # get max
        Config.anomaly_type_1_upper_xlimitation = col2.number_input(
            label='Upper limitation [max]',
            min_value = -100.0,
            max_value = float(list(Config.x_steps.values())[1] + Config.anomaly_type_1_lower_xlimitation),
            value = Config.anomaly_type_1_upper_xlimitation,
            step = 1.0,
            help = 'add a description later')

        # get hight 
        st.write('**Adjust the Hight of the Leap and its distribution:**')
        # get value for hight
        Config.anomaly_type_1_hight = st.number_input(
            label = 'Select a value for generating the leap (hight)',
            min_value = parameter['anomalies_type_1']['hight_min'],
            max_value = parameter['anomalies_type_1']['hight_max'],
            value=parameter['anomalies_type_1']['hight_val'],
            step=parameter['anomalies_type_1']['hight_stp'],)
        # get distribution for hight
        (Config.anomaly_type_1_hight_selected_type,
        Config.anomaly_type_1_hight_normal_stadev, 
        Config.anomaly_type_1_hight_uniform_range, 
        Config.anomaly_type_1_hight_weibull_alpha) = get_distribution(
            default_parameter=parameter['anomalies_type_1_hight'],
            info_text=info_text, 
            selection=parameter['distributions']['list_of_types'],
            key=5)

        # get width 
        st.write('**Adjust the Width of the Leap and its distribution:**')
        # get value for width
        Config.anomaly_type_1_width = st.number_input(
            label = 'Select a value for generating the leap (width)',
            min_value = parameter['anomalies_type_1']['width_min'],
            max_value = parameter['anomalies_type_1']['width_max'],
            value=parameter['anomalies_type_1']['width_val'],
            step=parameter['anomalies_type_1']['width_stp'],)
        # get distribution for width
        (Config.anomaly_type_1_width_selected_type,
        Config.anomaly_type_1_width_normal_stadev, 
        Config.anomaly_type_1_width_uniform_range, 
        Config.anomaly_type_1_width_weibull_alpha) = get_distribution(
            default_parameter=parameter['anomalies_type_1_width'],
            info_text=info_text, 
            selection=parameter['distributions']['list_of_types'],
            key=6)

        # select an offset type to apply [left skewed, right skewed, centered, random]
        st.write('**Adjust the Shape of the Leap:**')
        Config.anomaly_type_1_leap_shape = st.selectbox(
            label = 'Select the shape of the generated leap',
            options = Config.anomaly_type_1_leap_shapes,
            index = Config.anomaly_type_1_leap_shapes.index(Config.anomaly_type_1_leap_shape)
        )


def anormal_sb_type_2(Config : Configuration, parameter : dict, info_text : dict) -> None:
    '''Visualises a sidebar expander to adjust all parameter of type 2 anomalies. 

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
    '''
    # select box for generation of the anomaly type 
    Config.anomaly_type_2_generate = bool_to_numeric(st.checkbox(
        label = 'Generate Type 2 Anomalies in the Final Dataset',
        value = parameter['anomalies_type_2']['generate']))

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_2_generate:
        # display image of the anomaly type
        st.image(get_image('anomaly_type_02.png'), 
            caption = 'Schematic Representation of the Course of a Type 2 Anomaly',
            width = 300,
            use_column_width = 'auto')

        # input amounts for both generation and visualization
        Config.anomaly_type_2_generate_amount = st.number_input(
            label='Adjust the Total Number of Type 2 Anomalies to Generate',
            min_value = parameter['anomalies_type_2']['generate_amount_min'],
            max_value = parameter['anomalies_type_2']['generate_amount_max'],
            value = parameter['anomalies_type_2']['generate_amount_val'],
            step = parameter['anomalies_type_2']['generate_amount_stp'],
            help = info_text['anomalies']['amount'])
        Config.anomaly_type_2_generate_amount_to_plot = st. number_input(
            label = 'Adjust the Number of Type 2 Anomalies to Plot as Example',
            min_value = parameter['anomalies_type_2']['generate_amount_to_plot_min'],
            max_value = parameter['anomalies_type_2']['generate_amount_to_plot_max'],
            value = parameter['anomalies_type_2']['generate_amount_to_plot_val'],
            step = parameter['anomalies_type_2']['generate_amount_to_plot_stp'], 
            help = info_text['anomalies']['amount_to_plot'])


def anormal_sb_type_3(Config : Configuration, parameter : dict, info_text : dict) -> None:
    '''Visualises a sidebar expander to adjust all parameter of type 3 anomalies. 

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
    '''
    # select box for generation of the anomaly type 
    Config.anomaly_type_3_generate = bool_to_numeric(st.checkbox(
        label = 'Generate Type 3 Anomalies in the Final Dataset',
        value = parameter['anomalies_type_3']['generate']))

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_3_generate:
        # display image of the anomaly type
        st.image(get_image('anomaly_type_03.png'), 
            caption = 'Schematic Representation of the Course of a Type 3 Anomaly',
            width = 300,
            use_column_width = 'auto')

        # input amounts for both generation and visualization
        Config.anomaly_type_3_generate_amount = st.number_input(
            label='Adjust the Total Number of Type 3 Anomalies to Generate',
            min_value = parameter['anomalies_type_3']['generate_amount_min'],
            max_value = parameter['anomalies_type_3']['generate_amount_max'],
            value = parameter['anomalies_type_3']['generate_amount_val'],
            step = parameter['anomalies_type_3']['generate_amount_stp'],
            help = info_text['anomalies']['amount'])
        Config.anomaly_type_3_generate_amount_to_plot = st. number_input(
            label = 'Adjust the Number of Type 3 Anomalies to Plot as Example',
            min_value = parameter['anomalies_type_3']['generate_amount_to_plot_min'],
            max_value = parameter['anomalies_type_3']['generate_amount_to_plot_max'],
            value = parameter['anomalies_type_3']['generate_amount_to_plot_val'],
            step = parameter['anomalies_type_3']['generate_amount_to_plot_stp'], 
            help = info_text['anomalies']['amount_to_plot'])


def anormal_sb_type_4(Config : Configuration, parameter : dict, info_text : dict) -> None:
    '''Visualises a sidebar expander to adjust all parameter of type 4 anomalies. 

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
    '''
    # select box for generation of the anomaly type 
    Config.anomaly_type_4_generate = bool_to_numeric(st.checkbox(
        label = 'Generate Type 4 Anomalies in the Final Dataset',
        value = parameter['anomalies_type_4']['generate']))

    # adjust parameter to specify the anomaly type
    if Config.anomaly_type_4_generate:
        # display image of the anomaly type
        st.image(get_image('anomaly_type_04.png'), 
            caption = 'Schematic Representation of the Course of a Type 4 Anomaly',
            width = 300,
            use_column_width = 'auto')

        # input amounts for both generation and visualization
        Config.anomaly_type_4_generate_amount = st.number_input(
            label='Adjust the Total Number of Type 4 Anomalies to Generate',
            min_value = parameter['anomalies_type_4']['generate_amount_min'],
            max_value = parameter['anomalies_type_4']['generate_amount_max'],
            value = parameter['anomalies_type_4']['generate_amount_val'],
            step = parameter['anomalies_type_4']['generate_amount_stp'],
            help = info_text['anomalies']['amount'])
        Config.anomaly_type_4_generate_amount_to_plot = st. number_input(
            label = 'Adjust the Number of Type 4 Anomalies to Plot as Example',
            min_value = parameter['anomalies_type_4']['generate_amount_to_plot_min'],
            max_value = parameter['anomalies_type_4']['generate_amount_to_plot_max'],
            value = parameter['anomalies_type_4']['generate_amount_to_plot_val'],
            step = parameter['anomalies_type_4']['generate_amount_to_plot_stp'], 
            help = info_text['anomalies']['amount_to_plot'])


def anormal(Config : Configuration, parameter : dict, info_text : dict) -> None:
    '''Visualises the current Configuration on the anormal page using the selected anomaly types. 

    Parameters
    ---
    Baseline : Observation
        Single observation according to current configuration
    Config : Configuration
        Details of the current configuration
    info_text : dict
        Dictionary with information texts 
    '''    
    # display static page elements 
    st.header('Generation of Anormal Observations (nOK) of four potential Types')
    
    if Config.anomaly_type_1_generate: 
        anomal_type_1(Config)


def anomal_type_1(Config : Configuration):
    # Type 1
    st.subheader(f'Visualization of a Subset of Type 1 Anomalies: _Leap in the Tightening Phase_')
    Obs_type_1 = []
    for _ in range(int(Config.anomaly_type_1_generate_amount_to_plot)):
        Obs_type_1.append(Observation(Config, obs_type='anomaly_type_01'))
    plot_multiple_observations(
        observations = Obs_type_1, 
        Config = Config,
        plot_title = f'Exemplary Visualization of Type 1 Anomalies (\
            n={int(Config.anomaly_type_1_generate_amount_to_plot)})')

def anomal_type_2(Config, Baseline):

    # Type 2
    st.subheader('Visualization of a Subset of Type 2 Anomalies: _Leap during the Final Tightening_')   
    Obs_type_2 = []
    for _ in range(int(Config.anomaly_type_2_generate_amount_to_plot)):
        Obs_type_2.append(Observation(Config, obs_type='anomaly_type_02'))
    plot_multiple_observations(
        observations = Obs_type_2, 
        Reference = Baseline,
        show_linear_basis = Config.show_linear_basis)

    # Type 3
    st.subheader('Visualization of a Subset of Type 3 Anomalies: _Hard Screw Run with Steeper Slope_')   
    Obs_type_3 = []
    for _ in range(int(Config.anomaly_type_3_generate_amount_to_plot)):
        Obs_type_3.append(Observation(Config, obs_type='anomaly_type_03'))
    plot_multiple_observations(
        observations = Obs_type_3, 
        Reference = Baseline,
        show_linear_basis = Config.show_linear_basis)

    # Type 4
    st.subheader('Visualization of a Subset of Type 4 Anomalies: _Softer Screw Run with Flatter Slope_')   
    Obs_type_4 = []
    for _ in range(int(Config.anomaly_type_4_generate_amount_to_plot)):
        Obs_type_4.append(Observation(Config, obs_type='anomaly_type_04'))
    plot_multiple_observations(
        observations = Obs_type_4, 
        Reference = Baseline,
        show_linear_basis = Config.show_linear_basis)