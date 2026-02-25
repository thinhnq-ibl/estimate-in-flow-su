import pandas as pd

# Load the dataset
# Replace 'your_data.csv' with the actual filename
df = pd.read_csv('./all_flow_cell.csv')

print(df['in_amount'].sum())