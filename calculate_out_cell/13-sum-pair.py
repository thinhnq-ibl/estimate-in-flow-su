import pandas as pd

# Load the dataset
# Replace 'your_data.csv' with the actual filename
df = pd.read_csv('./all_flow_cell.csv')

# Group by destination coordinates and sum the COUNT column
aggregated_df = df.groupby(['origin_cell','destination_cell'], as_index=False)['in_amount'].sum()

# Sort the results by count in descending order
aggregated_df = aggregated_df.sort_values(by='origin_cell', ascending=True)

# Display the result
print(aggregated_df.head())

# Save the aggregated data to a new CSV file
aggregated_df.to_csv('all_flow_cell.csv', index=False)