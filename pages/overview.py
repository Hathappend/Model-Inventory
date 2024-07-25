import streamlit as st
import pages.calculate as calculate

def main():
    st.title("Overview")
    st.caption('Deskripsi dan tutorial penggunaan')

    st.markdown('''
    **Studi Kasus**: Implementasi model inventory Economical Order Quantity (EOQ) berdasarkan **Coffee Shop Chain Dataset**
                     . Program berbasis website ini akan mengkalkulasikan stok berdasarka **kota dan produk** dengan menghitung EOQ
                     ditambah dengan Reorder Point (ROP) dan Safety Stock (SS) untuk memastikan tidak adanya kekurangan stok 
                     terutama pada saat Lead Time. 
    ''')

    st.subheader("Dataset")
    st.caption('Berikut adalah overview dari dataset yang di gunakan yaitu Cofee Shop Chain')
    st.dataframe(calculate.read_data(), hide_index=True)

    st.subheader("Tutorial Penggunaan")
    st.caption('Berikut adalah cara menggunakan/mengkalkulasikan *recommended stock*')

    st.markdown('** Calculate : ** ' )
    st.markdown('1. Masuk ke tab/menu **Calculate** pada sidebar' )
    st.markdown('2. Pilih kota yang ingin di kalkulasikan' )
    st.markdown('3. Pilih Produk mana saja yang ingin di kalkulasikan' )
    st.markdown('4. Masukkan **Biaya Pemesanan**, **Biaya Simpan**, **Lead Time**, dan **Service Level**' )
    st.markdown('5. Klik kalkulasikan' )
    st.caption('_Note:_ Untuk batas pengisian Servide Level itu *75% - 99,9%* ')

    st.image('z-score.webp', caption='Service Level (Z-Score)')

    st.markdown('** Melihat Rekapitulasi : ** ' )
    st.markdown('1. Masuk ke tab/menu **Rekapitulasi** pada sidebar' )
    st.markdown('2. Pilih kota yang ingin di lihat hasil perhitungan **recommended stock**' )

if __name__ == "__main__":
    main()