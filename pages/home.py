import streamlit as st

from utils.load import get_image


def run():

    home_sb()
    home()


def home() -> None:

    st.header("General Information regarding the Use of Screw Data")

    st.subheader("Purpose")

    st.write(
        'The generator "Screw Data" provides an easy way to generate screw-driving data. It uses a simple linear baseline\
        to synthetically generate a desired number of correct and faulty observations. '
    )

    st.subheader("Process")

    st.image(get_image("flow_chart.png"), use_column_width=True)


def home_sb() -> None:

    st.sidebar.subheader("Additional Information")

    with st.sidebar.expander("Parameter Selection"):
        st.write(
            "The tool is designed in such a way that all parameter entries can be made in the side menu. No entries can\
         be made on the main page. This is where the visualization of parameter decisions and results takes place "
        )

    with st.sidebar.expander("Parameter storage"):
        st.write(
            "As you navigate the tool, the parameter will be saved. At download, they are used to generate the data set."
        )

    with st.sidebar.expander("Parameter import"):
        st.write(
            "You can import parameter from previous usage in the following section"
        )

    st.sidebar.subheader("Import Parameter")

    with st.sidebar.expander("Import from file"):
        st.write("TO DO")
