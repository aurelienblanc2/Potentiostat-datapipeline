"""
Command Line Interface (CLI) for the potentiopipe package

Functions:
    process_raw_cli
    peak_detection_proc_cli
"""


###############
# - IMPORTS - #
###############

# Libraries
import sys
import io
import pandas as pd

# Inside the package
from potentiopipe.data_processing import process_raw, peak_detection_proc


####################
# - GLOBAL SCOPE - #
####################
# TODO : Place Holder until the raw data are also managed by the package
columns_raw_file = ["Time", "Voltage", "Current", "Cycle", "Dummy", "Reference"]


#################
# - FUNCTIONS - #
#################


def process_raw_cli() -> pd.DataFrame:
    """
    Description :

        cli version of the function process_raw

        Process the raw potentiostat data by slicing it into Voltage ramp, cleaning the signal, and then smoothing
        the Current and Voltage

    Args:

        raw_data_stream (type: StringIO) : Stream of raw potentiostat data to be processed

    Returns:

        df_proc (type: pd.DataFrame) : Processed potentiostat data Dataframe
    """

    # Formatting Inputs
    ###################
    # Input stream
    raw_data_stream = sys.argv[1]

    # Checking the inputs
    #####################
    if not isinstance(raw_data_stream, io.IOBase):
        raise TypeError("Input is not a file-like object")

    # Main
    ######
    # Reading the stream
    df_raw = pd.read_csv(
        raw_data_stream, header=None, na_values="NAN", names=columns_raw_file
    )

    # Calling the function
    return process_raw(df_raw)


def peak_detection_proc_cli() -> pd.DataFrame:
    """
    Description :

        cli version of the function peak_detection_proc

        Perform peak detection on the Current of a processed DataFrame

    Args:

        proc_data_stream (type: StringIO) : Stream of processed data

    Returns:

        df_peaks (type: pd.DataFrame) : Peaks found on the processed data
    """

    # Formatting Inputs
    ###################
    # Input stream
    proc_data_stream = sys.argv[1]

    # Checking the inputs
    #####################
    if not isinstance(proc_data_stream, io.IOBase):
        raise TypeError("Input is not a file-like object")

    # Main
    ######
    # Reading the stream
    df_proc = pd.read_csv(proc_data_stream, header=0, na_values="NAN")

    # Calling the function
    return peak_detection_proc(df_proc)
