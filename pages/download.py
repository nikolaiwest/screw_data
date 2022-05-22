import streamlit as st
import pandas as pd

from utils.configuration import Configuration
from utils.observation import Observation
from utils.load import get_image
from utils.plot import plot_multiple_observations


def run(Config: Configuration, parameter: dict, info_text: dict) -> None:
    """Function to run the menu page "Download" that consists of a sidebar and the main page."""
    # display sidebar
    download_sb(Config, parameter, info_text)
    # display 'download' page
    download(Config, parameter, info_text)


def download_sb(
    Config: Configuration,
    parameter: dict,
    info_text: dict,
) -> None:

    st.sidebar.subheader("Settings for the Download")
    st.sidebar.write("Side bar Download")


def download(
    Config: Configuration,
    parameter: dict,
    info_text: dict,
) -> None:

    st.header("Download")

    # display summary of the created Config/dataset
    download_summary(Config)

    download_execute(Config)


def download_summary(Config: Configuration) -> None:
    """Function to create the page subsection displaying a simple summary."""
    st.subheader("Summary of the selected screw run observations to create")
    col1, col2, col3, col4, col5 = st.columns(5)
    count_normal = Config.number_of_ok
    count_type_1 = Config.anomaly_type_1_generate_amount
    count_type_2 = Config.anomaly_type_2_generate_amount
    count_type_3 = Config.anomaly_type_3_generate_amount
    count_type_4 = Config.anomaly_type_4_generate_amount
    count_total = (
        count_normal + count_type_1 + count_type_2 + count_type_3 + count_type_4
    )

    col1.image(get_image("anomaly_type_01.png"), use_column_width="auto")
    col1.metric(
        "Normal observations",
        int(count_normal),
        f"{(count_normal/count_total)*100:.2f}%",
        delta_color="normal",
    )
    col2.image(get_image("anomaly_type_01.png"), use_column_width="auto")
    col2.metric(
        "Anomalies of Type 1",
        int(count_type_1),
        f"{(count_type_1/count_total)*100:.2f}%",
        delta_color="inverse",
    )
    col3.image(get_image("anomaly_type_02.png"), use_column_width="auto")
    col3.metric(
        "Anomalies of Type 2",
        int(count_type_2),
        f"{(count_type_2/count_total)*100:.2f}%",
        delta_color="inverse",
    )
    col4.image(get_image("anomaly_type_03.png"), use_column_width="auto")
    col4.metric(
        "Anomalies of Type 3",
        int(count_type_3),
        f"{(count_type_3/count_total)*100:.2f}%",
        delta_color="inverse",
    )
    col5.image(get_image("anomaly_type_04.png"), use_column_width="auto")
    col5.metric(
        "Anomalies of Type 4",
        int(count_type_4),
        f"{(count_type_4/count_total)*100:.2f}%",
        delta_color="inverse",
    )

    Obs_preview = []
    for _ in range(int(Config.number_of_ok_to_plot)):
        Obs_preview.append(Observation(Config, obs_type="ok"))
    for _ in range(int(Config.anomaly_type_1_generate_amount_to_plot)):
        Obs_preview.append(Observation(Config, obs_type="anomaly_type_01"))
    for _ in range(int(Config.anomaly_type_2_generate_amount_to_plot)):
        Obs_preview.append(Observation(Config, obs_type="anomaly_type_02"))
    for _ in range(int(Config.anomaly_type_3_generate_amount_to_plot)):
        Obs_preview.append(Observation(Config, obs_type="anomaly_type_03"))
    for _ in range(int(Config.anomaly_type_4_generate_amount_to_plot)):
        Obs_preview.append(Observation(Config, obs_type="anomaly_type_04"))

    plot_multiple_observations(
        observations=Obs_preview,
        Config=Config,
        use_default_color=False,
        plot_title=f"Exemplary Visualization of all observations \
(#normal={int(Config.number_of_ok_to_plot)}; \
#type_1={int(Config.anomaly_type_1_generate_amount_to_plot)}; \
#type_2={int(Config.anomaly_type_2_generate_amount_to_plot)}; \
#type_3={int(Config.anomaly_type_3_generate_amount_to_plot)}; \
#type_4={int(Config.anomaly_type_4_generate_amount_to_plot)})",
    )


def download_execute(Config: Configuration) -> None:
    """Function to execute the generation of screw data and to download it."""
    st.subheader("Generate the data set according to the current parameter selection")

    @st.cache
    def convert_df(df):
        return df.to_csv().encode("utf-8")

    df = pd.DataFrame([0, 1, 2, 3])  # dummy...

    disable_download = True
    if st.button(label="Generate Screw Data"):
        df, disable_download = generate_data(Config)

    st.download_button(
        label="Download Data",
        data=convert_df(df),
        file_name="screw_data.csv",
        mime="text/csv",
        disabled=disable_download,
    )


def generate_data(Config: Configuration):
    # get individual type count from Config file
    count_normal = Config.number_of_ok
    count_type_1 = Config.anomaly_type_1_generate_amount
    count_type_2 = Config.anomaly_type_2_generate_amount
    count_type_3 = Config.anomaly_type_3_generate_amount
    count_type_4 = Config.anomaly_type_4_generate_amount
    # # list all counts for iteration
    amounts_listed = [
        count_normal,
        count_type_1,
        count_type_2,
        count_type_3,
        count_type_4,
    ]
    # create list to add up counts for iteration and simply add them up
    amounts_limits = [0]
    for i in range(5):
        amounts_limits.append(amounts_limits[i] + amounts_listed[i])
    # get sum of all amounts
    amounts_counted = sum(amounts_listed)

    # loop over amounts in spinner
    with st.spinner(f"Calculating paths for {amounts_counted} screw runs..."):
        # initialize progress bar
        bar = st.progress(0)

        # create emply list for observations
        df_as_list = []  # temporary... TODO: switch to dataframe format

        # iterate over total number of OK observations
        for idx in range(amounts_counted):
            # update the progress bar accordingly
            bar.progress(int((idx + 1) * (100 / (amounts_counted))))
            # get obs type
            obs_types = [
                "ok",
                "anomaly_type_1",
                "anomaly_type_2",
                "anomaly_type_3",
                "anomaly_type_4",
            ]
            # loop ofer obs types
            for i in range(5):
                if amounts_limits[i] <= 0 < amounts_limits[i + 1]:
                    obs_type = obs_types[i]
            # append value for the current obs type
            df_as_list.append(Observation(Config, obs_type=obs_type))

    # simple temp return for app testing
    return pd.DataFrame([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), False
