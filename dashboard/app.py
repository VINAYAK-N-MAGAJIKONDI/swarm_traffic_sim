# Swarm Traffic Simulation - Comparative Analysis Dashboard
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Swarm Traffic Analytics", layout="wide")

def main():
    st.title("🚦 Swarm Intelligence Traffic Control: Thesis Analytics")
    st.markdown("""
    **Comparative Analysis** of Swarm Intelligence (PSO, ACO) vs Traditional Control (Static, Actuated).
    """)

    # 1. Load Data
    # Use absolute path relative to this script to ensure it works regardless of CWD
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(base_dir, "..", "results", "logs", "metrics.csv")
    log_file = os.path.abspath(log_file) # Normalize path
    if not os.path.exists(log_file):
        st.error(f"Log file not found at `{log_file}`. Please run `run_simulation.py` first.")
        return

    try:
        df = pd.read_csv(log_file)
    except Exception as e:
        st.error(f"Error reading metrics: {e}")
        return

    # CLEANUP: Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Force types to numeric to avoid "Empty graph" issues
    numeric_cols = ['step', 'avg_waiting_time', 'avg_co2', 'avg_halting_number', 'avg_vehicles', 'avg_occupancy']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Force algorithm to string
    if 'algorithm' in df.columns:
        df['algorithm'] = df['algorithm'].astype(str)

    # Sort by step
    if 'step' in df.columns:
        df = df.sort_values('step')

    if df.empty:
        st.warning("Metrics file is empty (after processing).")
        return

    # Cleanup: Filter out weird steps if any
    df = df.dropna(subset=['step'])
    df = df[df['step'] >= 0]
    
    # 2. KPI Section
    st.header("🏆 Performance Summary")
    
    # Aggregate stats by Algorithm
    summary = df.groupby('algorithm').agg({
        'avg_waiting_time': 'mean',
        'avg_co2': 'mean',
        'avg_halting_number': 'mean',
        'avg_vehicles': 'mean'
    }).reset_index()

    # Find Best and Baseline
    if summary.empty:
        st.error("Summary is empty. No valid data found for algorithms.")
        st.dataframe(df) # Show what we have
        return

    # We assume 'waiting_time' is the primary metric to minimize
    best_algo_row = summary.loc[summary['avg_waiting_time'].idxmin()]
    worst_algo_row = summary.loc[summary['avg_waiting_time'].idxmax()]
    
    best_algo_name = best_algo_row['algorithm']
    best_val = best_algo_row['avg_waiting_time']
    worst_val = worst_algo_row['avg_waiting_time']
    
    improvement = ((worst_val - best_val) / worst_val) * 100 if worst_val != 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Best Algorithm", value=best_algo_name)
    with col2:
        st.metric(label="Lowest Avg Wait Time", value=f"{best_val:.2f} s", delta=f"{improvement:.1f}% vs Worst")
    with col3:
        st.metric(label="Avg Queue Length (Best)", value=f"{best_algo_row['avg_halting_number']:.2f}")
    with col4:
        st.metric(label="Avg CO2 (Best)", value=f"{best_algo_row['avg_co2']:.2f}")

    st.divider()

    # 3. Time Series Analysis
    st.header("📈 Time-Series Analysis")
    
    # Helper to pivot for native charts
    def get_chart_data(metric):
        # pivot so columns are algorithms, index is step
        return df.pivot_table(index='step', columns='algorithm', values=metric)

    tab1, tab2, tab3 = st.tabs(["Waiting Time", "CO2 Emissions", "Queue Length"])
    
    with tab1:
        st.subheader("Average Waiting Time per Step")
        st.line_chart(get_chart_data('avg_waiting_time'))
        
    with tab2:
        st.subheader("Network CO2 Emissions per Step")
        st.line_chart(get_chart_data('avg_co2'))

    with tab3:
        st.subheader("Average Queue Length (Halting Vehicles)")
        st.line_chart(get_chart_data('avg_halting_number'))

    # 4. Comparative Bar Charts
    st.header("📊 Algorithm Comparison")
    
    # Prepare summary for charts (set index to algorithm)
    summary_chart = summary.set_index('algorithm')

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Average Waiting Time")
        st.bar_chart(summary_chart['avg_waiting_time'])
        
    with c2:
        st.subheader("Average CO2 Emissions")
        st.bar_chart(summary_chart['avg_co2'])

    # 5. Raw Data & Screenshots
    st.header("📂 Raw Data & Visualization")
    with st.expander("View Raw Metrics CSV"):
        st.dataframe(df)
        
    st.subheader("Simulation Screenshots")
    img_folder = "results/screenshots"
    if os.path.exists(img_folder):
        img_files = sorted([f for f in os.listdir(img_folder) if f.endswith('.png')])
        if img_files:
            # Show a slider to pick step
            selected_img = st.select_slider("Select Screenshot", options=img_files)
            st.image(os.path.join(img_folder, selected_img), caption=selected_img)
        else:
            st.info("No screenshots found.")
    else:
        st.info("No screenshot folder found.")

if __name__ == "__main__":
    main()
