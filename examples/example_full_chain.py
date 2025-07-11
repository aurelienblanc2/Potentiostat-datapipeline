import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from potentiopipe import (
    process_raw,
    peak_detection_proc,
    plot_potentiostat_proc,
    ParametersPeakDetection,
)


# Peak Detection
half_width_min = 0.1  # Volt
width_max = 0.3  # Volt
derivation_width = 0.05  # Volt
derivation_sensitivity = 0.00000002  # Ampere/Volt

# Default values of the Named tuple of the parameters
parameters_peak_detection = ParametersPeakDetection(
    half_width_min,
    width_max,
    derivation_width,
    derivation_sensitivity,
)


def example_full_chain():
    folder_in = "data"
    folder_out = "results"
    columns_raw_file = ["Time", "Voltage", "Current", "Cycle", "Dummy", "Reference"]

    if not os.path.isdir(folder_in):
        print("Input folder does not exist")
        sys.exit(1)
    else:
        list_files = os.listdir(folder_in)

    for file in list_files:
        file_path = os.path.join(folder_in, file)
        df_raw = pd.read_csv(
            file_path, header=None, na_values="NAN", names=columns_raw_file
        )

        df_proc = process_raw(df_raw)
        df_peak = peak_detection_proc(df_proc, parameters_peak_detection)

        # Path to the processed Data
        folder_out_example = os.path.join(folder_out, "example_full_chain")
        if not os.path.isdir(folder_out_example):
            os.makedirs(folder_out_example)
        path_out_proc = os.path.join(folder_out_example, "proc_" + file)
        path_out_peak = os.path.join(folder_out_example, "peak_" + file)

        # Save the processed Data
        df_proc.to_csv(path_out_proc, index=False)
        df_peak.to_csv(path_out_peak, index=False)

        # Plotting the results
        plot_potentiostat_proc(
            df_raw,
            df_proc,
            df_peak,
            mode="Both",
            name="example_full_chain",
            path_folder_out=folder_out_example,
        )

        plt.show()


if __name__ == "__main__":
    example_full_chain()
