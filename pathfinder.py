import os
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="✨ File Path Explorer", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {background-color: #1f1f2e; color: #e0e0eb; font-family: Arial, sans-serif;}
    .stTextInput label {font-size: 18px; font-weight: bold; color: #ffa500;}
    .stButton button {background-color: #4caf50; color: white; font-size: 16px; padding: 10px 20px;}
    .stDataFrame {border-radius: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);}
    </style>
""", unsafe_allow_html=True)

st.title("✨ File Path Explorer")

# Folder selection
folder_path = st.text_input("📂 Enter the main folder path:")

if folder_path:
    folder = Path(folder_path)
    if folder.exists() and folder.is_dir():
        file_data = []

        # Traverse folder structure
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_data.append({"File Name": file, "Path": file_path})

        # Display and export results
        if file_data:
            df = pd.DataFrame(file_data)
            st.dataframe(df)

            # Download button with styling
            st.markdown("### 📥 Download the file")
            if st.download_button(
                label="✨ Download Excel",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name="file_paths.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                st.success("✅ File downloaded successfully.")
        else:
            st.warning("⚠️ No files found in the selected folder.")
    else:
        st.error("❌ Invalid folder path. Please enter a valid path.")
