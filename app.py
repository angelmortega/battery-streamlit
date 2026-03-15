import streamlit as st
import matplotlib.pyplot as plt
import io

from utils.data_loader import load_excel, clean_data, split_by_mode, get_available_cycles, cycle_selector
from utils.plotting import build_plot_sets, plot_matplotlib

st.set_page_config(layout="wide")
st.title("🔋 Li-S Battery Charge–Discharge Visualizer")

plt.style.use("seaborn-v0_8-whitegrid")

uploaded_file = st.file_uploader(
    "Upload XLS/XLSX battery file",
    type=["xls", "xlsx"]
)

view_mode = st.radio(
    "Select curves to display:",
    ["Both", "Charge (CCC)", "Discharge (CCD)"],
    horizontal=True
)

if uploaded_file is not None:
    df_record = load_excel(uploaded_file)

    st.subheader("Preview")
    st.dataframe(df_record.head())

    df_record = clean_data(df_record)

    # Cycle selection
    all_cycles = get_available_cycles(df_record)
    selected_cycles = cycle_selector(all_cycles)

    df_record = df_record[df_record['CycleNo'].isin(selected_cycles)]

    df_charge, df_discharge = split_by_mode(df_record)
    plot_sets = build_plot_sets(df_charge, df_discharge, view_mode)

    fig = plot_matplotlib(plot_sets)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)

    st.download_button(
        label="📥 Download Plot (PNG)",
        data=buf,
        file_name="battery_charge_discharge.png",
        mime="image/png"
    )

    # Display centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig)
