import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*70)
print("MONTGOMERY COUNTY LIQUOR SALES ANALYSIS")
print("Business Intelligence Report")
print("="*70)

df = pd.read_csv('Warehouse_and_Retail_Sales.csv')

print(f"\nDataset loaded: {len(df):,} records")
print(f"Columns: {list(df.columns)}")
print(f"Date range: {df['YEAR'].min()} to {df['YEAR'].max()}")

print("\n" + "="*70)
print("1. DATA QUALITY ASSESSMENT")
print("="*70)

print(f"\nMissing Values:")
missing = df.isnull().sum()
for col, count in missing[missing > 0].items():
    pct = (count / len(df)) * 100
    print(f"  {col:30s}: {count:8,} ({pct:5.2f}%)")

print(f"\nData Types:")
print(df.dtypes)

print(f"\nBasic Statistics:")
print(df.describe())

df['TOTAL SALES'] = df['RETAIL SALES'] + df['WAREHOUSE SALES']
df['Date'] = pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-01')

print("\n" + "="*70)
print("2. EXECUTIVE SUMMARY - KEY METRICS")
print("="*70)

total_retail_sales = df['RETAIL SALES'].sum()
total_warehouse_sales = df['WAREHOUSE SALES'].sum()
total_sales = df['TOTAL SALES'].sum()
total_transfers = df['RETAIL TRANSFERS'].sum()
unique_items = df['ITEM DESCRIPTION'].nunique()
unique_suppliers = df['SUPPLIER'].nunique()
unique_item_types = df['ITEM TYPE'].nunique()

print(f"\n  Total Retail Sales:      {total_retail_sales:,.0f} units")
print(f"  Total Warehouse Sales:   {total_warehouse_sales:,.0f} units")
print(f"  Total Sales Volume:      {total_sales:,.0f} units")
print(f"  Total Retail Transfers:  {total_transfers:,.0f} units")
print(f"  Unique Products:         {unique_items:,}")
print(f"  Unique Suppliers:        {unique_suppliers:,}")
print(f"  Product Types:           {unique_item_types:,}")

retail_pct = (total_retail_sales / total_sales) * 100
warehouse_pct = (total_warehouse_sales / total_sales) * 100
print(f"\n  Retail Channel:          {retail_pct:.1f}% of total sales")
print(f"  Warehouse Channel:       {warehouse_pct:.1f}% of total sales")

print("\n" + "="*70)
print("3. ANNUAL SALES TREND ANALYSIS")
print("="*70)

yearly_sales = df.groupby('YEAR').agg({
    'RETAIL SALES': 'sum',
    'WAREHOUSE SALES': 'sum',
    'TOTAL SALES': 'sum',
    'RETAIL TRANSFERS': 'sum'
})

print("\nYearly Performance:")
print(yearly_sales)

yoy_growth = yearly_sales['TOTAL SALES'].pct_change() * 100
print(f"\nYear-over-Year Sales Growth:")
for year, growth in yoy_growth.items():
    if not np.isnan(growth):
        arrow = "↑" if growth > 0 else "↓"
        print(f"  {year}: {growth:+.2f}% {arrow}")

print("\n" + "="*70)
print("4. TOP PERFORMERS ANALYSIS")
print("="*70)

print("\nTop 15 Products by Total Sales Volume:")
top_products = df.groupby('ITEM DESCRIPTION')['TOTAL SALES'].sum().sort_values(ascending=False).head(15)
for i, (product, sales) in enumerate(top_products.items(), 1):
    pct = (sales / total_sales) * 100
    print(f"  {i:2d}. {product[:55]:55s} {sales:>12,.0f} ({pct:5.2f}%)")

print("\nTop 10 Suppliers by Sales Volume:")
top_suppliers = df.groupby('SUPPLIER')['TOTAL SALES'].sum().sort_values(ascending=False).head(10)
for i, (supplier, sales) in enumerate(top_suppliers.items(), 1):
    pct = (sales / total_sales) * 100
    print(f"  {i:2d}. {supplier[:45]:45s} {sales:>12,.0f} ({pct:5.2f}%)")

print("\n" + "="*70)
print("5. PRODUCT TYPE ANALYSIS")
print("="*70)

type_performance = df.groupby('ITEM TYPE').agg({
    'RETAIL SALES': 'sum',
    'WAREHOUSE SALES': 'sum',
    'TOTAL SALES': 'sum'
}).sort_values('TOTAL SALES', ascending=False)

print("\nSales by Product Type:")
for item_type, row in type_performance.iterrows():
    pct = (row['TOTAL SALES'] / total_sales) * 100
    print(f"  {item_type[:35]:35s} {row['TOTAL SALES']:>12,.0f} ({pct:5.2f}%)")

print("\n" + "="*70)
print("6. CHANNEL PERFORMANCE (Retail vs Warehouse)")
print("="*70)

print(f"\nRetail Sales:     {total_retail_sales:>15,.0f} units ({retail_pct:5.1f}%)")
print(f"Warehouse Sales:  {total_warehouse_sales:>15,.0f} units ({warehouse_pct:5.1f}%)")
print(f"Retail Transfers: {total_transfers:>15,.0f} units")

channel_by_year = df.groupby('YEAR')[['RETAIL SALES', 'WAREHOUSE SALES']].sum()
print("\nChannel Performance by Year:")
print(channel_by_year)

print("\n" + "="*70)
print("7. SEASONALITY ANALYSIS")
print("="*70)

monthly_sales = df.groupby('MONTH')['TOTAL SALES'].sum().sort_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

print("\nTotal Sales by Month (All Years Combined):")
for month, sales in monthly_sales.items():
    pct = (sales / total_sales) * 100
    print(f"  {month_names[month-1]:3s}: {sales:>12,.0f} ({pct:5.2f}%)")

best_month = monthly_sales.idxmax()
worst_month = monthly_sales.idxmin()
print(f"\nBest Month:  {month_names[best_month-1]} ({monthly_sales[best_month]:,.0f} units)")
print(f"Worst Month: {month_names[worst_month-1]} ({monthly_sales[worst_month]:,.0f} units)")

print("\n" + "="*70)
print("8. SUPPLIER CONCENTRATION ANALYSIS")
print("="*70)

top_5_suppliers = df.groupby('SUPPLIER')['TOTAL SALES'].sum().sort_values(ascending=False).head(5)
top_5_total = top_5_suppliers.sum()
top_5_pct = (top_5_total / total_sales) * 100

print(f"\nTop 5 suppliers account for {top_5_pct:.1f}% of total sales")
print("This indicates", "HIGH" if top_5_pct > 50 else "MODERATE", "supplier concentration")

print("\n" + "="*70)
print("CREATING VISUALIZATIONS...")
print("="*70)

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])
yearly_data = df.groupby('YEAR')['TOTAL SALES'].sum() / 1_000_000
ax1.plot(yearly_data.index, yearly_data.values, marker='o', linewidth=3, markersize=10, color='steelblue')
ax1.fill_between(yearly_data.index, yearly_data.values, alpha=0.3, color='steelblue')
ax1.set_title('Annual Sales Volume Trend', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Sales Volume (Millions of Units)', fontsize=11)
ax1.grid(True, alpha=0.3)
for i, v in enumerate(yearly_data.values):
    ax1.text(yearly_data.index[i], v, f'{v:.1f}M', ha='center', va='bottom', fontsize=9)

ax2 = fig.add_subplot(gs[1, 0])
top_10_products = df.groupby('ITEM DESCRIPTION')['TOTAL SALES'].sum().sort_values(ascending=False).head(10) / 1000
ax2.barh(range(len(top_10_products)), top_10_products.values, color='coral')
ax2.set_yticks(range(len(top_10_products)))
ax2.set_yticklabels([p[:30] for p in top_10_products.index], fontsize=8)
ax2.set_xlabel('Sales Volume (Thousands)', fontsize=10)
ax2.set_title('Top 10 Products by Sales', fontsize=12, fontweight='bold')
ax2.invert_yaxis()

ax3 = fig.add_subplot(gs[1, 1])
type_sales = df.groupby('ITEM TYPE')['TOTAL SALES'].sum().sort_values(ascending=False)
type_sales_positive = type_sales[type_sales > 0].head(5)
colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']
wedges, texts, autotexts = ax3.pie(type_sales_positive.values, labels=None, autopct='%1.1f%%', 
        startangle=90, colors=colors, textprops={'fontsize': 10, 'weight': 'bold'})
ax3.legend(wedges, type_sales_positive.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
ax3.set_title('Sales by Product Type', fontsize=12, fontweight='bold')

ax4 = fig.add_subplot(gs[1, 2])
monthly_avg = df.groupby('MONTH')['TOTAL SALES'].sum() / 1000
ax4.bar(range(1, 13), monthly_avg.values, color='mediumseagreen', edgecolor='black', linewidth=0.5)
ax4.set_xticks(range(1, 13))
ax4.set_xticklabels(month_names, fontsize=9)
ax4.set_ylabel('Sales Volume (Thousands)', fontsize=10)
ax4.set_title('Monthly Sales Pattern', fontsize=12, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)

ax5 = fig.add_subplot(gs[2, 0])
top_suppliers_plot = df.groupby('SUPPLIER')['TOTAL SALES'].sum().sort_values(ascending=False).head(10) / 1000
ax5.barh(range(len(top_suppliers_plot)), top_suppliers_plot.values, color='skyblue', edgecolor='black')
ax5.set_yticks(range(len(top_suppliers_plot)))
ax5.set_yticklabels([s[:25] for s in top_suppliers_plot.index], fontsize=8)
ax5.set_xlabel('Sales Volume (Thousands)', fontsize=10)
ax5.set_title('Top 10 Suppliers by Sales', fontsize=12, fontweight='bold')
ax5.invert_yaxis()

ax6 = fig.add_subplot(gs[2, 1])
channel_data = pd.Series({
    'Retail': total_retail_sales,
    'Warehouse': total_warehouse_sales
})
ax6.pie(channel_data.values, labels=channel_data.index, autopct='%1.1f%%', 
        startangle=90, colors=['#ff9999', '#66b3ff'], textprops={'fontsize': 11})
ax6.set_title('Sales by Channel', fontsize=12, fontweight='bold')

ax7 = fig.add_subplot(gs[2, 2])
channel_trend = df.groupby('YEAR')[['RETAIL SALES', 'WAREHOUSE SALES']].sum() / 1000
ax7.plot(channel_trend.index, channel_trend['RETAIL SALES'], marker='o', label='Retail', linewidth=2)
ax7.plot(channel_trend.index, channel_trend['WAREHOUSE SALES'], marker='s', label='Warehouse', linewidth=2)
ax7.set_xlabel('Year', fontsize=10)
ax7.set_ylabel('Sales Volume (Thousands)', fontsize=10)
ax7.set_title('Channel Trends Over Time', fontsize=12, fontweight='bold')
ax7.legend()
ax7.grid(True, alpha=0.3)

plt.suptitle('Montgomery County Liquor Sales - Business Intelligence Dashboard', 
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig('liquor_sales_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Dashboard saved: liquor_sales_dashboard.png")

monthly_trend = df.groupby('Date')['TOTAL SALES'].sum()

plt.figure(figsize=(16, 6))
plt.plot(monthly_trend.index, monthly_trend.values / 1000, linewidth=2, color='darkblue', alpha=0.7)
plt.fill_between(monthly_trend.index, monthly_trend.values / 1000, alpha=0.2, color='darkblue')
plt.title('Monthly Sales Volume Trend', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Date', fontsize=11)
plt.ylabel('Sales Volume (Thousands)', fontsize=11)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('monthly_sales_trend.png', dpi=300, bbox_inches='tight')
print("✓ Trend chart saved: monthly_sales_trend.png")

summary_df = df.groupby(['YEAR', 'MONTH']).agg({
    'RETAIL SALES': 'sum',
    'WAREHOUSE SALES': 'sum',
    'TOTAL SALES': 'sum',
    'RETAIL TRANSFERS': 'sum'
}).reset_index()

summary_df.to_csv('sales_summary.csv', index=False)
print("✓ Summary data saved: sales_summary.csv")

print("\n" + "="*70)
print("BUSINESS RECOMMENDATIONS")
print("="*70)

print(f"""
1. INVENTORY OPTIMIZATION:
   → Focus procurement on top 10 products (they drive {(top_products.sum()/total_sales*100):.1f}% of sales)
   → Maintain higher stock levels for best-selling items
   → Consider discontinuing low-performing SKUs

2. SUPPLIER RELATIONSHIP MANAGEMENT:
   → Top 5 suppliers account for {top_5_pct:.1f}% of sales
   → Negotiate better terms with key suppliers
   → Develop contingency plans to reduce concentration risk

3. SEASONAL PLANNING:
   → {month_names[best_month-1]} is peak month - ensure adequate staffing and inventory
   → {month_names[worst_month-1]} is slowest - consider promotional campaigns
   → Adjust inventory levels based on monthly patterns

4. CHANNEL STRATEGY:
   → Retail accounts for {retail_pct:.1f}% of sales
   → Optimize warehouse operations for {warehouse_pct:.1f}% warehouse sales
   → Analyze profitability differences between channels

5. PRODUCT MIX OPTIMIZATION:
   → Top product type: {type_performance.index[0]}
   → Expand offerings in high-performing categories
   → Review underperforming product types for removal

6. GROWTH OPPORTUNITIES:
   → Recent year-over-year growth: {yoy_growth.iloc[-1]:.2f}%
   → Focus on products showing consistent growth
   → Explore new product categories based on market trends
""")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print("\nGenerated files:")
print("  1. liquor_sales_dashboard.png - Executive dashboard with 7 charts")
print("  2. monthly_sales_trend.png - Detailed time series analysis")
print("  3. sales_summary.csv - Monthly aggregated data for further analysis")