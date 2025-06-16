# Streamlit dashboard for visualization (optional)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    st.title("Swarm Traffic Simulation Dashboard")
    st.write("Visualize simulation results here.")
    # Load metrics
    try:
        df = pd.read_csv("results\\logs\\metrics.csv")
        st.line_chart(df.set_index(df.columns[0]))
        st.bar_chart(df.mean(numeric_only=True))
    except Exception as e:
        st.warning(f"Metrics not found or error: {e}")

    # Show simulation screenshots
    st.header("Simulation Screenshots")
    img_folder = "results/screenshots"
    if os.path.exists(img_folder):
        img_files = [f for f in sorted(os.listdir(img_folder)) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        if img_files:
            for img_file in img_files:
                st.image(os.path.join(img_folder, img_file), caption=img_file)
        else:
            st.info("No screenshots found in 'results/screenshots/'.")
    else:
        st.info("No screenshots folder found. Save screenshots from SUMO-GUI to 'results/screenshots/'.")

    # # Show simulation video
    # st.header("Simulation Video")
    # video_path = "results/video/simulation.mp4"
    # if os.path.exists(video_path):
    #     st.video(video_path)
    # else:
    #     st.info("No video found. Save a video from SUMO-GUI to 'results/video/simulation.mp4'.")

if __name__ == "__main__":
    main()
