from typing import Tuple
from toml import dump, load
from pathlib import Path
from utils.load import get_root
from streamlit import selectbox, slider, sidebar, checkbox

class Configuration():

    def __init__(self, parameter):
        # Check if lengths match
        if len(parameter['base']['init_x']) != len(parameter['base']['init_y']):
            raise ValueError('X and Y have different number of steps')
        else: 
            self.init_len = len(parameter['base']['init_x'])

        # set point values for linear basis of X and Y as dict 
        self.x_steps = {f'x{i}' : x for x, i in zip(parameter['base']['init_x'], range(self.init_len))}
        self.y_steps = {f'y{i}' : y for y, i in zip(parameter['base']['init_y'], range(self.init_len))}

        # set default values for all amounts 
        self.number_of_ok = parameter['amounts']['number_of_ok']
        self.number_of_ok_to_plot = parameter['amounts']['number_of_ok_to_plot']

        # set default values for smoothing filter 
        self.types = parameter['filter']['list_of_types']
        self.selected_type = parameter['filter']['selected_type']
        self.filter_sg_window_length = parameter['filter']['filter_sg_window_length_val']
        self.filter_sg_poly_order = parameter['filter']['filter_sg_poly_order_val']

        # set default values for random scattering
        self.rnd_scattering_apply = parameter['randomize_scattering']['apply']
        self.rnd_scattering_selected_type = parameter['randomize_scattering']['selected_type']
        self.rnd_scattering_normal_stadev = parameter['randomize_scattering']['normal_stadev_val']
        self.rnd_scattering_uniform_range = parameter['randomize_scattering']['uniform_range_val']
        self.rnd_scattering_weibull_alpha = parameter['randomize_scattering']['weibull_alpha_val']

        # set default values for randomizing the tightening phase
        self.rnd_tightening_apply = parameter['randomize_tightening']['apply']
        self.rnd_tightening_selected_type = parameter['randomize_tightening']['selected_type']
        self.rnd_tightening_normal_stadev = parameter['randomize_tightening']['normal_stadev_val']
        self.rnd_tightening_uniform_range = parameter['randomize_tightening']['uniform_range_val']
        self.rnd_tightening_weibull_alpha = parameter['randomize_tightening']['weibull_alpha_val']
        self.rnd_tightening_lower_xlimitation = parameter['randomize_tightening']['lower_xlimitation']
        self.rnd_tightening_upper_xlimitation = parameter['randomize_tightening']['upper_xlimitation']

        # set default values for the vertical offset
        self.offset_hori_apply = parameter['randomize_horizontal_offset']['apply']
        self.offset_hori_selected_points = parameter['randomize_horizontal_offset']['selected_points']
        self.offset_hori_selected_type = parameter['randomize_horizontal_offset']['selected_type']
        self.offset_hori_normal_stadev = parameter['randomize_horizontal_offset']['normal_stadev_val']
        self.offset_hori_uniform_range = parameter['randomize_horizontal_offset']['uniform_range_val']
        self.offset_hori_weibull_alpha = parameter['randomize_horizontal_offset']['weibull_alpha_val']

        # set default values for the horizontal offset
        self.offset_vert_apply = parameter['randomize_vertical_offset']['apply']
        self.offset_vert_selected_points = parameter['randomize_vertical_offset']['selected_points']
        self.offset_vert_selected_type = parameter['randomize_vertical_offset']['selected_type']
        self.offset_vert_normal_stadev = parameter['randomize_vertical_offset']['normal_stadev_val']
        self.offset_vert_uniform_range = parameter['randomize_vertical_offset']['uniform_range_val']
        self.offset_vert_weibull_alpha = parameter['randomize_vertical_offset']['weibull_alpha_val']
        
        # set default values for anomaly (type 1)
        self.anomaly_type_1_generate = parameter['anomalies_type_1']['generate']
        self.anomaly_type_1_generate_amount = parameter['anomalies_type_1']['generate_amount_val']
        self.anomaly_type_1_generate_amount_to_plot = parameter['anomalies_type_1']['generate_amount_to_plot_val']
        self.anomaly_type_1_lower_xlimitation = parameter['anomalies_type_1']['lower_xlimitation']
        self.anomaly_type_1_upper_xlimitation = parameter['anomalies_type_1']['upper_xlimitation']
        self.anomaly_type_1_width = parameter['anomalies_type_1']['width_val']
        self.anomaly_type_1_width_selected_type = parameter['anomalies_type_1_width']['selected_type']
        self.anomaly_type_1_width_normal_stadev = parameter['anomalies_type_1_width']['normal_stadev_val']
        self.anomaly_type_1_width_uniform_range = parameter['anomalies_type_1_width']['uniform_range_val']
        self.anomaly_type_1_width_weibull_alpha = parameter['anomalies_type_1_width']['weibull_alpha_val']
        self.anomaly_type_1_hight = parameter['anomalies_type_1']['hight_val']
        self.anomaly_type_1_hight_selected_type = parameter['anomalies_type_1_hight']['selected_type']
        self.anomaly_type_1_hight_normal_stadev = parameter['anomalies_type_1_hight']['normal_stadev_val']
        self.anomaly_type_1_hight_uniform_range = parameter['anomalies_type_1_hight']['uniform_range_val']
        self.anomaly_type_1_hight_weibull_alpha = parameter['anomalies_type_1_hight']['weibull_alpha_val']
        self.anomaly_type_1_leap_shape = parameter['anomalies_type_1']['leap_shape']
        self.anomaly_type_1_leap_shapes = parameter['anomalies_type_1']['leap_shapes']


        # set default values for anomaly (type 2)
        self.anomaly_type_2_generate = parameter['anomalies_type_2']['generate']
        self.anomaly_type_2_generate_amount = parameter['anomalies_type_2']['generate_amount_val']
        self.anomaly_type_2_generate_amount_to_plot = parameter['anomalies_type_2']['generate_amount_to_plot_val']

        # set default values for anomaly (type 3)
        self.anomaly_type_3_generate = parameter['anomalies_type_3']['generate']
        self.anomaly_type_3_generate_amount = parameter['anomalies_type_3']['generate_amount_val']
        self.anomaly_type_3_generate_amount_to_plot = parameter['anomalies_type_3']['generate_amount_to_plot_val']

        # set default values for anomaly (type 4)
        self.anomaly_type_4_generate = parameter['anomalies_type_4']['generate']
        self.anomaly_type_4_generate_amount = parameter['anomalies_type_4']['generate_amount_val']
        self.anomaly_type_4_generate_amount_to_plot = parameter['anomalies_type_4']['generate_amount_to_plot_val']


        # set default values for additional preparations
        self.remove_neg_y_values = parameter['preparation']['remove_neg_y_values']
        # set default values for visualizations
        self.show_linear_basis = parameter['visualization']['show_linear_basis']
        self.show_linear_basis_observation = parameter['visualization']['show_linear_basis_observation']


    def export_config(self):
        pass

#def update_config()

def get_distribution(
    default_parameter : dict, 
    info_text : dict,
    selection : list,
    key : int
    ) -> Tuple[float, float, float]:
    '''Creates a sidebar element to select and configure a distribution. 

    Parameters
    ---
    default_parameter : dict
        Dictionary with parameter configurations
    info_text : dict
        Dictionary with information texts 
    selection : list
        List of distribution types to choose from
    key : int
        Unique key for the input widgets

    Returns
    ---
    selected_type : str
        Choosen type of distribution to apply
    normal_stadev : float
        Standard deviation for normal distribution
    uniform_range : float
        Range for uniform distribution  
    weibull_alpha : float
        Alpha value for weibull distribution
    '''
    # initialize with default values
    selected_type = default_parameter['selected_type']
    normal_stadev = default_parameter['normal_stadev_val']
    uniform_range = default_parameter['uniform_range_val']
    weibull_alpha = default_parameter['weibull_alpha_val']
    # selection for distribution type
    selected_type = selectbox(
        label = 'Select a type of random distribution to apply', 
        options = selection,
        index = selection.index(default_parameter['selected_type']),
        key=f'{key}_sb'
    )
    if selected_type == selection[0]: # Normal distribution
        normal_stadev = slider(
            label = 'Adjust standard deviation of the normal distribution',
            min_value = default_parameter['normal_stadev_min'],
            max_value = default_parameter['normal_stadev_max'],
            value = default_parameter['normal_stadev_val'],
            step = default_parameter['normal_stadev_stp'],
            help = info_text['distributions']['normal_stadev'],
            key=f'{key}_s1',
        )
    if selected_type == selection[1]: # Uniform distribution
        uniform_range = slider(
            label = 'Adjust the range of the uniform distribution',
            min_value = default_parameter['uniform_range_min'],
            max_value = default_parameter['uniform_range_max'],
            value = default_parameter['uniform_range_val'],
            step = default_parameter['uniform_range_stp'],
            help = info_text['distributions']['uniform_range'],
            key=f'{key}_s2',
        )
    if selected_type == selection[2]: # Weibull distribution
        weibull_alpha = slider(
            label = 'Adjust scale of the weibull distribution',
            min_value = default_parameter['weibull_alpha_min'],
            max_value = default_parameter['weibull_alpha_max'],
            value = default_parameter['weibull_alpha_val'],
            step = default_parameter['weibull_alpha_stp'],
            help = info_text['distributions']['weibull_alpha'],
            key=f'{key}_s3',
        )

    return selected_type, normal_stadev, uniform_range, weibull_alpha

def bool_to_numeric(val : bool) -> int:
    '''Simple bool conversion, necessary for the .toml files'''
    if val:
        return 1
    else: 
        return 0  

def show_linear_basis(Config : Configuration) -> None: 
    '''Simple checkbox to toggle visualization of linear basis of the baseline'''
    Config.show_linear_basis = bool_to_numeric(sidebar.checkbox(
        'Display the linear basis according to the Baseline', 
        value=Config.show_linear_basis))

def show_linear_basis_observation(Config : Configuration) -> None: 
    '''Simple checkbox to toggle visualization of linear basis of each anomaly'''
    Config.show_linear_basis_observation = bool_to_numeric(sidebar.checkbox(
        'Display the linear basis of each generated anomaly', 
        value=Config.show_linear_basis_observation))

def update_config(Config : Configuration ) -> None:

    parameter = load(Path(get_root()) / 'config//parameter.toml')
    # Modify field
    parameter['base']['init_x'] = list(Config.x_steps.values())
    parameter['base']['init_y'] = list(Config.y_steps.values())

    # randomize scattering
    parameter['randomize_scattering']['apply'] = Config.rnd_scattering_apply
    parameter['randomize_scattering']['selected_type'] = Config.rnd_scattering_selected_type
    parameter['randomize_scattering']['normal_stadev_val'] = Config.rnd_scattering_normal_stadev
    parameter['randomize_scattering']['uniform_range_val'] = Config.rnd_scattering_uniform_range
    parameter['randomize_scattering']['weibull_alpha_val'] = Config.rnd_scattering_weibull_alpha

    # update default values for all amounts 
    parameter['amounts']['number_of_ok'] = Config.number_of_ok
    parameter['amounts']['number_of_ok_to_plot'] = Config.number_of_ok_to_plot 

    # update default values for smoothing filter 
    parameter['filter']['list_of_types'] = Config.types
    parameter['filter']['selected_type'] = Config.selected_type
    parameter['filter']['filter_sg_window_length'] = Config.filter_sg_window_length
    parameter['filter']['filter_sg_poly_order'] = Config.filter_sg_poly_order

    # update default values for random scattering
    parameter['randomize_scattering']['apply'] = Config.rnd_scattering_apply
    parameter['randomize_scattering']['selected_type'] = Config.rnd_scattering_selected_type
    parameter['randomize_scattering']['normal_stadev_val'] = Config.rnd_scattering_normal_stadev
    parameter['randomize_scattering']['uniform_range_val'] = Config.rnd_scattering_uniform_range
    parameter['randomize_scattering']['weibull_alpha_val'] = Config.rnd_scattering_weibull_alpha

    # update default values for randomizing the tightening phase
    parameter['randomize_tightening']['apply'] = Config.rnd_tightening_apply
    parameter['randomize_tightening']['selected_type'] = Config.rnd_tightening_selected_type
    parameter['randomize_tightening']['normal_stadev_val'] = Config.rnd_tightening_normal_stadev
    parameter['randomize_tightening']['uniform_range_val'] = Config.rnd_tightening_uniform_range
    parameter['randomize_tightening']['weibull_alpha_val'] = Config.rnd_tightening_weibull_alpha
    parameter['randomize_tightening']['lower_xlimitation'] = Config.rnd_tightening_lower_xlimitation
    parameter['randomize_tightening']['upper_xlimitation'] = Config.rnd_tightening_upper_xlimitation

    # update default values for the vertical offset
    parameter['randomize_horizontal_offset']['apply'] = Config.offset_hori_apply
    parameter['randomize_horizontal_offset']['selected_points'] = Config.offset_hori_selected_points
    parameter['randomize_horizontal_offset']['selected_type'] = Config.offset_hori_selected_type
    parameter['randomize_horizontal_offset']['normal_stadev_val'] = Config.offset_hori_normal_stadev 
    parameter['randomize_horizontal_offset']['uniform_range_val'] = Config.offset_hori_uniform_range
    parameter['randomize_horizontal_offset']['weibull_alpha_val'] = Config.offset_hori_weibull_alpha 

    # update default values for the horizontal offset
    parameter['randomize_vertical_offset']['apply'] = Config.offset_vert_apply
    parameter['randomize_vertical_offset']['selected_points'] = Config.offset_vert_selected_points
    parameter['randomize_vertical_offset']['selected_type'] = Config.offset_vert_selected_type
    parameter['randomize_vertical_offset']['normal_stadev_val'] = Config.offset_vert_normal_stadev
    parameter['randomize_vertical_offset']['uniform_range_val'] = Config.offset_vert_uniform_range
    parameter['randomize_vertical_offset']['weibull_alpha_val'] = Config.offset_vert_weibull_alpha
    
    # update default values for additional preparations
    parameter['preparation']['remove_neg_y_values'] = Config.remove_neg_y_values
    # update default values for visualizations
    parameter['visualization']['show_linear_basis'] = Config.show_linear_basis

    # To use the dump function, you need to open the file in 'write' mode
    # It did not work if I just specify file location like in load
    f = open(Path(get_root()) / 'config//parameter.toml','w')
    dump(parameter, f)
    f.close()

    pass