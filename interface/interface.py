import streamlit as st

from streamlit_option_menu import option_menu

from utils.load import get_config
from utils.observation import Observation
from utils.configuration import Configuration

from pages import baseline, home, normal, anormal, download


def launch():

    # get the config and text files
    parameter, info_text, readme = get_config(
        "parameter.toml", "info_text.toml", "readme.toml"
    )

    # config streamlit page
    st.set_page_config(
        page_title="Screw Data",
        page_icon=":wrench:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # set a custom sidebar width
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 450px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 450px;
            margin-left: -450px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # load the main menu for all pages
    selected = option_menu(
        menu_title=None,
        options=["Home", "Baseline", "Normal", "Anormal", "Download"],
        icons=["house", "caret-right", "check-circle", "x-circle", "download"],
        default_index=0,
        orientation="horizontal",
    )

    # set default view to sidebar
    st.sidebar.write("nikolai.west@udo.edu")
    st.sidebar.title("- 🔧 ————— Settings ————— 🔩 -")

    # import config from parameter (.toml)
    Config = Configuration(parameter)

    # run pages by selection in main menu
    if selected == "Home":
        home.run()
    if selected == "Baseline":
        baseline.run(Config, parameter, info_text)
    if selected == "Normal":
        normal.run(Config, parameter, info_text)
    if selected == "Anormal":
        anormal.run(Config, parameter, info_text)
    if selected == "Download":
        download.run(Config, parameter, info_text)
