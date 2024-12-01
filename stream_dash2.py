import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Dataset
@st.cache_data
def load_data(file_path=None):
    if file_path:
        return pd.read_csv(file_path)
    return pd.read_csv(r"D:\Ddrive\DataSet\OfficeSupplies.csv")

# 2. App Title
st.title("📊 Office Supplies Sales Dashboard")

# 3. Sidebar for Filters
st.sidebar.header("Filter Options")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your CSV file:", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data()

# Convert OrderDate to datetime
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# Multiselect for Regions
regions = st.sidebar.multiselect(
    "Select Region(s):",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Multiselect for Items
items = st.sidebar.multiselect(
    "Select Item(s):",
    options=df["Item"].unique(),
    default=df["Item"].unique()
)

# Date Range Picker
date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=(df["OrderDate"].min(), df["OrderDate"].max())
)

# Filter the DataFrame based on sidebar inputs
filtered_data = df[
    (df["Region"].isin(regions)) &
    (df["Item"].isin(items)) &
    (df["OrderDate"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# 4. Display Filtered Data
st.write(f"### Filtered Data (Showing {filtered_data.shape[0]} rows):")
st.dataframe(filtered_data)

# 5. Summary Statistics
st.subheader("Summary Statistics")
st.write(filtered_data.describe())

# 6. Visualizations

# 6.1 Bar Chart: Total Units Sold by Region
st.subheader("Total Units Sold by Region")
units_by_region = filtered_data.groupby("Region")["Units"].sum().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=units_by_region, x="Region", y="Units", ax=ax, palette="viridis")
ax.set_title("Units Sold by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Total Units Sold")
st.pyplot(fig)

# 6.2 Line Chart: Sales Trends Over Time
st.subheader("Sales Trends Over Time")
sales_over_time = filtered_data.groupby(filtered_data["OrderDate"].dt.to_period("M"))["Units"].sum()

fig, ax = plt.subplots()
sales_over_time.plot(kind="line", ax=ax, marker='o', color="blue")
ax.set_title("Units Sold Over Time")
ax.set_xlabel("Order Month")
ax.set_ylabel("Total Units Sold")
st.pyplot(fig)

# 6.3 Pie Chart: Distribution of Items Sold
st.subheader("Distribution of Items Sold")
item_distribution = filtered_data["Item"].value_counts()

fig, ax = plt.subplots()
item_distribution.plot(kind="pie", autopct='%1.1f%%', ax=ax, startangle=90, colors=sns.color_palette("pastel"))
ax.set_ylabel("")  # Hides the y-axis label
ax.set_title("Distribution of Items Sold")
st.pyplot(fig)

# 6.4 Correlation Heatmap
st.subheader("Correlation Heatmap")
numerical_cols = ["Units", "Unit Price"]
correlation = filtered_data[numerical_cols].corr()

fig, ax = plt.subplots()
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Between Numerical Variables")
st.pyplot(fig)

# 7. Download Button for Filtered Data
st.subheader("Download Filtered Data")
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_office_supplies.csv",
    mime="text/csv",
)

# 8. Conclusion
st.write("### Thank you for exploring the Office Supplies Sales Dashboard! 🚀")
