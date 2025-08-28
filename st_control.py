import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
from func import *
# import plotly as plt
# import plotly.express as px


DATA_PATH = 'data/uber_data_prepared_1.csv'
# st.set_option('deprecation.showPyplotGlobalUse', False)
sns.set_style("darkgrid")

st.title('Uber Data Analytics Dashboard')
@st.cache_data
def load_data(nrows=10000):
    df = pd.read_csv(DATA_PATH, nrows=nrows)
    return df


# Загрузка данных
data_load_state = st.text('Loading data...')
df_uber = load_data()
df_uber['Date'] = pd.to_datetime(df_uber['Date'])
df_uber['Time'] = pd.to_datetime(df_uber['Time'], utc=True).dt.time
payment_order = ['UPI', 'Cash', 'Uber Wallet', 'Credit Card', 'Debit Card']
df_uber['Payment Method'] = pd.Categorical(df_uber['Payment Method'], categories=payment_order, ordered=True)
vehicle_order = ['eBike', 'Go Sedan', 'Auto', 'Premier Sedan', 'Bike', 'Go Mini', 'Uber XL']
df_uber['Vehicle Type'] = pd.Categorical(df_uber['Vehicle Type'], categories=vehicle_order, ordered=True)


# Гистограмма распределения времени поездок
st.subheader('Time of trips distribution')
df_filtered, start_date, end_date = date_control(df_uber, "Time filter for time of trips distribution", 'time_distr')
df_filtered = day_of_week_filter(df_filtered, 'time_distr')
if df_filtered.empty:
    st.warning("No data available for the selected date range.")
else:
    # --- Построение графика ---
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_filtered['SecondsFromMidnight'] / 3600, bins=48, color='#383838', ax=ax)
    ax.set_xlabel('Time of day (Hours from midnight)')
    ax.set_ylabel('Number of trips')
    ax.set_title(f'Travel Time Distribution ({start_date} — {end_date})')
    ax.set_xlim(0, 24)  # Часы суток
    ax.set_xticks(range(0, 25, 2))  # Каждые 2 часа
    # Отображаем график в Streamlit
    st.pyplot(fig)
    plt.close(fig)
    # --- Дополнительно: статистика ---
    st.caption(f"Total trips in period: {len(df_filtered)}")


# Две колонки для причин отмены
col1, col2 = st.columns(2)

# === ЛЕВАЯ КОЛОНКА: Клиенты ===
with col1:
    st.subheader('Reasons for Cancellation by Customers')

    df_cust, s, e = date_control(
        df_uber,
        "Select date range for Customers",
        "cust"
    )

    reasons = df_cust['Reason for cancelling by Customer'].value_counts().reindex(
        ['Driver is not moving towards pickup location', 'Driver asked to cancel',
         'AC is not working', 'Change of plans', 'Wrong Address'],
        fill_value=0
    )

    fig = create_pie_chart(
        df_cust,
        reasons,
        "Customers",
        s, e,
        ['#1a1a1a', '#2a2a2a', '#383838', '#4a4a4a', '#5a5a5a'],
        reasons.index.tolist()
    )
    st.pyplot(fig)
    plt.close(fig)

# === ПРАВАЯ КОЛОНКА: Водители ===
with col2:
    st.subheader('Reasons for Cancellation by Drivers')

    df_driv, s, e = date_control(
        df_uber,
        "Select date range for Drivers",
        "driv"
    )

    reasons = df_driv['Driver Cancellation Reason'].value_counts().reindex(
        ['Personal & Car related issues', 'Customer related issue',
         'More than permitted people in there', 'The customer was coughing/sick'],
        fill_value=0
    )

    fig = create_pie_chart(
        df_driv,
        reasons,
        "Drivers",
        s, e,
        ['#1a1a1a', '#2a2a2a', '#383838', '#4a4a4a'],
        reasons.index.tolist()
    )
    st.pyplot(fig)
    plt.close(fig)


# Гистограмма распределения способов оплаты
st.subheader('Payment Method')
df_filtered = day_of_week_filter(df_uber, 'pay_meth')
fig, ax = plt.subplots(figsize=(12, 9))
sns.histplot(y=df_filtered['Payment Method'].dropna(), color='#383838', hue_order=payment_order)
ax.tick_params(labelsize=16)
# plt.ylabel('Payment Method', fontsize=20)
plt.xlabel('Count', fontsize=20)
# plt.title('Payment Method')
plt.show()
st.pyplot(fig)


# Контрол со распределению заказов по разным типам транспорта
st.subheader('Vehicle Type')
df_filtered = day_of_week_filter(df_uber, 'veh_type')
fig, ax = plt.subplots(figsize=(12, 9))
sns.histplot(x=df_filtered['Vehicle Type'].dropna(), color='#383838', hue_order=vehicle_order)
ax.tick_params(labelsize=16)
# plt.xlabel('Vehicle Type', fontsize=20)
plt.ylabel('Count', fontsize=20)
# plt.title('Vehicle Type')
plt.show()
st.pyplot(fig)


# Контрол со статистикой по ценам бронирования разных типо транспорта
st.subheader('Value of booking various Vehicle Type')
df_filtered = day_of_week_filter(df_uber, 'veh_type_stats')
stats = df_filtered.groupby('Vehicle Type')['Booking Value'].agg(['mean', 'min', 'median', 'max']).round(2)
styled_table = stats.style\
    .background_gradient(cmap='Greys', subset=['mean', 'min', 'median', 'max'])\
    .format(precision=2, thousands=',')
st.dataframe(
    styled_table,
    column_config={
        "mean": st.column_config.NumberColumn("Mean", format="$%.2f"),
        "min": st.column_config.NumberColumn("Minimum", format="$%.2f"),
        "median": st.column_config.NumberColumn("Median", format="$%.2f"),
        "max": st.column_config.NumberColumn("Maximum", format="$%.2f")
    },
    height=300,
    use_container_width=True
)







