import mne
import numpy as np
import pandas as pd

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
edf_file_path = "/Users/sumitpandey/Downloads/EEG-consciousness/EDF files/01CX-EDF+.edf"
csv_file_path = "/Users/sumitpandey/Downloads/EEG-consciousness/input_data/01CX-EDF+.csv"
convert_edf_to_csv(edf_file_path, csv_file_path)
