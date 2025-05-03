import math
import streamlit as st

st.set_page_config(layout="wide")
st.title("Option Order Calculator")

# Segment and Lot Size
col_seg, col_lot = st.columns([3, 1])
with col_seg:
    segment = st.radio("Segment", ["Nifty", "Sensex", "BankNifty", "FinNifty", "MIDC"], horizontal=True)
with col_lot:
    segment_lot_sizes = {
        "Nifty": 75,
        "Sensex": 20,
        "BankNifty": 30,
        "FinNifty": 65,
        "MIDC": 120
    }
    lot_size = segment_lot_sizes[segment]
    st.number_input("Lot Size", value=lot_size, step=1, disabled=True, label_visibility="collapsed")

# Input and Summary Side by Side
col1, col2 = st.columns([2, 1])

with col1:
    # Initial Capital Input
    st.markdown("**Initial Capital (Rs) or enter manually**")
    cap_col1, cap_col2 = st.columns([2, 1])
    capital_options = [i for i in range(50000, 10000001, 50000)] + ["Custom"]
    with cap_col1:
        selected_capital_option = st.selectbox("Choose or select custom", capital_options, label_visibility="collapsed")
    with cap_col2:
        custom_capital = st.number_input(" ", value=50000.0, step=1000.0, label_visibility="collapsed", disabled=(selected_capital_option != "Custom"))
    initial_capital = float(custom_capital if selected_capital_option == "Custom" else selected_capital_option)

    # LTP Input
    st.markdown("**LTP (Last Traded Price) or enter manually**")
    ltp_col1, ltp_col2 = st.columns([2, 1])
    ltp_options = [i for i in range(100, 301, 10)] + ["Custom"]
    with ltp_col1:
        selected_ltp_option = st.selectbox("Choose or select custom", ltp_options, label_visibility="collapsed")
    with ltp_col2:
        custom_ltp = st.number_input("  ", value=200.0, step=1.0, label_visibility="collapsed", disabled=(selected_ltp_option != "Custom"))
    ltp = float(custom_ltp if selected_ltp_option == "Custom" else selected_ltp_option)

    # Capital Percentage
    capital_percent = st.slider("Capital Percentage to Use (%)", min_value=25, max_value=100, step=25, value=75)

    calculate = st.button("Calculate Order")
# Calculation logic
def calculate_order(initial_capital, ltp, lot_size, capital_percent):
    usable_capital = (capital_percent / 100) * initial_capital
    total_units = usable_capital / ltp

    # Calculate both floor and ceil lot sizes
    floor_lots = math.floor(total_units / lot_size)
    ceil_lots = math.ceil(total_units / lot_size)

    # Calculate total cost for both
    floor_cost = floor_lots * lot_size * ltp
    ceil_cost = ceil_lots * lot_size * ltp

    # Choose the one closer to usable capital
    if abs(floor_cost - usable_capital) < abs(ceil_cost - usable_capital):
        full_lots = floor_lots
        total_cost = floor_cost
    else:
        full_lots = ceil_lots
        total_cost = ceil_cost

    total_buyable_units = full_lots * lot_size

    summary = {
        "Initial Capital (Rs)": initial_capital,
        "Capital Used (%)": capital_percent,
        "Usable Capital (Rs)": usable_capital,
        "LTP (Rs)": ltp,
        "Lot Size": lot_size,
        "Total Options (Units)": int(total_units),
        "Total Buyable Units": total_buyable_units,
        "Full Lots": full_lots,
        "Total Cost (Rs)": total_cost,
        "Remaining Capital (Rs)": usable_capital - total_cost
    }
    return summary

# Right side output
if calculate:
    result = calculate_order(initial_capital, ltp, lot_size, capital_percent)
    with col2:
        st.subheader("📊 Order Summary")
        for key, value in result.items():
            # st.write(f"**{key}**: {value}")
            if key == "Total Buyable Units":
                st.markdown(f"<span style='color:green'><strong>{key}:</strong> {value}</span>", unsafe_allow_html=True)
            else:
                st.write(f"**{key}**: {value}")


