"""
Data processing functions for the potentiostat

Functions:
    process_raw
    peak_detection_proc

Nested functions:
    _cleaning_raw
"""


###############
# - IMPORTS - #
###############

# Libraries
from scipy.signal import savgol_filter
import pandas as pd

# Inside the package
from potentiopipe.types import ParametersPeakDetection
from potentiopipe.signal_processing import slicing_ramp, peak_detection


####################
# - GLOBAL SCOPE - #
####################

# - Default Parameters for ParametersDataProcessing
###################################################

# Peak Detection
half_width_min_default = 0.1  # Volt
width_max_default = 0.3  # Volt
derivation_width_default = 0.05  # Volt
derivation_sensitivity_default = 0.00004  # Ampere/Volt

# Default values of the Named tuple of the parameters
parameters_peak_detection_default = ParametersPeakDetection(
    half_width_min_default,
    width_max_default,
    derivation_width_default,
    derivation_sensitivity_default,
)


#################
# - FUNCTIONS - #
#################


def process_raw(
    df_raw: pd.DataFrame, smoothing_window_percentage: float = 0.1
) -> pd.DataFrame:
    """
    Description :

        Process the raw potentiostat data by slicing it into Voltage ramp, cleaning the signal, and then smoothing
        the Current and Voltage

    Args:

        df_raw (type: pd.DataFrame) : Raw potentiostat data Dataframe
        smoothing_window_percentage (type: float, optional) : percentage of the ramp length used as the smoothing window
            for the Savgol filter

    Returns:

        df_proc (type: pd.DataFrame) : Processed potentiostat data Dataframe
    """

    # Checking the inputs
    #####################
    if not isinstance(df_raw, pd.DataFrame):
        raise TypeError("Input df_raw is not a DataFrame")

    # Checking that Voltage and Current are in the DataFrame
    if (
        ("Voltage" not in df_raw.columns)
        or ("Current" not in df_raw.columns)
        or ("Time" not in df_raw.columns)
    ):
        raise ValueError("df_raw does not contain 'Voltage', 'Current' or 'Time'")

    # Main
    ######
    # Cleaning the DataFrame
    df_raw.dropna(inplace=True)

    # Indexes of the Voltage ramps
    index_list = slicing_ramp(df_raw, "Voltage")

    # Initialization of the output DataFrame containing the processed data
    df_proc = pd.DataFrame()

    # Smoothing and cleaning by ramps
    for num_ramp in range(len(index_list) - 1):
        # Index of the Subset Dataframe
        start_idx = index_list[num_ramp]
        end_idx = index_list[num_ramp + 1] - 1

        # Extracting Subset the DataFrame
        df_raw_ramp = df_raw.loc[(df_raw.index >= start_idx) & (df_raw.index < end_idx)]

        # Cleaning the artifacts on the Potentiostat datas
        df_raw_ramp = _cleaning_raw(df_raw_ramp)

        # Size of the windows
        window_savgol = int(smoothing_window_percentage * len(df_raw_ramp))

        df_proc_ramp = pd.DataFrame()

        # Smoothing of the Current and Voltage on the same window size
        df_proc_ramp["Time"] = df_raw_ramp["Time"]
        df_proc_ramp["Current"] = savgol_filter(df_raw_ramp.Current, window_savgol, 2)
        df_proc_ramp["Voltage"] = savgol_filter(df_raw_ramp.Voltage, window_savgol, 2)

        # Adding the ramp number to the cleaned DataFrame
        df_proc_ramp["Ramp"] = [num_ramp for j in range(len(df_proc_ramp))]

        # Storing the processed ramp in the output DataFrame
        df_proc = pd.concat([df_proc, df_proc_ramp], axis=0)

    # Output DataFrame
    return df_proc


def peak_detection_proc(
    df_proc: pd.DataFrame,
    parameters: ParametersPeakDetection = parameters_peak_detection_default,
) -> pd.DataFrame:
    """
    Description :

        Perform peak detection on the Current of a processed DataFrame

    Args:

        df_proc (type: pd.DataFrame) : Processed potentiostat data Dataframe
        parameters (type: Named Tuple, optional) : Contains the parameters for the peak detection

    Returns:

        df_peak (type: pd.DataFrame) : Peaks found on the processed data extended with a quality mark
    """

    # Checking the inputs
    #####################
    if not isinstance(df_proc, pd.DataFrame):
        raise TypeError("Input df_proc is not a DataFrame")

    if not isinstance(parameters, ParametersPeakDetection):
        raise TypeError("Input parameters is not a ParametersPeakDetection")

    # Checking that Voltage and Current are in the DataFrame
    if (
        ("Voltage" not in df_proc.columns)
        or ("Current" not in df_proc.columns)
        or ("Ramp" not in df_proc.columns)
    ):
        raise ValueError("df_proc does not contain 'Voltage', 'Current' or 'Ramp'")

    # Remove unwanted column if it exists
    if "Unnamed: 0" in df_proc.columns:
        df_proc.drop(columns=["Unnamed: 0"], inplace=True)

    # Main
    ######
    # Initialization of the output DataFrame containing the peaks
    df_peak = pd.DataFrame()

    # Initialization
    series_peak_detection = ["Voltage", "Current"]
    num_ramp = 0

    # Peak detection by ramps
    while len(df_proc[df_proc["Ramp"] == num_ramp]) > 0:
        # Extracting Subset the DataFrame
        df_proc_ramp = df_proc.loc[df_proc["Ramp"] == num_ramp]

        # If we are on an increasing ramp we want the maximums, on a decreasing ramp the minimums
        if (df_proc_ramp.Voltage.iloc[-1] - df_proc_ramp.Voltage.iloc[0]) > 0:
            df_peak_ramp = peak_detection(
                df_proc_ramp, series_peak_detection, parameters, type_extremum="Max"
            )
        else:
            df_peak_ramp = peak_detection(
                df_proc_ramp, series_peak_detection, parameters, type_extremum="Min"
            )

        # Storing the detected peaks in the output DataFrame
        if len(df_peak_ramp) > 0:
            df_peak = pd.concat([df_peak, df_peak_ramp], axis=0)

        num_ramp += 1

    # Outputs DataFrames
    return df_peak


########################
# - NESTED FUNCTIONS - #
########################


def _cleaning_raw(
    df_raw: pd.DataFrame, voltage_threshold: float = 0.04
) -> pd.DataFrame:
    """
    Description :

        Clean the raw data by erasing signal artifacts

    Args:

        df_raw (type: pd.DataFrame) : Raw potentiostat data Dataframe
        voltage_threshold (type: float, optional) : Voltage Threshold for the detection of the

    Returns:

        df_clean (type: pd.DataFrame) : Peaks found on the processed data
    """

    # Differentiating of the Voltage to identify anomalies
    series_voltage_diff = df_raw.Voltage.diff()

    # Extracting the index to clear
    idx_anomalies = list(
        df_raw.Voltage[series_voltage_diff.abs() >= voltage_threshold].index
    )

    if len(idx_anomalies) > 0:
        # Case of decreasing ramp
        if df_raw.Voltage.iloc[0] - df_raw.Voltage.iloc[-1] > 0:
            # Meaning we started with going down, then it is not a full anomaly pattern
            if (
                series_voltage_diff[series_voltage_diff.index == idx_anomalies[0]].iloc[
                    0
                ]
                < 0
            ):
                idx_anomalies = [int(series_voltage_diff.index[0])] + idx_anomalies

            # Meaning we finished with going up, then it is not a full anomaly pattern
            if (
                series_voltage_diff[
                    series_voltage_diff.index == idx_anomalies[-1]
                ].iloc[0]
                > 0
            ):
                idx_anomalies = idx_anomalies + [int(series_voltage_diff.index[-1])]

        # Case of increasing ramp
        else:
            # Meaning we started with going up, then it is not a full anomaly pattern
            if (
                series_voltage_diff[series_voltage_diff.index == idx_anomalies[0]].iloc[
                    0
                ]
                > 0
            ):
                idx_anomalies = [int(series_voltage_diff.index[0])] + idx_anomalies

            # Meaning we finished with going down, then it is not a full anomaly pattern
            if (
                series_voltage_diff[
                    series_voltage_diff.index == idx_anomalies[-1]
                ].iloc[0]
                < 0
            ):
                idx_anomalies = idx_anomalies + [int(series_voltage_diff.index[-1])]

    # To account for imperfect slicing caused by the anomaly, and the possibility of detecting the anomaly pattern
    # in the next ramp
    if len(idx_anomalies) % 2 != 0:
        idx_anomalies.pop(-1)

    # A pattern to clean is located between a rising edge and a dropping edge
    for i in range(len(idx_anomalies) // 2):
        # The pattern on the Voltage is also creating a transitional effect on the current that we need to clean
        current_patern_size = (idx_anomalies[2 * i + 1] - idx_anomalies[2 * i]) // 2

        # Calculating the indexes to remove from the DataFrame
        idx_remove = list(
            df_raw[
                (df_raw.index >= idx_anomalies[2 * i])
                & (df_raw.index <= idx_anomalies[2 * i + 1] + current_patern_size)
            ].index
        )

        # Cleaning the anomaly on the voltage and the Current
        df_raw.drop(idx_remove, inplace=True)

    # TODO : We could also cleaned the residual spikes on the current, too much data loss ? For now we consider
    #  the smoothing called after this function is enough

    # Cleaned DataFrame
    return df_raw
