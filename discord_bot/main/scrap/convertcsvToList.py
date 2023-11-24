import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('tfidf_data2.csv', header=None)

# Define a function to parse and convert a cell value to a list of floats
def parse_and_convert(cell):
    if isinstance(cell, str):
        return [float(x) for x in cell.split(',')]
    elif isinstance(cell, float):
        return [cell]
    else:
        return []

# Apply the function to each cell in the DataFrame
tfidf_values_df = df.iloc[1:, 1:].applymap(parse_and_convert)

# Convert the DataFrame to a list of lists
tfidf_values = tfidf_values_df.values.tolist()

# Print the result
print(tfidf_values)
