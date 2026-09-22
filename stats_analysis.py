import pandas as pd
from scipy import stats

df = pd.read_csv(r"C:\Users\Bhargavi\Data analytics projects\Flagship Project\sales_master_export.csv")

print("=== DESCRIPTIVE STATS: SALES ===")
print(df['sales'].describe())

print("\n=== DESCRIPTIVE STATS: PROFIT ===")
print(df['profit'].describe())

print("\n=== CORRELATION: Discount vs Profit ===")
print(df['discount'].corr(df['profit']))

print("\n=== T-TEST: High Discount vs Low Discount Profit ===")
high_discount = df[df['discount'] >= 0.3]['profit']
low_discount = df[df['discount'] < 0.3]['profit']
t_stat, p_value = stats.ttest_ind(high_discount, low_discount, equal_var=False)
print("High discount mean profit:", high_discount.mean())
print("Low discount mean profit:", low_discount.mean())
print("T-statistic:", t_stat)
print("P-value:", p_value)