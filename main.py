import pandas as pd
import numpy as np

def get_random_data_points(file_path):
    try:
        # Load the CSV file and manually set the column names
        data = pd.read_csv(file_path, header=None, names=["Stock-ID", "Date", "Stock Price"])
        print(f"Loaded data successfully.")
        
        # Print the corrected column names
        print(f"Column names in the file: {data.columns}")
        
        # Ensure the file has at least 30 rows
        if len(data) < 30:
            print(f"Error: File has less than 30 rows.")
            return pd.DataFrame()
        
        # Select a random starting point (cannot be from the last 29 points)
        random_start = np.random.randint(0, len(data) - 30)
        data_points = data.iloc[random_start:random_start + 30]
        print(f"Selected 30 random data points:\n{data_points.head()}")
        
        return data_points
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return pd.DataFrame()

def find_outliers(data):
    prices = data['Stock Price']
    mean = np.mean(prices)
    std_dev = np.std(prices)
    threshold = 2 * std_dev

    print(f"Mean: {mean}, Standard Deviation: {std_dev}, Threshold: {threshold}")
    
    # Find outliers
    outliers = data[(prices > mean + threshold) | (prices < mean - threshold)]
    if not outliers.empty:
        outliers['Mean'] = mean
        outliers['Price-Mean'] = outliers['Stock Price'] - mean
        outliers['% Deviation'] = (outliers['Price-Mean'] / threshold) * 100

    return outliers


def process_stock_data(file_path, output_file):
    print(f"Processing file: {file_path}")
    
    # Get 30 random consecutive data points
    data_points = get_random_data_points(file_path)
    if data_points.empty:
        print("No data points to process.")
        return

    # Find outliers in the selected data points
    outliers = find_outliers(data_points)
    print(f"Outliers found:\n{outliers}")
    
    # Save the outliers to a CSV file if any are found
    if not outliers.empty:
        outliers.to_csv(output_file, index=False)
        print(f"Outliers saved to {output_file}")
    else:
        print("No outliers found.")

if __name__ == "__main__":
    # File paths
    file_path = '/Users/ridhichhablani/Documents/lseg/LSE/FLTR LSE.csv'  # Replace with actual path
    output_file = 'outliers_FLTR_LSE.csv'  # Output file for saving outliers
    
    # Process the stock data
    process_stock_data(file_path, output_file)
