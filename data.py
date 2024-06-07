import pandas as pd

def to_int(value):
    try:
        if value > 1:
            return int(value)
        return round(value,2)
    except (ValueError, TypeError):
        return value

# Path to the CSV file
file_path = 'plot-data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Apply the conversion to all cells
df = df.map(to_int)


# Sort the DataFrame by the 'x' column in ascending order
df = df.sort_values(by='x')

# Write the updated DataFrame back to the original CSV file
df.to_csv("new-data.csv", index=False)

print(f"Updated the CSV file at {file_path}")