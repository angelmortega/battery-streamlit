import streamlit as st
import pandas as pd

COLUMNS_TO_DROP = [
    'Capacity/uAh',
    'SysTime',
    'StepTime',
    'SOC|DOD/%',
    'Energy/uWh',
]


@st.cache_data
def load_excel(file):
    return pd.read_excel(file, sheet_name='Record')


def clean_data(df):
    df = df.drop(columns=COLUMNS_TO_DROP, errors="ignore")
    df = df[df['StepStatus'] != 'R']
    df = df[df['StepNo'] >= 3]
    return df


def split_by_mode(df):
    df_charge = df[df['StepStatus'] == 'CCC']
    df_discharge = df[df['StepStatus'] == 'CCD']
    return df_charge, df_discharge


def get_available_cycles(df):
    return sorted(df['CycleNo'].unique())


def cycle_selector(all_cycles):
    filter_mode = st.sidebar.radio(
        "Cycle filter",
        ["All", "Multiples of 5", "Multiples of 10", "Custom"],
    )

    if filter_mode == "All":
        return all_cycles
    elif filter_mode == "Multiples of 5":
        return [c for c in all_cycles if c % 5 == 0]
    elif filter_mode == "Multiples of 10":
        return [c for c in all_cycles if c % 10 == 0]
    else:
        return st.sidebar.multiselect(
            "Select cycles to display",
            options=all_cycles,
            default=all_cycles,
        )
