import streamlit as st
import pages.calculate as calculate
import pages.recap as recap
import pages.overview as overview


st.set_page_config(layout="wide")

def main():

    # #inisialisasi session
    # if "frequency_tables" not in st.session_state:
    #     st.session_state['frequency_tables'] = {}

    # if 'guest' not in st.session_state:
    #     st.session_state.guest = {}

    # if 'productSelected' not in st.session_state:
    #     st.session_state['productSelected'] = list()

    # tampilan sidebar
    st.sidebar.title("Model Inventory")
    selected_tab = st.sidebar.radio("Menu", ["Overview", "Calculate","Rekapitulasi"])

    if selected_tab == "Overview":
        overview.main()
    elif selected_tab == "Calculate":
        calculate.main()
    elif selected_tab == "Rekapitulasi" :
        recap.main()


if __name__ == "__main__":
    main()
