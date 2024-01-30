import mne
import numpy as np
import pandas as pd

def plot_description_histogram(csv_file_path, output_file_name):
    # Read the .csv file using pandas
    df = pd.read_csv(csv_file_path)
    
    # Check if the 'description' column exists
    if 'description' not in df.columns:
        print("The file does not contain a 'description' column.")
        return
    
    # Extract unique values from the 'description' column
    unique_descriptions = df['description'].dropna().unique()
    
    # Count the occurrences of each unique description
    description_counts = df['description'].value_counts().loc[unique_descriptions]
    
    # Plot a histogram of the unique description counts
    plt.figure(figsize=(10, 6))
    description_counts.plot(kind='bar')
    plt.title('Histogram of Unique Descriptions')
    plt.xlabel('Description')
    plt.ylabel('Frequency')
    
    # Save the histogram as a .png file
    plt.savefig(f'{output_file_name}.png')
    print(f"Histogram saved as '{output_file_name}.png'")

# Example usage:
# Replace 'your_csv_file_path.csv' with the actual path to your .csv file
# and 'output_histogram' with your desired output file name (without extension)
# plot_description_histogram('your_csv_file_path.csv', 'output_histogram')

def convert_edf_to_csv(edf_path, csv_path):
    # Load the EDF file
    raw = mne.io.read_raw_edf(edf_path, preload=True)

    # Get the annotations
    annotations = raw.annotations
    annotations_df = pd.DataFrame({
        'onset': annotations.onset,
        'duration': annotations.duration,
        'description': annotations.description
    })

    # Get the signals
    signals = raw.get_data().T  # Transpose the data for correct shape
    signals_df = pd.DataFrame(signals, columns=raw.ch_names)

    # Create a time column based on the sample rate
    sample_rate = raw.info['sfreq']
    num_samples = raw.n_times
    time_column = pd.Series(range(num_samples)) / sample_rate

    # Set the time column as the index of signals_df
    signals_df = signals_df.set_index(time_column, drop=False)

    # Align annotations with signals based on the time column
    merged_df = pd.merge_asof(signals_df, annotations_df, left_index=True, right_on='onset', direction='backward')

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(csv_path, index=True)

# Usage example:
#edf_file_path = "/Users/sumitpandey/Downloads/EEG-consciousness/EDF files/01CX-EDF+.edf"
#csv_file_path = "/Users/sumitpandey/Downloads/EEG-consciousness/input_data/01CX-EDF+.csv"
#convert_edf_to_csv(edf_file_path, csv_file_path)


def print_csv_columns(file_path):
    # Read the .csv file using pandas
    df = pd.read_csv(file_path)
    
    # Get the column names from the DataFrame
    columns = df.columns
    
    # Print the column names
    print("Columns in the CSV file:")
    for column in columns:
        print(column.values())

# Example usage
# Replace 'your_file_path.csv' with the actual path to your .csv file
# print_csv_columns('your_file_path.csv')
        
