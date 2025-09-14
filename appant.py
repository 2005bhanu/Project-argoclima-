import pandas as pd

# Step 1: Load the Excel files
# Explicitly specify engine='xlrd' for .xls files
df_capsicum = pd.read_excel("Capsicum.xlsx")
df_carrot = pd.read_excel("carrot.xlsx") # .xlsx files usually don't need engine specified
df_potato = pd.read_excel("potato.xlsx")

# Step 2: Add a column to identify the vegetable
df_capsicum["Vegetable"] = "Capsicum"
df_carrot["Vegetable"] = "Carrot"
df_potato["Vegetable"] = "Potato"

# Step 3: Combine the three DataFrames
combined_df = pd.concat([df_capsicum, df_carrot, df_potato], ignore_index=True)

# Step 4: Save the result to a new Excel file
combined_df.to_excel("Combined_Vegetable_Data.xlsx", index=False)

print("✅ Files merged successfully into Combined_Vegetable_Data.xlsx")