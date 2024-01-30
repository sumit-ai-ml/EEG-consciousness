import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    print("Columns in the CSV file:", columns.values)
    

# Example usage
# Replace 'your_file_path.csv' with the actual path to your .csv file
# print_csv_columns('your_file_path.csv')
        
def filter_csv(input_file_path, output_folder='filtered_data', output_file_name='filtered_data.csv'):
    """
    Filters a CSV file to keep only specific values in the 'description' column and saves the result to a new file.

    :param input_file_path: Path to the input CSV file.
    :param output_folder: Folder where the filtered CSV will be saved. Defaults to 'filtered_data'.
    :param output_file_name: Name of the output CSV file. Defaults to 'filtered_data.csv'.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the CSV file
    df = pd.read_csv(input_file_path)

    # print the unique values 
    unique_descriptions = df['description'].unique()
    print("Unique values in 'description' column:", unique_descriptions)

    # Define the EEG columns to keep
    eeg_columns = [
        'EEG Fp1-REF', 'EEG Fp2-REF', 'EEG F3-REF', 'EEG F4-REF',
        'EEG C3-REF', 'EEG C4-REF', 'EEG P3-REF', 'EEG P4-REF', 'EEG O1-REF',
        'EEG O2-REF', 'EEG F7-REF', 'EEG F8-REF', 'EEG T7-REF', 'EEG T8-REF',
        'EEG P7-REF', 'EEG P8-REF', 'EEG T9-REF', 'EEG T10-REF', 'EEG Fz-REF',
        'EEG Cz-REF', 'EEG Pz-REF', 'EEG F10-REF', 'EEG F9-REF', 'EEG P9-REF',
        'EEG P10-REF', 'ECG EKG-REF', 'description'
    ]

    # Filter the dataframe to keep only specific values in the 'description' column and the specified EEG columns
    filtered_df = df[df['description'].isin(['Resting', 'Tiltale-X', 'Tiltale-Y'])][eeg_columns]



    # Construct the full output path
    #output_file_path = os.path.join(output_folder, output_file_name)

    # Save the filtered data to the specified output CSV file
    #filtered_df.to_csv(output_file_path, index=False)

    #print(f"Filtered CSV saved to '{output_file_path}'")

    return filtered_df
