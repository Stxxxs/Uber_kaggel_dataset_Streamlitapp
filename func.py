import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
# import plotly as plt
# import plotly.express as px


def create_pie_chart(df, reasons, title, start_date, end_date, colors, reason_list):
    """Единая функция для построения диаграмм"""
    fig, ax = plt.subplots(figsize=(12, 10))

    if reasons.sum() > 0:
        ax.pie(
            reasons,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1},
            textprops={'fontsize': 20, 'weight': 'bold', 'color': 'white'}
        )
        ax.legend(reason_list, loc="upper center", bbox_to_anchor=(0.5, -0.1), labelcolor='black', fontsize=16, ncol=2)
    else:
        ax.text(0, 0, "No data", ha='center', color='#5a5a5a')

    ax.axis('equal')
    plt.title(f"{title}\n{start_date} — {end_date}", pad=20, fontsize=24)
    return fig


def date_control(df, title, key_suffix):
    """Простой фильтр по датам как строки"""
    all_dates = sorted(df['Date'].unique())
    min_date, max_date = all_dates[0], all_dates[-1]

    start, end = st.date_input(
        title,
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        key=f"date_{key_suffix}"
    )

    # Конвертация в строки для сравнения
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    return df[(df['Date'] >= start_str) & (df['Date'] <= end_str)], start_str, end_str


def day_of_week_filter(df, key_suffix):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    selected = st.multiselect('Days', days, default=days, key=f'days_{key_suffix}')
    if selected:
        df = df.copy()
        df['Weekday'] = pd.to_datetime(df['Date']).dt.day_name()
        return df[df['Weekday'].isin(selected)]
    return df

