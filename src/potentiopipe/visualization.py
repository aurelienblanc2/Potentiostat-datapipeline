"""
Visualization of the potentiostat data

Functions:
    plot_potentiostat_raw
    plot_potentiostat_proc

Nested functions:
    _plot_ramp
    _plot_cycle
"""


###############
# - IMPORTS - #
###############

# Libraries
import os
import matplotlib.pyplot as plt
import pandas as pd


#################
# - FUNCTIONS - #
#################


def plot_potentiostat_raw(
    df_raw: pd.DataFrame,
    mode: str = "Plot",
    name: str = "Potentiostat",
    path_folder_out: str = "",
):
    """
    Description :

        Plot and/or save figures for analyzing potentiostat raw data

    Args:

        df_raw (type: pd.DataFrame) : Raw potentiostat data Dataframe
        mode (type: str, optional) : 'Display' to display the figures, 'Save' to save them at path_folder_out or 'Both'
        name (type: str, optional) : Name to use for the saved files and figure titles
        path_folder_out (type: str, optional) : Path to the folder for saving the graphs
    """

    # Checking the inputs
    #####################
    if not isinstance(df_raw, pd.DataFrame):
        raise TypeError("Input df_raw is not a DataFrame")

    # Checking that Voltage and Current are in the df_raw
    if ("Voltage" not in df_raw.columns) or ("Current" not in df_raw.columns):
        raise ValueError("df_raw does not contain 'Voltage' or 'Current'")

    # Checking mode
    if (mode != "Display") and (mode != "Save") and (mode != "Both"):
        raise ValueError("mode not recognized (Display, Save or Both)")

    if (mode == "Save") or (mode == "Both"):
        if path_folder_out == "":
            path_folder_out = os.path.join(os.getcwd(), "result")
            os.makedirs(path_folder_out, exist_ok=True)
            print(
                f"WARNING : no path_folder_out provided, figures will be saved at {path_folder_out}"
            )
        else:
            os.makedirs(path_folder_out, exist_ok=True)

    # Main
    ######
    df_raw = df_raw.dropna()

    # Formating the name and output path
    path_folder_out = os.path.join(path_folder_out, "figures")
    os.makedirs(path_folder_out, exist_ok=True)
    path_file_out = os.path.join(path_folder_out, name)

    # - Plot 1 - #
    # Plotting the raw data
    plt.plot(df_raw.Time, df_raw.Voltage, "b")

    # Formating the plot
    plt.title(name)
    plt.xlabel("Time")
    plt.ylabel("Voltage")
    plt.legend(["Raw"])

    # Saving the plot
    plt.savefig(path_file_out + "_VoltageRaw.png")

    # Display the plot or saving only
    if mode == "Display":
        plt.show()
    else:
        plt.clf()

    # - Plot 2 - #
    # Plotting the raw data
    plt.plot(df_raw.Voltage, df_raw.Current, "b")

    # Formating the plot
    plt.title(name)
    plt.xlabel("Voltage")
    plt.ylabel("Current")
    plt.legend(["Raw"])

    # Saving the plot
    plt.savefig(path_file_out + "_CycleRaw.png")

    # Display the plot or saving only
    if mode == "Display":
        plt.show()
    else:
        plt.clf()


def plot_potentiostat_proc(
    df_raw: pd.DataFrame,
    df_proc: pd.DataFrame,
    df_peak: pd.DataFrame,
    mode: str = "Display",
    name: str = "Potentiostat",
    path_folder_out: str = "",
):
    """
    Description :

        Plot and/or save figures for analyzing potentiostat data processing

    Args:

        df_raw (type: pd.DataFrame) : Raw potentiostat data Dataframe
        df_proc (type: pd.DataFrame) : Processed potentiostat data Dataframe
        df_peak (type: pd.DataFrame) : Peaks in the processed potentiostat Dataframe
        mode (type: str, optional) : 'Display' to display the figures, 'Save' to save them at path_folder_out or 'Both'
        name (type: str, optional) : Name to use for the saved files and figure titles
        path_folder_out (type: str, optional) : Path to the folder for saving the graphs
    """

    # Checking the inputs
    #####################
    if not isinstance(df_raw, pd.DataFrame):
        raise TypeError("Input df_raw is not a DataFrame")

    # Checking that Time, Voltage and Current are in the df_raw
    if (
        ("Time" not in df_raw.columns)
        or ("Voltage" not in df_raw.columns)
        or ("Current" not in df_raw.columns)
    ):
        raise ValueError("df_raw does not contain 'Time', 'Voltage' or 'Current'")

    if not isinstance(df_proc, pd.DataFrame):
        raise TypeError("Input df_proc is not a DataFrame")

    # Checking that Time, Voltage, Current and Ramp are in the df_proc
    if (
        ("Time" not in df_proc.columns)
        or ("Voltage" not in df_proc.columns)
        or ("Current" not in df_proc.columns)
        or ("Ramp" not in df_proc.columns)
    ):
        raise ValueError(
            "df_proc does not contain 'Time', 'Voltage', 'Current' or 'Ramp'"
        )

    if not isinstance(df_peak, pd.DataFrame):
        raise TypeError("Input df_peak is not a DataFrame")

    # Checking that Time, Voltage, Current, Ramp, PeakQuality and Extremum are in the df_peak
    if (
        ("Time" not in df_peak.columns)
        or ("Voltage" not in df_peak.columns)
        or ("Current" not in df_peak.columns)
        or ("Ramp" not in df_peak.columns)
        or ("PeakQuality" not in df_peak.columns)
        or ("Extremum" not in df_peak.columns)
    ):
        raise ValueError(
            "df_peak does not contain 'Time', 'Voltage', 'Current', 'Ramp', 'PeakQuality' or 'Extremum'"
        )

    # Checking mode
    if (mode != "Display") and (mode != "Save") and (mode != "Both"):
        raise ValueError("mode not recognized (Display, Save or Both)")

    if (mode == "Save") or (mode == "Both"):
        if path_folder_out == "":
            path_folder_out = os.path.join(os.getcwd())
            os.makedirs(path_folder_out, exist_ok=True)
            print(
                f"WARNING : no path_folder_out provided, figures will be saved at {path_folder_out}"
            )
        else:
            os.makedirs(path_folder_out, exist_ok=True)

    # Main
    ######
    df_raw = df_raw.dropna()

    # Plot results of full Cycle
    _plot_cycle(df_raw, df_proc, df_peak, mode, name, path_folder_out)

    # Init the num_ramp
    num_ramp = 0

    # Looping on the ramps
    while len(df_proc[df_proc["Ramp"] == num_ramp]) > 0:
        sub_df_proc = df_proc.loc[df_proc["Ramp"] == num_ramp]
        sub_df_peak = df_peak.loc[df_peak["Ramp"] == num_ramp]

        # Plotting the results on the ramp
        _plot_ramp(sub_df_proc, sub_df_peak, mode, name, path_folder_out, num_ramp)

        num_ramp = num_ramp + 1


########################
# - NESTED FUNCTIONS - #
########################


def _plot_cycle(
    df_raw: pd.DataFrame,
    df_proc: pd.DataFrame,
    df_peak: pd.DataFrame,
    mode: str,
    name: str,
    path_folder_out: str,
):
    """
    Description :

        Plot and/or save figures for analyzing potentiostat data processing over a full cycle

    Args:

        df_raw (type: pd.DataFrame) : Raw potentiostat data Dataframe
        df_proc (type: pd.DataFrame) : Processed potentiostat data Dataframe
        df_peak (type: pd.DataFrame) : Peaks in the processed potentiostat Dataframe
        mode (type: str, optional) : 'Display' to display the figures, 'Save' to save them at path_folder_out or 'Both'
        name (type: str, optional) : Name to use for the saved files and figure titles
        path_folder_out (type: str, optional) : Path to the folder for saving the graphs
    """

    # Main
    ######
    # Formating the name and output path
    path_folder_out = os.path.join(path_folder_out, "figures")
    os.makedirs(path_folder_out, exist_ok=True)
    path_file_out = os.path.join(path_folder_out, name)

    list_time_sliced = list(df_proc.Time[df_proc.Ramp.diff().ne(0)])
    list_time_sliced.append(df_proc.Time.iloc[-1])

    # - Plot 1 - #
    # Plotting the raw data
    plt.plot(df_raw.Time, df_raw.Voltage, "b")

    # Plotting the sliced index
    for i in list_time_sliced:
        if df_raw.Voltage[df_raw.Time == i].mean() > 0:
            plt.plot(i, df_raw.Voltage[df_raw.Time == i].max(), "+r", markersize=20)
        else:
            plt.plot(i, df_raw.Voltage[df_raw.Time == i].min(), "+r", markersize=20)

    # Formating the plot
    plt.title(name)
    plt.xlabel("Time")
    plt.ylabel("Voltage")
    plt.legend(["Raw", "Sliced"])

    # Saving the plot
    plt.savefig(path_file_out + "_VoltageRawSliced.png")

    # Display the plot or saving only
    if mode == "Display":
        plt.show()
    else:
        plt.clf()

    # - Plot 2 - #
    # Plotting the raw data
    plt.plot(df_raw.Voltage, df_raw.Current, "b")

    # Plotting the processed data
    plt.plot(df_proc.Voltage, df_proc.Current, "r")

    # Plotting the detected peaks
    plt.plot(df_peak.Voltage, df_peak.Current, "m+", markersize=12)

    # Formating the plot
    plt.title(name)
    plt.xlabel("Voltage")
    plt.ylabel("Current")
    plt.legend(["Cycle", "Peaks"])

    # Saving the plot
    plt.savefig(path_file_out + "_CycleSmoothPeaks.png")

    # Display the plot or saving only
    if (mode == "Display") or (mode == "Both"):
        plt.show()
    else:
        plt.clf()


def _plot_ramp(
    df_proc: pd.DataFrame,
    df_peak: pd.DataFrame,
    mode: str,
    name: str,
    path_folder_out: str,
    num_ramp: int,
):
    """
    Description :

        Plot and/or save figures for analyzing potentiostat data processing over a ramp

    Args:

        df_proc (type: pd.DataFrame) : Processed potentiostat data on the ramp
        df_peak (type: pd.DataFrame) : Peaks in the processed potentiostat data on the ramp
        mode (type: str, optional) : 'Display' to display the figures, 'Save' to save them at path_folder_out or 'Both'
        name (type: str, optional) : Name to use for the saved files and figure titles
        path_folder_out (type: str, optional) : Path to the folder for saving the graphs
        num_ramp (type: int, optional) : Number of the ramp to plot
    """

    # Main
    ######
    # Formating the name and output path
    path_folder_out = os.path.join(path_folder_out, "figures")
    os.makedirs(path_folder_out, exist_ok=True)
    path_file_out = os.path.join(path_folder_out, name)

    # Plotting the processed data
    plt.plot(df_proc.Voltage, df_proc.Current, "r")

    # Plotting the detected peaks
    plt.plot(df_peak.Voltage, df_peak.Current, "m+", markersize=12)

    # Adding the quality mark to the plot
    for j in range(len(df_peak)):
        plt.text(
            df_peak.Voltage.iloc[j],
            df_peak.Current.iloc[j],
            str(round(df_peak.PeakQuality.iloc[j], 2)),
        )

    # Formating the plot
    plt.title(name + " Ramp " + str(num_ramp))
    plt.xlabel("Voltage")
    plt.ylabel("Current")
    plt.legend(["Smooth", "Peaks"])

    # Saving the plot
    plt.savefig(path_file_out + "_SmoothPeaks" + str(num_ramp) + ".png")

    # Display the plot or saving only
    if (mode == "Display") or (mode == "Both"):
        plt.show()
    else:
        plt.clf()
