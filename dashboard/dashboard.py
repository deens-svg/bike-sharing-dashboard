import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Gagal memuat dataset main_data.csv. Pastikan file ada di folder dashboard/")
    st.stop()

# Sidebar Filter
st.sidebar.title("🚲 Bike Sharing Filter")
min_date = df['dteday'].min()
max_date = df['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Main Title & Metrics
st.title("🚲 Bike Sharing Data Analysis Dashboard")
st.markdown("Dashboard ini menampilkan visualisasi data penyewaan sepeda berdasarkan rentang waktu yang dipilih.")

col1, col2 = st.columns(2)
with col1:
    total_orders = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan Sepeda", value=f"{total_orders:,}")
with col2:
    avg_orders = int(filtered_df['cnt'].mean()) if not filtered_df.empty else 0
    st.metric("Rata-rata Penyewaan per Hari", value=f"{avg_orders:,}")

st.divider()

# Visualisasi 1: Tren Penyewaan
st.subheader("Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(filtered_df['dteday'], filtered_df['cnt'], marker='o', linewidth=1.5, color='#72BCD4')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# Visualisasi 2: Penyewaan Berdasarkan Cuaca
st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")
if 'weathersit' in filtered_df.columns:
    weather_df = filtered_df.groupby('weathersit')['cnt'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x='weathersit', y='cnt', data=weather_df, palette='Blues_d', ax=ax2)
    ax2.set_xlabel("Kondisi Cuaca (1: Cerah, 2: Mendung/Kabut, 3: Hujan/Salju Ringan)")
    ax2.set_ylabel("Total Penyewaan")
    st.pyplot(fig2)
