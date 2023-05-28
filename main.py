import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import stemgraphic
from scipy import stats
from streamlit_lottie import st_lottie
import json
import requests

# Set page title and description
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")



def get_url(url:str):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

url=get_url("https://assets6.lottiefiles.com/packages/lf20_vvjhceqy.json")
url2=get_url(("https://assets6.lottiefiles.com/packages/lf20_qpsnmykx.json"))
url3=get_url("https://assets1.lottiefiles.com/packages/lf20_uxndffhr.json")


colx,coly=st.columns(2)
with colx:
    st.title("Data Analysis Dashboard")
    st.write("Upload a CSV or Excel file for Dashboard")
with coly:
    st_lottie(url)


# Upload file
uploaded_file = st.sidebar.file_uploader("Upload file", type=["csv", "xlsx"])

try:
    if uploaded_file is not None:
        # Determine file type
        file_type = "csv" if uploaded_file.type == "text/csv" else "excel"

        # Read file into DataFrame
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        # File Information
        st.sidebar.header("Created by Saksham ✨")
        st.sidebar.subheader("File Information")
        st.sidebar.write("File Name:", uploaded_file.name)
        st.sidebar.write("Number of Rows:", df.shape[0])
        st.sidebar.write("Number of Columns:", df.shape[1])
        

        # Missing Values
        st.sidebar.subheader("Missing Values")
        missing_values = pd.DataFrame(df.isnull().sum(), columns=["Missing Values"]).reset_index()
        missing_values.columns = ["Column", "Missing Values"]
        st.sidebar.dataframe(missing_values)
        # Data Types
        st.sidebar.subheader("Data Types")
        data_types = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index()
        data_types.columns = ["Column", "Data Type"]
        st.sidebar.dataframe(data_types)
        

        # Display the first few rows of the DataFrame
        st.subheader("Preview")
        st.dataframe(df.head())

        

        # Create columns for layout
        col1, col2, col3 = st.columns(3)

        # Summary Statistics
        with col1:
            st.subheader("Summary Statistics")
            st.write(df.describe())

        # Correlation Heatmap
        with col2:
            st.subheader("Correlation Heatmap")
            display_corr_heatmap = st.checkbox("Check Correlation Heatmap")
            if display_corr_heatmap:
                corr = df.corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

        # Histogram
        with col3:
            st.subheader("Histogram")
            selected_column_hist = st.selectbox("Select a column for the histogram", df.columns)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(data=df, x=selected_column_hist, kde=True, ax=ax)
            st.pyplot(fig)

        col4,col5, colz=st.columns(3)
        with col4:
        # Density Plot
            st.subheader("Density Plot")
            selected_column_density = st.selectbox("Select a column for the density plot", df.columns)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.kdeplot(data=df, x=selected_column_density, fill=True, ax=ax)
            st.pyplot(fig)
        with colz:
            st_lottie(url2)

        with col5 :
            

        # Area Plot
            st.subheader("Area Plot")
            selected_column_area = st.selectbox("Select a column for the area plot", df.columns)
            area_data = df[selected_column_area].value_counts().reset_index()
            area_data.columns = ["Value", "Count"]
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.lineplot(data=area_data, x="Value", y="Count", ax=ax)
            st.pyplot(fig)
        col8,colt=st.columns(2)
        with colt:
            st_lottie(url3)
        with col8:

        # Pie Plot
            st.subheader("Pie Plot")
            selected_column_pie = st.selectbox("Select a column for the pie plot", df.columns)
            pie_data = df[selected_column_pie].value_counts().reset_index()
            pie_data.columns = ["Value", "Count"]
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(pie_data["Count"], labels=pie_data["Value"], autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

        col6 , col7 = st.columns(2)

        with col6:

        # Stem-and-Leaf Plot
            st.subheader("Stem-and-Leaf Plot")
            selected_column_stemleaf = st.selectbox("Select a column for the stem-and-leaf plot", df.columns)
            fig, ax = plt.subplots(figsize=(8, 6))
            stemgraphic.stem_graphic(df[selected_column_stemleaf], ax=ax)
            st.pyplot(fig)
            
        with col7:

        # Quantile-Normal Plot
            st.subheader("Quantile-Normal Plot")
            selected_column_qqplot = st.selectbox("Select a column for the quantile-normal plot", df.columns)
            fig, ax = plt.subplots(figsize=(8, 6))
            stats.probplot(df[selected_column_qqplot], dist="norm", plot=ax)
            st.pyplot(fig)

        # Bubble Chart
        st.subheader("Bubble Chart")
        selected_column_bubble_x = st.selectbox("Select a column for the x-axis", df.columns)
        selected_column_bubble_y = st.selectbox("Select a column for the y-axis", df.columns)
        selected_column_bubble_size = st.selectbox("Select a column for the bubble size", df.columns)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df[selected_column_bubble_x], df[selected_column_bubble_y], s=df[selected_column_bubble_size], alpha=0.5)
        ax.set_xlabel(selected_column_bubble_x)
        ax.set_ylabel(selected_column_bubble_y)
        st.pyplot(fig)

        # PivotTables and PivotCharts
        st.subheader("PivotTables and PivotCharts")
        pivot_column = st.selectbox("Select a column for the pivot table", df.columns)
        pivot_index = st.selectbox("Select an index column for the pivot table", df.columns)
        pivot_values = st.selectbox("Select a values column for the pivot table", df.columns)
        pivot_table = df.pivot_table(values=pivot_values, index=pivot_index, columns=pivot_column, aggfunc="mean")
        st.dataframe(pivot_table)

        # Add more user-friendly visualizations and insights as desired

except Exception as e:
    st.error("An error occurred: {} : Try another column for continue".format(str(e)))
