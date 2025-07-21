import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from potentiopipe import (
    peak_detection_proc,
    plot_potentiostat_proc,
    ParametersPeakDetection,
)


# Peak Detection
half_width_min = 0.05  # Volt
width_max = 0.15  # Volt
derivation_width = 0.05  # Volt
derivation_sensitivity = 0.0000001  # Ampere/Volt   0.0000003 => only one peak

# Default values of the Named tuple of the parameters
parameters_peak_detection = ParametersPeakDetection(
    half_width_min,
    width_max,
    derivation_width,
    derivation_sensitivity,
)


def example_detection():
    name_example = "example_detection"
    folder_in = "data"
    folder_out = os.path.join("results", name_example)
    if not os.path.isdir(folder_out):
        os.makedirs(folder_out)

    df_raw = pd.DataFrame()

    if not os.path.isdir(folder_in):
        print("Input folder does not exist")
        sys.exit(1)
    else:
        list_files = os.listdir(folder_in)

    for file in list_files:
        if "proc" in file:
            file_path = os.path.join(folder_in, file)
            df_proc = pd.read_csv(file_path, header=0, na_values="NAN")

            df_peak = peak_detection_proc(df_proc, parameters_peak_detection)

            path_out_peak = os.path.join(folder_out, "peak_" + file)

            # Save the processed Data
            df_peak.to_csv(path_out_peak, index=False)

            # Plotting the results
            plot_potentiostat_proc(
                df_raw,
                df_proc,
                df_peak,
                mode="Both",
                name=name_example,
                path_folder_out=folder_out,
            )

            plt.show()


if __name__ == "__main__":
    example_detection()
