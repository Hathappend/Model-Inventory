import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm

# st.set_page_config(layout="wide")

def init():
    if 'guest' not in st.session_state:
        st.session_state['guest'] = {}

def calculate(OC, CC, L, Z):
    df = read_data()
    # Mengubah kolom 'Date' menjadi format datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    filtered_df = df[(df['State'] == st.session_state["stateSelected"]) & (df['Product'].isin(st.session_state["productSelected"]))]

    # Menghitung permintaan harian rata-rata dan standar deviasi harian untuk setiap produk di setiap area
    daily_stats = filtered_df.groupby(['State', 'Product']).agg(
        daily_avg_demand=('Sales', 'mean'),
        std_daily_demand=('Sales', 'std')
    ).reset_index()

    daily_stats['Service Level'] = (str(round(norm.cdf(Z) * 100))) + '%' 
    daily_stats['Lead Time'] = L

    #menghitung Yearly Demand
    annual_demand = np.ceil(daily_stats['daily_avg_demand'] * 365)

    daily_stats['Yearly Demand'] = annual_demand

    #menghitung EOQ
    daily_stats['EOQ'] = np.ceil(np.sqrt((2 * annual_demand * OC) / CC))

    # Menghitung Safety Stock (SS)
    daily_stats['Safety Stock'] = np.ceil(Z * daily_stats['std_daily_demand'] * np.sqrt(L))

    # Menghitung Reorder Point (ROP)
    daily_stats['ROP'] = np.ceil(( daily_stats['daily_avg_demand'] * L) + daily_stats['Safety Stock'])

    return daily_stats

def show_data(calculated_data):
    products = st.session_state['productSelected']
    for product in products:
        st.caption(product)
        daily_stats = calculated_data[calculated_data['Product'] == product]
        
        st.dataframe(daily_stats, hide_index=True)

        visualization(daily_stats)

def visualization(stats):
    order_quantity = stats['EOQ'].values[0]
    daily_demand = stats['daily_avg_demand'].values[0]
    rop = stats['ROP'].values[0]
    safety_stock = stats['Safety Stock'].values[0]
    lead_time = stats["Lead Time"].values[0]  # Asumsi waktu lead time

    # Plotting the lines
    num_cycles = 3  # Ubah jumlah siklus di sini
    time = np.arange(0, num_cycles * lead_time * 2, 1)  # Buat array waktu untuk empat siklus
    inventory_level = []

    # Menghitung level inventaris pada setiap waktu
    current_inventory = order_quantity
    daily_reduction = (order_quantity - rop) / lead_time

    for t in time:
        inventory_level.append(current_inventory)
        if t % (lead_time * 2) == lead_time * 2 - 1:
            current_inventory = order_quantity  # Reset to order_quantity after each full cycle
        else:
            if current_inventory > rop:
                current_inventory -= daily_reduction
            elif current_inventory > safety_stock:
                current_inventory -= daily_demand
            if current_inventory < safety_stock:
                current_inventory = safety_stock

    # Membuat grafik
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot inventory levels with vertical lines at lead time points
    for i in range(len(time) - 1):
        ax.plot([time[i], time[i + 1]], [inventory_level[i], inventory_level[i]], 'b-')
        if i + 1 < len(time):
            ax.plot([time[i + 1], time[i + 1]], [inventory_level[i], inventory_level[i + 1]], 'b-')

    # Plotting the Reorder Point (ROP) line as a full line
    ax.plot([0, num_cycles * lead_time * 2], [rop, rop], 'g-', label='Reorder Point (ROP)')

    # Plotting the Safety Stock (SS) line
    ax.plot([0, num_cycles * lead_time * 2], [safety_stock, safety_stock], 'r-', label='Safety Stock')

    # Plotting the Lead Time (LT) line
    for t in range(lead_time, num_cycles * lead_time * 2, lead_time):
        ax.axvline(x=t, color='b', linestyle='--', label='Lead Time' if t == lead_time else "")

    # Labels and title
    ax.set_title('Grafik EOQ, ROP, dan Safety Stock')
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Jumlah Pesanan')
    ax.legend()
    ax.grid(True)

    # Menampilkan grafik dalam Streamlit
    st.pyplot(fig)  

def read_data():
    return pd.read_csv("Coffee_Chain_Sales.csv")

def main():

    #inisialsisasi
    init()

    st.title("Kalkukasikan Stock")
    st.caption('Kalkulasi produk berdasarkan kota dan produk')

    df = read_data()

    getStateData = df['State'].unique().tolist()

    state = st.selectbox(
            "Pilih Kota yang ingin kalkulasi",
            (getStateData), 
            key="stateSelected")

    if state is None:
        st.session_state['stateSelected'] = getStateData[0]

    if st.session_state['stateSelected']:
        get_produk_by_state = df[df['State'] == state]['Product']

        products = st.multiselect(
        "Pilih produk yang ingin di kalkulasi",
        get_produk_by_state.unique())

        if products:

            st.session_state['productSelected'] = products

            inputCol1, inputCol2 = st.columns(2)
            
            with inputCol1:
                OC = st.number_input("Biaya Pemesanan (Order Cost)", min_value=1, value=100)
                L = st.number_input("Masa Tunggu datang Pesanan (Lead Time)", min_value=1, value=7)
            with inputCol2:
                CC = st.number_input("Biaya Simpan (Carrying Cost)", min_value=1, value=2)
                Z = st.number_input("Target Tingkat Pelayanan (Service Level) dalan satuan '%'", min_value=75.0, max_value=99.9, step=1.0, value=95.0)
                
                z_score = 0
                if Z == 99.9:
                    z_score = norm.ppf(Z/100)
                else:
                    Z = math.floor(Z) 
                    z_score = norm.ppf(Z/100)

            if st.button("Kalkulasikan Sekarang", type="primary", use_container_width=True):
                calculated_data = calculate(OC, CC, L, round(z_score,2))
                show_data(calculated_data)

                session_name = f"{state}_state"
                st.session_state[session_name] = calculated_data

                st.success("Data berhasil di simpan")
                
        

if __name__ == "__main__":
    main()