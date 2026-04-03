# E-Commerce Sales Analysis
# Dataset: Online Sales Dataset
# Tools: Python, Pandas, Matplotlib, Seaborn

# Block 1: Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
print("Saving files to:", os.getcwd())
# Block 2: Load Dataset
df = pd.read_csv("sales_data.csv")
print("Column Names:", df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))

# Block 3: Understand the Data
print("\nShape (rows, columns):", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nBasic Statistics:\n", df.describe())

# Block 4: Data Cleaning
df["Date"]       = pd.to_datetime(df["Date"])
df["Month"]      = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%b")
df["Year"]       = df["Date"].dt.year

before = df.shape[0]
df.drop_duplicates(inplace=True)
after = df.shape[0]
print(f"\nDuplicates removed: {before - after}")

df.dropna(subset=["Total Revenue", "Product Category", "Region"], inplace=True)
print(f"Clean dataset ready: {df.shape[0]} rows, {df.shape[1]} columns ✅")

# Block 5: Business Questions — EDA
category_revenue = df.groupby("Product Category")["Total Revenue"].sum()\
                     .sort_values(ascending=False).reset_index()
category_revenue.columns = ["Category", "Total Revenue"]
print("\n📦 Revenue by Category:")
print(category_revenue)

monthly_revenue = df.groupby(["Year", "Month", "Month_Name"])["Total Revenue"]\
                    .sum().reset_index()
monthly_revenue = monthly_revenue.sort_values(["Year", "Month"])
print("\n📅 Monthly Revenue Trend:")
print(monthly_revenue[["Month_Name", "Total Revenue"]])

region_revenue = df.groupby("Region")["Total Revenue"].sum()\
                   .sort_values(ascending=False).reset_index()
print("\n🌍 Revenue by Region:")
print(region_revenue)

top_products = df.groupby("Product Name")["Total Revenue"].sum()\
                 .nlargest(5).reset_index()
print("\n🏆 Top 5 Products:")
print(top_products)

payment_counts = df["Payment Method"].value_counts().reset_index()
payment_counts.columns = ["Payment Method", "Count"]
print("\n💳 Payment Method Usage:")
print(payment_counts)

total_revenue    = df["Total Revenue"].sum()
total_orders     = df["Transaction ID"].nunique()
avg_order_value  = df["Total Revenue"].mean()
total_units_sold = df["Units Sold"].sum()

print("\n📊 KEY KPIs:")
print(f"  Total Revenue    : ${total_revenue:,.2f}")
print(f"  Total Orders     : {total_orders:,}")
print(f"  Avg Order Value  : ${avg_order_value:,.2f}")
print(f"  Total Units Sold : {total_units_sold:,}")

# Block 6: Visualizations
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle("E-Commerce Sales Performance Dashboard",
             fontsize=18, fontweight="bold", y=1.01)

# Chart 1: Revenue by Category
axes[0, 0].bar(
    category_revenue["Category"],
    category_revenue["Total Revenue"],
    color=sns.color_palette("Blues_d", len(category_revenue))
)
axes[0, 0].set_title("Revenue by Product Category", fontsize=13, fontweight="bold")
axes[0, 0].set_xlabel("Category")
axes[0, 0].set_ylabel("Total Revenue ($)")
axes[0, 0].tick_params(axis="x", rotation=30)
for i, val in enumerate(category_revenue["Total Revenue"]):
    axes[0, 0].text(i, val + 500, f"${val:,.0f}", ha="center", fontsize=8)

# Chart 2: Monthly Revenue Trend
axes[0, 1].plot(
    monthly_revenue["Month_Name"],
    monthly_revenue["Total Revenue"],
    marker="o", color="darkorange", linewidth=2.5, markersize=7
)
axes[0, 1].set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold")
axes[0, 1].set_xlabel("Month")
axes[0, 1].set_ylabel("Total Revenue ($)")
axes[0, 1].tick_params(axis="x", rotation=30)
axes[0, 1].fill_between(
    monthly_revenue["Month_Name"],
    monthly_revenue["Total Revenue"],
    alpha=0.1, color="darkorange"
)

# Chart 3: Revenue by Region
axes[1, 0].barh(
    region_revenue["Region"],
    region_revenue["Total Revenue"],
    color=sns.color_palette("Greens_d", len(region_revenue))
)
axes[1, 0].set_title("Revenue by Region", fontsize=13, fontweight="bold")
axes[1, 0].set_xlabel("Total Revenue ($)")
axes[1, 0].set_ylabel("Region")
for i, val in enumerate(region_revenue["Total Revenue"]):
    axes[1, 0].text(val + 200, i, f"${val:,.0f}", va="center", fontsize=8)

# Chart 4: Payment Method Pie Chart
axes[1, 1].pie(
    payment_counts["Count"],
    labels=payment_counts["Payment Method"],
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("Set2")
)
axes[1, 1].set_title("Payment Method Distribution", fontsize=13, fontweight="bold")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
print("\n✅ Dashboard saved as sales_dashboard.png")
plt.close()

# Block 7: Export to Excel
with pd.ExcelWriter("sales_summary_report.xlsx", engine="openpyxl") as writer:
    kpi_df = pd.DataFrame({
        "KPI"  : ["Total Revenue", "Total Orders",
                  "Avg Order Value", "Total Units Sold"],
        "Value": [f"${total_revenue:,.2f}", f"{total_orders:,}",
                  f"${avg_order_value:,.2f}", f"{total_units_sold:,}"]
    })
    kpi_df.to_excel(writer, sheet_name="KPI Summary",   index=False)
    category_revenue.to_excel(writer, sheet_name="By Category",   index=False)
    monthly_revenue[["Month_Name", "Total Revenue"]]\
        .to_excel(writer, sheet_name="Monthly Trend",  index=False)
    region_revenue.to_excel(writer, sheet_name="By Region",     index=False)
    top_products.to_excel(writer, sheet_name="Top Products",   index=False)

print("✅ Excel report saved as sales_summary_report.xlsx")
print("\n🎉 Analysis Complete! Check your project folder.")