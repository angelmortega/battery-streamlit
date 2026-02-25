# ==============================
# IMPORTS
# ==============================
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io

# ==============================
# PAGE SETUP
# ==============================
st.set_page_config(layout="wide")
st.title("🔋 Li-S Battery Charge–Discharge Visualizer")

plt.style.use("seaborn-v0_8-whitegrid")

# ==============================
# FILE UPLOAD
# ==============================
uploaded_file = st.file_uploader(
    "Upload XLS/XLSX battery file",
    type=["xls", "xlsx"]
)

view_mode = st.radio(
    "Select curves to display:",
    ["Both", "Charge (CCC)", "Discharge (CCD)"],
    horizontal=True
)

# ==============================
# LOAD FUNCTION (CACHED)
# ==============================
@st.cache_data
def load_excel(file):
    return pd.read_excel(file, sheet_name='Record')

# ==============================
# MAIN APP FLOW
# ==============================
if uploaded_file is not None:

    df_record = load_excel(uploaded_file)

    st.subheader("Preview")
    st.dataframe(df_record.head())

    # --------------------------
    # CLEANING
    # --------------------------
    df_record = df_record.drop(
        columns=[
            'Capacity/uAh',
            'SysTime',
            'StepTime',
            'SOC|DOD/%',
            'Energy/uWh',
            'SysTime'
        ],
        errors="ignore"
    )

    df_record = df_record[~(df_record['StepStatus'] == 'R')]
    df_record = df_record[df_record['StepNo'] >= 3]

    # --------------------------
    # SPLIT DATA
    # --------------------------
    df_record_c = df_record[df_record['StepStatus'] == 'CCC']
    df_record_d = df_record[df_record['StepStatus'] == 'CCD']

    # --------------------------
    # PLOTTING
    # --------------------------
    fig, ax = plt.subplots(figsize=(6,4))


    plot_sets = []

    if view_mode == "Both":
        plot_sets = [(df_record_c, 'CCC'), (df_record_d, 'CCD')]
    elif view_mode == "Charge (CCC)":
        plot_sets = [(df_record_c, 'CCC')]
    elif view_mode == "Discharge (CCD)":
        plot_sets = [(df_record_d, 'CCD')]

    for df_subset, mode in plot_sets:
        for cycle, group in df_subset.groupby('CycleNo'):
            color = "red" if mode == "CCC" else "blue"
            ax.plot(
                group['SpeCap/mAh/g'],
                group['Voltage/V'],
                color=color,
                alpha=0.8,
                linewidth=1.5)

    # --------------------------
    # AXIS FORMATTING
    # --------------------------
    ax.set_xlabel('SpeCap/mAh/g')
    ax.set_ylabel('Voltage/V')
    ax.set_title('Voltage vs Capacity')

    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # ==============================
    # DOWNLOAD BUTTON
    # ==============================
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)

    st.download_button(
        label="📥 Download Plot (PNG)",
        data=buf,
        file_name="battery_charge_discharge.png",
        mime="image/png"
    )

    # ==============================
    # DISPLAY (CENTERED SMALLER FIGURE)
    # ==============================
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.pyplot(fig)
