import pandas as pd
import os

# Extract function is already implemented for you 
def extract(store_data, extra_data):
    extra_df = pd.read_parquet(extra_data)
    merged_df = store_data.merge(extra_df, on = "index")
    return merged_df

# Call the extract() function and store it as the "merged_df" variable
grocery_sales = pd.read_csv("grocery_sales.csv")
merged_df = extract(grocery_sales, "extra_data.parquet")

# Create the transform() function with one parameter: "raw_data"
def transform(raw_data):
  # Write your code here
    raw_data.fillna(raw_data.select_dtypes(include='number').mean(), inplace=True)
    raw_data["Month"] = pd.to_datetime(raw_data["Date"]).dt.month
    raw_data = raw_data[raw_data["Weekly_Sales"] > 10000]
    raw_data = raw_data[["Store_ID", "Month", "Dept", "IsHoliday", 
                          "Weekly_Sales", "CPI", "Unemployment"]]
    return raw_data

clean_data = transform(merged_df)

def avg_weekly_sales_per_month(clean_data):
    # Write your code here
    result = (clean_data[["Month", "Weekly_Sales"]] 
              .groupby("Month")                      
              .agg(Avg_Sales=("Weekly_Sales", "mean")) 
              .reset_index()                         
              .round(2))                            
    return result

agg_data = avg_weekly_sales_per_month(clean_data)

def load(full_data, full_data_file_path, agg_data, agg_data_file_path):
    # Write your code here
    full_data.to_csv(full_data_file_path, index=False) 
    agg_data.to_csv(agg_data_file_path, index=False)   


load(clean_data, "clean_data.csv", agg_data, "agg_data.csv")

def validation(file_path):
    # Write your code here
    return os.path.exists(file_path) 

validation("clean_data.csv")  
validation("agg_data.csv")  