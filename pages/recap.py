import streamlit as st
import pandas as pd
import pages.calculate as calculate

def show_data(calculated_data):
    products = calculated_data['Product']
    for product in products:
        st.caption(product)
        daily_stats = calculated_data[calculated_data['Product'] == product]
        
        st.dataframe(daily_stats, hide_index=True)

        calculate.visualization(daily_stats)

def main():

    st.title("Rekapitulasi Hasil Kalkukasi")
    st.caption('Kumpulan data hasil kalkulasi yang di simpan sebelumnya')

    getStateData = calculate.read_data()

    state = st.selectbox(
            "Pilih Kota untuk melihat hasil kalkulasi",
            (getStateData['State'].unique()))

    if state:
        session_key = f"{state}_state"
        if session_key in st.session_state:
            show_data(st.session_state[session_key])
        else:
            st.warning("Data belum di kalkulasi")
        

if __name__ == "__main__":
    main()

