import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px


st.set_page_config(page_title="Data Transformer", layout="wide")

theme = st.sidebar.radio("🌓 Choose Theme", ["Dark Purple", "Cyber Light"])


if theme == "Cyber Light":
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(to right, #fff1f8, #e0c3fc);
                color: #222;
            }
            [data-testid="stSidebar"] {
                background-color: #f9eaff;
                color: #000;
                border-right: 2px solid #a259ff;
            }
            .glow-text {
                text-shadow: 0 0 5px #a259ff, 0 0 10px #a259ff, 0 0 20px #e959ff;
                color: #e0d6f5;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #a259ff);
                background-size: 400% 400%;
                animation: gradientBG 20s ease infinite;
                color: #e0d6f5;
            }
            [data-testid="stSidebar"] {
                background: rgba(30, 20, 60, 0.95);
                border-right: 2px solid #a259ff;
                box-shadow: 5px 0px 15px rgba(162, 89, 255, 0.4);
            }
            div[data-testid="stFileUploader"] {
                border: 2px dashed #a259ff;
                border-radius: 12px;
                padding: 15px;
                transition: all 0.3s ease-in-out;
            }
            div[data-testid="stFileUploader"]:hover {
                border-color: #e959ff;
                transform: scale(1.02);
            }
            .stButton > button {
                background: linear-gradient(90deg, #a259ff, #e959ff);
                color: white;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
                transition: all 0.3s ease-in-out;
                border: none;
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #e959ff, #a259ff);
                transform: scale(1.05);
                box-shadow: 0px 0px 15px rgba(233, 89, 255, 0.7);
            }
            .stDownloadButton > button {
                background: linear-gradient(90deg, #d77eff, #8c52ff);
                color: white;
                border-radius: 12px;
                padding: 12px 20px;
                transition: all 0.3s ease-in-out;
                font-weight: bold;
            }
            .stDownloadButton > button:hover {
                background: linear-gradient(90deg, #8c52ff, #d77eff);
                transform: scale(1.05);
                box-shadow: 0px 0px 15px rgba(140, 82, 255, 0.7);
            }
            .stDataFrame {
                border-radius: 12px;
                overflow: hidden;
                border: 2px solid #a259ff;
                box-shadow: 0px 0px 20px rgba(162, 89, 255, 0.3);
            }
            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .glow-text {
                text-shadow: 0 0 5px #a259ff, 0 0 10px #a259ff, 0 0 20px #e959ff;
                color: #e0d6f5;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Sidebar 
st.sidebar.title("🧨Data Transformer🧨")
st.sidebar.write("✨Convert, clean, and visualize your **Excel & CSV** files!")

# Main Title with Glowing Effect
st.markdown('<h1 class="glow-text">⚡ DataForge: Neon Convertor 💾</h1>', unsafe_allow_html=True)
st.write("🔄 Convert files, clean data, and visualize in **style**!")

# File Upload Section 
uploaded_files = st.file_uploader(
    "📤 Drag & Drop or Upload your Excel/CSV file",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

# Progress Bar Effect
if uploaded_files:
    st.success("📂 File(s) Uploaded Successfully!")
    progress_bar = st.progress(0)

    for i in range(100):
        progress_bar.progress(i + 1)

    st.success("✅ Processing Complete!")

    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the file based on type
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
            continue

        # Display File Information
        st.markdown(f"### 📄 `{file.name}`")
        st.write(f"**File Size:** {round(file.size / 1024, 2)} KB")
        st.write("🔍 **Data Preview:**")
        st.dataframe(df.head())

        # Dataset Summary
        st.write("📊 **Dataset Summary:**")
        st.write(df.describe())

        # Data Cleaning Section
        st.subheader("🧹 Data Cleaning")
        clean_col1, clean_col2 = st.columns(2)

        with clean_col1:
            if st.button(f"🗑 Remove Duplicates from `{file.name}`"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")

        with clean_col2:
            if st.button(f"📉 Fill Missing Values for `{file.name}`"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing values filled!")

        # Select Columns to Keep
        st.subheader("🎯 Choose Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for `{file.name}`", df.columns, default=df.columns)
        df = df[selected_columns]

        # Rename Columns
        st.subheader("✏️ Rename Columns")
        new_column_names = {}
        for col in selected_columns:
            new_name = st.text_input(f"Rename `{col}`", col)
            new_column_names[col] = new_name
        df.rename(columns=new_column_names, inplace=True)

        # Data Visualization with Enhanced Charts
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"📊 Show Visualization for `{file.name}`"):
            numeric_df = df.select_dtypes(include=["number"])
            if not numeric_df.empty:
                if numeric_df.shape[1] >= 2:
                    x_col = st.selectbox("Select X-axis:", numeric_df.columns, key=f"x_{file.name}")
                    y_col = st.selectbox("Select Y-axis:", numeric_df.columns, index=1, key=f"y_{file.name}")
                    st.plotly_chart(px.bar(df, x=x_col, y=y_col, title="📊 Bar Chart"), use_container_width=True)
                    st.plotly_chart(px.scatter(df, x=x_col, y=y_col, title="🔬 Scatter Plot"), use_container_width=True)
                else:
                    st.plotly_chart(px.histogram(df, x=numeric_df.columns[0], title="📈 Histogram"), use_container_width=True)

                if df.select_dtypes(exclude='number').shape[1] > 0:
                    cat_col = st.selectbox("Choose categorical column for pie chart:", df.select_dtypes(exclude='number').columns, key=f"cat_{file.name}")
                    pie_df = df.groupby(cat_col)[numeric_df.columns[0]].sum().reset_index()
                    st.plotly_chart(px.pie(pie_df, names=cat_col, values=numeric_df.columns[0], title="🥧 Pie Chart"), use_container_width=True)
            else:
                st.warning("⚠️ No numeric data available for charts.")

        # File Conversion Options
        st.subheader("🔄 Convert File")
        conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🎯 Convert `{file.name}` to {conversion_type}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download `{new_file_name}`",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type,
            )

# Sidebar Completion Message
st.sidebar.success("✨All files processed successfully!")
