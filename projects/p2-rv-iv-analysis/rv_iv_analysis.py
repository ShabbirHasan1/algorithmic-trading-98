import pandas as pd
import numpy as np
import os
from datetime import datetime

# Configuration
FOLDER_PATH = "data/storage/processed/equity/zerodha/2015/day"
OUTPUT_FOLDER = "backtestresults/volatility"
FILE_LIMIT = 2
START_DAY = "Friday"
END_DAY = "Thursday"

# Create output folder and unique filename
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(OUTPUT_FOLDER, f"volatility_analysis_{timestamp}.txt")
results_text = []

# Function to compute absolute change percentage for all startday-to-endday periods
def get_weekly_abs_changes(df, start_day, end_day):
    # Calculate expected days between start and end day
    days_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    start_num = days_map[start_day]
    end_num = days_map[end_day]
    max_days = (end_num - start_num) % 7 if end_num != start_num else 7
    df["Date"] = pd.to_datetime(df["Date"])
    df["Day"] = df["Date"].dt.day_name()

    start_days = df[df["Day"] == start_day].reset_index()
    results = []
    
    for i, row in start_days.iterrows():
        if row["Close"] == 0:
            continue
            
        start_date = row["Date"]
        end_day_data = df[(df["Date"] > start_date) & (df["Day"] == end_day)]
        
        if not end_day_data.empty:
            potential_end_date = end_day_data.iloc[0]["Date"]
            days_diff = (potential_end_date - start_date).days
            
            if days_diff <= max_days:
                end_date = potential_end_date
                end_close = end_day_data.iloc[0]["Close"]
            else:
                # Find the date exactly max_days after start_date
                target_date = start_date + pd.Timedelta(days=max_days)
                available_dates = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
                if not available_dates.empty:
                    end_date = available_dates["Date"].max()
                    end_close = df[df["Date"] == end_date]["Close"].iloc[0]
                else:
                    continue
            
            abs_change_pct = round(abs((end_close - row["Close"]) / row["Close"]) * 100, 2)

            period_df = df[(df["Date"] > start_date) & (df["Date"] <= end_date)]

            peak_high = period_df["High"].max()
            peak_low = period_df["Low"].min()
            peak_high_change = round(abs((peak_high - row["Close"]) / row["Close"]) * 100, 2)
            peak_low_change = round(abs((peak_low - row["Close"]) / row["Close"]) * 100, 2)
            
            max_peak_change = max(peak_high_change, peak_low_change)

            results.append((start_date, abs_change_pct, max_peak_change))
            
            # Add OHLCV data to results_text
            # days_between = (end_date - start_date).days
            # results_text.append(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({days_between} days)")
            # results_text.append("\nOHLCV Data:")
            # results_text.append(f"{'Date':<12} {'Open':<10} {'High':<10} {'Low':<10} {'Close':<10} {'Volume':<15}")
            # results_text.append("-" * 75)
            
            # period_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
            # for _, period_row in period_df.iterrows():
            #     date_str = period_row['Date'].strftime('%Y-%m-%d')
            #     results_text.append(f"{date_str:<12} {period_row['Open']:<10} {period_row['High']:<10} {period_row['Low']:<10} {period_row['Close']:<10} {period_row['Volume']:<15}")
            

    return results

results_text.append(f"Start day\t-\t{START_DAY}")
results_text.append(f"End day\t\t-\t{END_DAY}")

# Process all CSV files in the folder
for file in os.listdir(FOLDER_PATH)[:FILE_LIMIT]:
    if file.endswith(".csv"):
        file_path = os.path.join(FOLDER_PATH, file)
        print(f"Processing file: {file}")
        results_text.append(f"\nAnalysis for: {file[:-4]}\n")

        df = pd.read_csv(file_path)

        if "Date" not in df.columns:
            print(f"Skipping {file} (No 'Date' column found)")
            continue

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
        df = df.dropna(subset=["Date"])

        for col in ["Close", "High", "Low"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Close", "High", "Low"])
        df.sort_values("Date", ascending=True, inplace=True)

        weekly_changes = get_weekly_abs_changes(df, START_DAY, END_DAY)

        if not weekly_changes:
            print(f"No {START_DAY}-to-{END_DAY} data found in {file}")
            continue

        avg_abs_change_pct = np.mean([change for _, change, _ in weekly_changes])
        avg_max_peak_change = np.mean([max_peak for _, _, max_peak in weekly_changes])
        min_max_peak_change = min(max_peak for _, _, max_peak in weekly_changes)


        results_text.extend([
            f"Average Absolute Change Percentage: {avg_abs_change_pct:.2f}%",
            f"Average Max Peak Change Percentage: {avg_max_peak_change:.2f}%\n",
            f"Minimum Max Peak Change: {min_max_peak_change:.2f}% (Important Factor)"
        ])

        max_peak_values = sorted([max_peak for _, _, max_peak in weekly_changes], reverse=True)
        num_entries = len(max_peak_values)
        percentile_size = max(1, num_entries // 20)

        percentile_averages = {}
        for i in range(20):
            start_idx = i * percentile_size
            end_idx = min((i + 1) * percentile_size, num_entries)
            percentile_avg = np.mean(max_peak_values[start_idx:end_idx])
            percentile_averages[f"{i * 5}-{(i + 1) * 5}%"] = round(percentile_avg, 2)

        # Percentile analysis for absolute changes
        abs_change_values = [change for _, change, _ in weekly_changes]
        abs_change_values.sort(reverse=True)
        
        abs_percentile_averages = {}
        for i in range(20):
            start_idx = i * percentile_size
            end_idx = min((i + 1) * percentile_size, num_entries)
            percentile_avg = np.mean(abs_change_values[start_idx:end_idx])
            abs_percentile_averages[f"{i * 5}-{(i + 1) * 5}%"] = round(percentile_avg, 2)

        results_text.append("\nPercentile Analysis:\n")
        results_text.append(f"{'Percentile':<12} {'Abs Change':<12} {'Max Peak Change':<15}")
        results_text.append("-" * 40)

        for percentile in abs_percentile_averages.keys():
            abs_avg = abs_percentile_averages[percentile]
            peak_avg = percentile_averages[percentile]
            line = f"{percentile:<12} {abs_avg:.2f}%{'':<8} {peak_avg:.2f}%"
            results_text.append(line)

        yearly_changes = {}
        yearly_peak_changes = {}

        for start, change, max_peak in weekly_changes:
            year = start.year

            if year not in yearly_changes:
                yearly_changes[year] = []
                yearly_peak_changes[year] = []

            yearly_changes[year].append(change)
            yearly_peak_changes[year].append(max_peak)

        avg_yearly_changes = {year: round(np.mean(changes), 2) for year, changes in yearly_changes.items()}
        avg_yearly_peak_changes = {year: round(np.mean(peaks), 2) for year, peaks in yearly_peak_changes.items()}

        results_text.append(f"\nAverage {START_DAY}-to-{END_DAY} Changes Per Year:\n")
        results_text.append(f"{'Year':<6} {'Abs Change':<12} {'Max Peak Change':<15}")
        results_text.append("-" * 35)
        
        for year in sorted(avg_yearly_changes.keys()):
            year_line = f"{year:<6} {avg_yearly_changes[year]:.2f}%{'':<8} {avg_yearly_peak_changes[year]:.2f}%"
            results_text.append(year_line)

        # Monthly analysis
        monthly_changes = {}
        monthly_peak_changes = {}
        for start, change, max_peak in weekly_changes:
            year = start.year
            month = start.strftime("%b")
            monthly_changes[(year, month)] = change
            monthly_peak_changes[(year, month)] = max_peak

        if monthly_changes:
            table = pd.DataFrame.from_dict(monthly_changes, orient='index', columns=["Abs Change Pct"])
            table.index = pd.MultiIndex.from_tuples(table.index, names=["Year", "Month"])
            table = table.unstack(level=1)["Abs Change Pct"]
            
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            table = table.reindex(columns=month_order)
            table.loc["Average"] = round(table.mean(), 2)
            
            results_text.append("\nMonthly Absolute Change Percentages Table:\n")
            results_text.append(str(table.round(2)))
            
            # Monthly max peak changes table
            peak_table = pd.DataFrame.from_dict(monthly_peak_changes, orient='index', columns=["Max Peak Change Pct"])
            peak_table.index = pd.MultiIndex.from_tuples(peak_table.index, names=["Year", "Month"])
            peak_table = peak_table.unstack(level=1)["Max Peak Change Pct"]
            peak_table = peak_table.reindex(columns=month_order)
            peak_table.loc["Average"] = round(peak_table.mean(), 2)
            
            results_text.append("\nMonthly Max Peak Change Percentages Table:\n")
            results_text.append(str(peak_table.round(2)))

# Save results to file
with open(output_file, 'w') as f:
    f.write('\n'.join(results_text))
print(f"\nResults saved to: {output_file}")