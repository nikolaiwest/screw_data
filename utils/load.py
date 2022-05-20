from PIL import Image
from typing import Any, Dict, Tuple
from pathlib import Path

import toml

def get_root() -> str:
    return str(Path(__file__).parent.parent)

def get_image(name: str) -> Image:
    return Image.open(Path(get_root()) / f'images/{name}' )

def get_config(
    parameter_file: str, tooltips_file: str, readme_file: str 
    ) -> Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]:
    """Loads configuration from toml config files. 
    
    Parameters
    ----------
    parameter_file : str
        Filename of the parameter configuration file that can also be imported.
    tooltips_file : str
        Filename of the written information that are used as tooltips.
    readme_file : str
        Filename of the readme file with additional information and descriptions.
    
    Returns
    -------
    parameter_config : dict
        Parameter needed to create new Observation.
    tooltip_config : dict
        Written instructions for tooltips.
    readme_config : dict
        Written information for online texts.
    """
    parameter_config = toml.load(Path(get_root()) / f'config/{parameter_file}')
    tooltip_config = toml.load(Path(get_root()) / f'config/{tooltips_file}')
    readme_config = toml.load(Path(get_root()) / f'config/{readme_file}')
    
    return dict(parameter_config), dict(tooltip_config), dict(readme_config)