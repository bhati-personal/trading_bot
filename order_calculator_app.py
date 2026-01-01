import math
import streamlit as st
from services.segment_service import (
    load_segments,
    add_or_update_segment,
    delete_segment,
)

# ---------------- Page Config ----------------
st.set_page_config(layout="wide")
st.title("📈 Option Order Calculator")

# ---------------- Sidebar: Segment Management ----------------
st.sidebar.header("⚙️ Manage Segments")

segments = load_segments()

with st.sidebar.form("add_segment"):
    seg_name = st.text_input("Segment Name (e.g. NIFTY)")
    lot_size = st.number_input("Lot Size", min_value=1, step=1)
    save = st.form_submit_button("Save / Update")

    if save:
        if seg_name.strip():
            add_or_update_segment(seg_name, lot_size)
            st.sidebar.success("Segment saved")
            st.rerun()
        else:
            st.sidebar.error("Segment name required")

if segments:
    del_seg = st.sidebar.selectbox(
        "Delete Segment",
        ["-- Select --"] + list(segments.keys())
    )
    if del_seg != "-- Select --":
        if st.sidebar.button("Delete Segment"):
            delete_segment(del_seg)
            st.sidebar.warning("Segment deleted")
            st.rerun()

# ---------------- Segment & Lot Size ----------------
segments = load_segments()

if not segments:
    st.warning("No segments available. Add from sidebar.")
    st.stop()

col_seg, col_lot = st.columns([3, 1])

with col_seg:
    segment = st.radio(
        "Segment",
        list(segments.keys()) + ["CUSTOM"],
        horizontal=True
    )

with col_lot:
    if segment == "CUSTOM":
        lot_size = st.number_input(
            "Enter Lot Size",
            min_value=1,
            step=1,
            value=50
        )
    else:
        lot_size = segments[segment]
        st.number_input(
            "Lot Size",
            value=lot_size,
            disabled=True,
            label_visibility="collapsed"
        )

# ---------------- Layout ----------------
col1, col2 = st.columns([2, 1])

with col1:
    # -------- Initial Capital --------
    st.markdown("**Initial Capital (Rs)**")
    initial_capital = st.number_input(
        "Capital",
        min_value=1000.0,
        step=1000.0,
        value=50000.0,
        label_visibility="collapsed"
    )

    # -------- LTP --------
    st.markdown("**LTP (Last Traded Price)**")
    ltp = st.number_input(
        "LTP",
        min_value=1.0,
        step=1.0,
        value=200.0,
        label_visibility="collapsed"
    )

    # -------- Capital Percentage --------
    capital_percent = st.slider(
        "Capital Percentage to Use (%)",
        min_value=25,
        max_value=100,
        step=25,
        value=75
    )

    calculate = st.button("Calculate Order")

# ---------------- Calculation Logic ----------------
def calculate_order(initial_capital, ltp, lot_size, capital_percent):
    usable_capital = (capital_percent / 100) * initial_capital
    total_units = usable_capital / ltp

    floor_lots = math.floor(total_units / lot_size)
    ceil_lots = math.ceil(total_units / lot_size)

    floor_cost = floor_lots * lot_size * ltp
    ceil_cost = ceil_lots * lot_size * ltp

    if abs(floor_cost - usable_capital) <= abs(ceil_cost - usable_capital):
        full_lots = floor_lots
        total_cost = floor_cost
    else:
        full_lots = ceil_lots
        total_cost = ceil_cost

    return {
        "Segment": segment,
        "Initial Capital (Rs)": round(initial_capital, 2),
        "Capital Used (%)": capital_percent,
        "Usable Capital (Rs)": round(usable_capital, 2),
        "LTP (Rs)": round(ltp, 2),
        "Lot Size": lot_size,
        "Total Options (Units)": int(total_units),
        "Total Buyable Units": full_lots * lot_size,
        "Full Lots": full_lots,
        "Total Cost (Rs)": round(total_cost, 2),
        "Remaining Capital (Rs)": round(usable_capital - total_cost, 2),
    }

# ---------------- Output ----------------
if calculate:
    result = calculate_order(
        initial_capital,
        ltp,
        lot_size,
        capital_percent
    )

    with col2:
        st.subheader("📊 Order Summary")
        for key, value in result.items():
            if key == "Total Buyable Units":
                st.markdown(
                    f"<span style='color:green'><strong>{key}:</strong> {value}</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.write(f"**{key}**: {value}")
