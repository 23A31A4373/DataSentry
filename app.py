
import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------


# CUSTOM CSS


st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F5F7FB;
    color: #1E293B;
}

/* Main headings */
h1, h2, h3 {
    color: #172554 !important;
}

/* All normal text */
.stApp p,
.stApp label,
.stApp span,
.stApp li {
    color: #334155;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1E293B;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #F8FAFC !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 20px;
    border-radius: 12px;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #2563EB !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #475569 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border: 1px dashed #94A3B8;
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stDownloadButton button,
.stButton button {
    background-color: #2563EB;
    color: #FFFFFF !important;
    border-radius: 8px;
    border: none;
}

.stDownloadButton button:hover,
.stButton button:hover {
    background-color: #1D4ED8;
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# SIDEBAR

with st.sidebar:
    st.title("🔍 DataSentry")

    st.caption("CSV DATA QUALITY ANALYZER")

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "Data Cleaning",
            "About"
        ]
    )

    st.divider()

    st.caption("Built with Python and Pandas")

# MAIN HEADER

st.title("DataSentry")
st.subheader("Your Data. Cleaner. Smarter.")

st.write(
    "Analyze your CSV datasets, identify quality issues "
    "and generate cleaner data."
)

st.write(
    "Upload your CSV dataset to inspect, analyze "
    "and improve its data quality."
)

# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

# Remove completely empty rows and columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    st.success("Dataset uploaded successfully!")

    # -----------------------------
    # DATASET OVERVIEW
    # -----------------------------

    st.header("📊 Dataset Overview")

    total_rows, total_columns = df.shape
    duplicates = df.duplicated().sum()
    missing_total = df.isnull().sum().sum()

    total_cells = df.size

    if total_cells > 0:
        quality_score = (
            (total_cells - missing_total) / total_cells
        ) * 100
    else:
        quality_score = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Rows", total_rows)
    col2.metric("Total Columns", total_columns)
    col3.metric("Duplicate Rows", duplicates)
    col4.metric("Data Quality Score", f"{quality_score:.1f}%")

    # -----------------------------
    # DATASET PREVIEW
    # -----------------------------

    st.header("📋 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    # -----------------------------
    # COLUMN INFORMATION
    # -----------------------------

    st.header("🔎 Column Information")

    info_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        info_df,
        use_container_width=True
    )

    # -----------------------------
    # MISSING VALUE ANALYSIS
    # -----------------------------

    st.header("⚠️ Missing Value Analysis")

    missing_data = df.isnull().sum()

    missing_data = missing_data[
        missing_data > 0
    ]

    if not missing_data.empty:

        st.bar_chart(missing_data)

        st.write("Columns containing missing values:")

        st.dataframe(
            missing_data.rename("Missing Count"),
            use_container_width=True
        )

    else:
        st.success("No missing values found!")

    # -----------------------------
    # DESCRIPTIVE STATISTICS
    # -----------------------------

    st.header("📈 Descriptive Statistics")

    st.dataframe(
        df.describe(include="all").transpose(),
        use_container_width=True
    )

    # -----------------------------
    # DATA CLEANING
    # -----------------------------

    st.header("🧹 Data Cleaning")

    remove_duplicates = st.checkbox(
        "Remove duplicate rows",
        value=True
    )

    clean_df = df.copy()

    if remove_duplicates:
        clean_df = clean_df.drop_duplicates()

    missing_action = st.selectbox(
        "How should we handle missing values?",
        [
            "Keep missing values",
            "Remove rows with missing values",
            "Fill numeric missing values with mean"
        ]
    )

    if missing_action == "Remove rows with missing values":
        clean_df = clean_df.dropna()

    elif missing_action == "Fill numeric missing values with mean":
        numeric_columns = clean_df.select_dtypes(
            include="number"
        ).columns

        clean_df[numeric_columns] = clean_df[
            numeric_columns
        ].fillna(clean_df[numeric_columns].mean())

    st.write(
        f"Original rows: {len(df)}"
    )

    st.write(
        f"Rows after cleaning: {len(clean_df)}"
    )

    st.write(
        f"Duplicate rows removed: {len(df) - len(clean_df)}"
    )

    # -----------------------------
    # DOWNLOAD CLEANED DATASET
    # -----------------------------

    csv_data = clean_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

else:

    st.info("Please upload a CSV file to begin analysis.")
