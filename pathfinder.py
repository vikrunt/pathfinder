import os
import pandas as pd
import streamlit as st
from pathlib import Path
from io import BytesIO

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

# Folder selection using text input
folder_path = st.text_input("📂 Enter the main folder path (e.g., D:\\Mar-25):")

if folder_path.strip() != "":
    try:
        folder = Path(folder_path).resolve(strict=False)
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

                # Prepare Excel for download
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)

                # Download button with styling
                st.markdown("### 📥 Download the file")
                st.download_button(
                    label="✨ Download Excel",
                    data=output,
                    file_name="file_paths.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("⚠️ No files found in the selected folder.")
        else:
            st.error("❌ Invalid folder path. Please enter a valid path.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
