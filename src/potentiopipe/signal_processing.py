"""
General Signal processing functions used for data processing of the potentiostat

Functions:
    peak_detection
    slicing_ramp

Nested functions:
    _merge_neighbor_idx
    _non_consecutive_idx
    _find_candidate_extremum
    _extract_row_extremum
"""


###############
# - IMPORTS - #
###############

# Libraries
import pandas as pd
import numpy as np
from typing import List

# Inside the package
from potentiopipe.types import ParametersPeakDetection


#################
# - FUNCTIONS - #
#################


def peak_detection(
    df: pd.DataFrame,
    series_name: List[str],
    parameters: ParametersPeakDetection,
    type_extremum: str = "Max",
) -> pd.DataFrame:
    """
    Description :

        Detect peaks (maximum or minimum) from a DataFrame Series Y by derivation with X

    Args:

        df (type: pd.DataFrame) : Dataframe with Series X and Y
        series_name (type: List[str]) : Names of the Series X and Y
        parameters (type: Named Tuple, optional) : Contains the parameters for the peak detection
        type_extremum (str) : Type of the extremum ("Max", "Min" or "Both")

    Returns:

        df_peak (type: pd.DataFrame) : Row of Peaks found on df extended with a quality marker
    """

    # Checking the inputs
    #####################
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df is not a DataFrame")

    if not isinstance(series_name, list):
        raise TypeError("Input series_name is not a List")

    if not isinstance(parameters, ParametersPeakDetection):
        raise TypeError("Input parameters is not a ParametersPeakDetection")

    if not isinstance(type_extremum, str):
        raise TypeError("Input type_extremum is not a str")

    if len(series_name) != 2:
        raise ValueError("series_name must contain 2 elements")

    # Checking that Names are in DataFrame
    if (series_name[0] not in df) or (series_name[1] not in df):
        raise ValueError("series_name not found in DataFrame")

    # Checking type_extremum
    if type_extremum == "Max":
        b_max = 1
        b_min = 0
    elif type_extremum == "Min":
        b_max = 0
        b_min = 1
    elif type_extremum == "Both":
        b_max = 1
        b_min = 1
    else:
        raise ValueError("type_extremum not recognized (Max, Min or Both)")

    # Checking the consistency of parameters
    if (
        (parameters.width_max <= 0)
        or (parameters.half_width_min <= 0)
        or (parameters.derivation_width <= 0)
    ):
        raise ValueError(
            "parameters : width_max, half_width_min, derivation_width must be greater than zero"
        )

    if parameters.derivation_sensitivity < 0:
        raise ValueError("parameters : derivation_sensitivity must be positive")

    if parameters.width_max < parameters.half_width_min:
        raise ValueError("parameters : width_max must be greater than half_width_min")

    # Checking the consistency of df
    if len(df) < parameters.width_max:
        raise ValueError("Not enough elements in df compared to parameters.width_max")

    # Main
    ######
    # Initialization of the DataFrame containing the peaks
    df_peak = pd.DataFrame()

    # Extracting the average unit_step of X
    unit_step = abs(df[series_name[0]].diff().dropna().mean())

    # Converting the Width from unit of X to Index
    half_width_min_idx = parameters.half_width_min // unit_step
    width_max_idx = parameters.width_max // unit_step
    derivation_width_idx = parameters.derivation_width // unit_step

    # TODO : Non continuity of the Series could be a problem, write a loop on X not the index or interpolating
    #  the missing X,Y
    # Derivation of Y by X with a step HalfWidthMin
    df_derivation = (
        df[series_name[1]].diff(periods=derivation_width_idx).dropna()
        / df[series_name[0]].diff(periods=derivation_width_idx).dropna().abs()
    )

    # Detection is impossible on the first derivation_width_idx and we discard the last derivation_width_idx
    # (to remove the smoothing border artifacts)
    df_derivation.drop(df_derivation.index[-int(derivation_width_idx) :], inplace=True)

    # Extracting the derivative higher than the threshold DerivationSensitivity
    df_derivation_inc = df_derivation[df_derivation > parameters.derivation_sensitivity]
    df_derivation_dec = df_derivation[
        df_derivation < -parameters.derivation_sensitivity
    ]

    # Extracting the indices where the derivative just surpasses or drops below the threshold DerivationSensitivity
    inc_idx = _non_consecutive_idx(df_derivation_inc)
    dec_idx = _non_consecutive_idx(df_derivation_dec)

    # Sign of the derivation
    df_derivation_sign = np.sign(df_derivation)

    # Extracting the zeros of the derivation to get indexes of extremum
    zero_idx = df_derivation.index[df_derivation_sign.diff().fillna(0).ne(0)].tolist()

    if (len(zero_idx) != 0) and ((len(inc_idx) != 0) or (len(dec_idx) != 0)):
        # Extracting only the maximum
        if b_max:
            peak_idx_max, dict_inc_max, dict_dec_max = _find_candidate_extremum(
                zero_idx,
                inc_idx,
                dec_idx,
                width_max_idx,
                half_width_min_idx,
                df_derivation_sign,
            )
            peak_idx_max = _merge_neighbor_idx(
                peak_idx_max, half_width_min_idx, dict_inc_max, dict_dec_max
            )
            df_peak = _extract_row_extremum(
                df,
                df_derivation_sign,
                df_peak,
                peak_idx_max,
                dict_inc_max,
                dict_dec_max,
                derivation_width_idx,
                series_name[1],
                "Max",
            )

        # Extracting only the minimum
        if b_min:
            peak_idx_min, dict_dec_min, dict_inc_min = _find_candidate_extremum(
                zero_idx,
                dec_idx,
                inc_idx,
                width_max_idx,
                half_width_min_idx,
                df_derivation_sign,
            )
            peak_idx_min = _merge_neighbor_idx(
                peak_idx_min, half_width_min_idx, dict_dec_min, dict_inc_min
            )
            df_peak = _extract_row_extremum(
                df,
                df_derivation_sign,
                df_peak,
                peak_idx_min,
                dict_dec_min,
                dict_inc_min,
                derivation_width_idx,
                series_name[1],
                "Min",
            )

    # Returning the DataFrame containing the detected peaks
    return df_peak


def slicing_ramp(df: pd.DataFrame, series_name: str) -> List[int]:
    """
    Description :

        Slice a periodic signal (triangular) into ramps

    Args:

        df (type: pd.DataFrame) : Dataframe with Series X
        series_name (type: str) : Name of the Series X

    Returns:

        list_idx (type: List[int]) : List of the indices of the starting and ending points of the ramps
    """

    # Inner Parameters
    ##################
    # Sensitivity to detect the ramps
    threshold_extremum = 0.9
    percentage_ramp_valid = 0.5

    # Checking the inputs
    #####################
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df is not a DataFrame")

    if not isinstance(series_name, str):
        raise TypeError("Input series_name is not a string")

    # Checking that series_name is in DataFrame
    if series_name not in df:
        raise ValueError("series_name not found in df")

    # Main
    ######
    # Extracting the min and max value of the cycle to slice
    value_max = threshold_extremum * df[series_name].max()
    value_min = threshold_extremum * df[series_name].min()

    # DataFrame around the min and max
    df_max = df[df[series_name] > value_max]
    df_min = df[df[series_name] < value_min]

    # Indexes
    df_max_start_idx = int(df_max.index.tolist()[0])
    df_max_end_idx = int(df_max.index.tolist()[-1])
    df_min_start_idx = int(df_min.index.tolist()[0])
    df_min_end_idx = int(df_min.index.tolist()[-1])
    df_start_idx = int(df.index.tolist()[0])
    df_end_idx = int(df.index.tolist()[0])

    if (len(df_max) == 0) or (len(df_min) == 0):
        raise ValueError(
            "Not enough points on the df, ramp dynamic is too fast or sampling is too low"
        )

    # TODO : Valid if the frequency of ramp is not varying threw the datas analyzed, check sensitivity to data loss
    # Estimation of the half period
    half_period = max(
        abs(df_max_start_idx - df_min_start_idx),
        abs(df_max_end_idx - df_min_end_idx),
    )

    # Defining if the ramp is increasing or decreasing
    if df_max_start_idx < df_min_start_idx:
        b_search_max = 1
    else:
        b_search_max = 0

    # Selecting the first and last index of the search
    loop_idx = min(df_max_start_idx, df_min_start_idx)
    end_idx = max(df_max_end_idx, df_min_end_idx)

    list_idx = []

    # If first ramp is at least 50% completed we take it into account
    if (loop_idx - df_start_idx) >= percentage_ramp_valid * half_period:
        list_idx.append(df_start_idx)

    # Searching alternately for max and min to slice the ramps
    while loop_idx < end_idx:
        if b_search_max:
            df_temp = df_max.iloc[
                (df_max.index >= loop_idx)
                & (df_max.index <= (loop_idx + 1.25 * half_period))
            ]
            new_idx = df_temp[series_name].idxmax()
            b_search_max = 0
        else:
            df_temp = df_min.iloc[
                (df_min.index >= loop_idx)
                & (df_min.index <= (loop_idx + 1.25 * half_period))
            ]
            new_idx = df_temp[series_name].idxmin()
            b_search_max = 1

        # Add the new index to the list of the ramp extremum
        list_idx.append(new_idx)
        loop_idx = int(df_temp.index.tolist()[-1])

    # If last ramp is at least 50% completed we take it into account
    if (df_end_idx - end_idx) > percentage_ramp_valid * half_period:
        list_idx.append(df_end_idx)

    # Return the index of the extremum of the ramps
    return list_idx


########################
# - NESTED FUNCTIONS - #
########################


def _merge_neighbor_idx(
    list_idx: List[int],
    distance: int,
    dict1: dict | None = None,
    dict2: dict | None = None,
) -> List[int]:
    """
    Description :

        Merge the indices in list_idx that are within distance of each other.
        Also update the associated dictionaries dict1 and dict2, if they exist

    Args:

        list_idx (type: List[int]) : List of the indices to check for merging
        distance (type: int) : minimal distance between neighboring indices
        dict1 (type : dict) : Dictionary with index as key
        dict2 (type : dict) : Dictionary with index as key

    Returns:

        list_idx (type: List[int]) : List of the indices merged
    """

    # Main
    ######
    # TODO : Maybe a check on the WidthMax to avoid merging to much points ?
    cpt = 0
    tmp_len = len(list_idx) - 1

    while cpt < tmp_len:
        if (list_idx[cpt + 1] - list_idx[cpt]) <= distance:
            new_idx = int((list_idx[cpt + 1] + list_idx[cpt]) // 2)

            if dict1 is not None:
                dict1[str(new_idx)] = min(
                    dict1[str(list_idx[cpt])], dict1[str(list_idx[cpt + 1])]
                )

            if dict2 is not None:
                dict2[str(new_idx)] = max(
                    dict2[str(list_idx[cpt])], dict2[str(list_idx[cpt + 1])]
                )

            list_idx[cpt] = new_idx
            list_idx.pop(cpt + 1)

            tmp_len -= 1
        else:
            cpt += 1

    return list_idx


def _non_consecutive_idx(df: pd.DataFrame) -> List[int]:
    """
    Description :

        Extracting the indices of a DataFrame that are not consecutive

    Args:

        df (type: pd.DataFrame) : List of the indices to check for merging

    Returns:

        idx (type: List[int]) : List of the indices
    """

    # Main
    ######
    idx = []

    if len(df) > 0:
        idx.append(int(df.index.tolist()[0]))
        if len(df) > 1:
            idx.append(int(df.index.tolist()[-1]))

    idx = idx + df[df.index.diff() > 1].index.tolist()
    idx = idx + df[df.index.diff(periods=-1) < -1].index.tolist()

    # Sorting them for faster calculation later
    idx.sort()

    return idx


def _find_candidate_extremum(
    zero_idx: List[int],
    list_idx1: List[int],
    list_idx2: List[int],
    width_max_idx: int,
    half_width_min_idx: int,
    df_derivation_sign: pd.DataFrame,
) -> tuple[List[int], dict, dict]:
    """
    Description :

        Extracting the indices that are good candidates to be extremum meaning we want at least one side of the peak
        to have a dynamic over the derivative threshold and at least one side of the peak to globally increase or
        decrease

    Args:

        zero_idx (type: List[int]) : List of the indices of the zeros of the derivative
        list_idx1 (type: List[int]) : List of the indices of the derivative over the threshold
        list_idx2 (type: List[int]) : List of the indices of the derivative over the threshold
        width_max_idx (type: int) : Maximum width of the peak to be detected
        half_width_min_idx (type: int) : Minimum half width of the peak to be detected
        df_derivation_sign (type: pd.DataFrame) : Sign of the derivative for the detection

    Returns:

        peak_idx (type: List[int]) : List of the indices of the potential peaks
        dict1 (type: dict) : Dictionary with index of the peak as key and index of the derivative over the threshold
                             as value
        dict2 (type: dict) : Dictionary with index of the peak as key and index of the derivative over the threshold
                             as value
    """

    # Main
    ######
    # Monotonicity sensitivity around the zeros
    # TODO : CHeck these values 0.8 / 0.5
    monotonicity_sensitivity_1 = 0.75
    monotonicity_sensitivity_2 = 0.25

    # Initialization
    dict1 = {}
    dict2 = {}
    peak_idx = []

    # For each zero_idx we want at least one side of the peaks to have a derivation dynamic > derivation_sensitivity
    for zero in zero_idx:
        # Initialization
        b_valid_idx1 = 0
        b_valid_idx2 = 0

        # The idx1 should be before the zero and distanced of maximum width_max_idx
        for idx1 in list_idx1:
            # If the distance to zero is already negative then no candidate (idx1 is ordered)
            if (zero - idx1) < 0:
                break

            if ((zero - idx1) <= width_max_idx) and ((zero - idx1) >= 0):
                b_valid_idx1 = 1
                dict1[str(zero)] = idx1

        # The idx2 should be after the zero and distanced of maximum width_max_idx
        for idx2 in list_idx2:
            # If the distance to zero is already > width_max_idx then no candidate (idx2 is ordered)
            if (idx2 - zero) > width_max_idx:
                break

            if ((idx2 - zero) <= width_max_idx) and ((idx2 - zero) >= 0):
                b_valid_idx2 = 1
                dict2[str(zero)] = idx2
                break

        # If at least one side of the peak is valid then zero is a good candidate
        if (b_valid_idx1 == 1) or (b_valid_idx2 == 1):
            # If no idx1 was found then a distance to zero of half_width_min_idx is chosen
            if b_valid_idx1 == 0:
                dict1[str(zero)] = zero - half_width_min_idx

            # If no idx2 was found then a distance to zero of half_width_min_idx is chosen
            if b_valid_idx2 == 0:
                dict2[str(zero)] = zero + half_width_min_idx

            # Before the index Y should globally increase, after it should globally decrease : at least one of the condition should be fulfilled (peak flat on one side )
            if dict1[str(zero)] == zero:
                mean_sign_derivation_before = df_derivation_sign[zero - 1]
            else:
                mean_sign_derivation_before = df_derivation_sign[
                    (df_derivation_sign.index >= dict1[str(zero)])
                    & (df_derivation_sign.index < zero)
                ].mean()
            if dict2[str(zero)] == zero:
                mean_sign_derivation_after = df_derivation_sign[zero]
            else:
                mean_sign_derivation_after = df_derivation_sign[
                    (df_derivation_sign.index > zero)
                    & (df_derivation_sign.index <= dict2[str(zero)])
                ].mean()

            if (
                (mean_sign_derivation_before > monotonicity_sensitivity_1)
                and (mean_sign_derivation_after < -monotonicity_sensitivity_2)
            ) or (
                (mean_sign_derivation_before > monotonicity_sensitivity_2)
                and (mean_sign_derivation_after < -monotonicity_sensitivity_1)
            ):
                # The candidate become a valid peak
                peak_idx.append(zero)

    return peak_idx, dict1, dict2


def _extract_row_extremum(
    df: pd.DataFrame,
    df_derivation_sign: pd.DataFrame,
    df_peak: pd.DataFrame,
    peak_idx: List[int],
    dict1: dict,
    dict2: dict,
    derivation_width_idx: int,
    name: str,
    type_extremum: str,
) -> pd.DataFrame:
    """
    Description :

        Extracting the indices of a DataFrame that are not consecutive

    Args:

        df (type: pd.DataFrame) : DataFrame in which the peak should be detected
        df_derivation_sign (type: pd.DataFrame) : DataFrame with the derivative sign
        df_peak (type: pd.DataFrame) : DataFrame with the detected peaks to fill up
        peak_idx (type: List[int]) : List with indices of the peaks
        dict1 (type: dict) : Dictionary with the peak index as the key and the window start index as the value
        dict2 (type: dict) : Dictionary with the peak index as the key and the window end index as the value
        derivation_width_idx (type: int) : Horizon on which the derivation is performed
        name (type: str) : Name of the series in which to find the peak
        type_extremum (type: str) : Type of the extremum ("Max" or "Min")


    Returns:

        df_peak (type: pd.DataFrame) :  DataFrame with the detected peaks to filled up
    """

    # Main
    ######
    for i in peak_idx:
        # Focusing on a window around the zero to extract the row of the extremum
        # StartWindow is adjusted  to take into account the horizon of the Derivation (DerivationWidthIndex)
        start_window_idx = dict1[str(i)] - derivation_width_idx
        end_window_idx = dict2[str(i)]

        # Creating the window
        df_window = df[(df.index >= start_window_idx) & (df.index <= end_window_idx)]

        if type_extremum == "Max":
            extremum_idx = np.argmax(df_window[name])
        else:
            extremum_idx = np.argmin(df_window[name])

        # Extracting the row of the extremum
        row_extremum = df_window.iloc[extremum_idx : extremum_idx + 1].copy()

        # Avoiding double detection on one peak
        if len(df_peak) > 0:
            if (df_peak[row_extremum.columns] == row_extremum.values).all(axis=1).any():
                continue

        # Sign of the derivation on the peak window
        mean_sign_derivation_before = df_derivation_sign[
            (df_derivation_sign.index >= start_window_idx + derivation_width_idx)
            & (df_derivation_sign.index < i)
        ].mean()
        mean_sign_derivation_after = df_derivation_sign[
            (df_derivation_sign.index >= i)
            & (df_derivation_sign.index <= end_window_idx)
        ].mean()

        # Quality Mark is based on the fluctuation of the derivation before and after the zero
        # it takes into account smoothness of the signal (on the derivation horizon) and sharpness of the peak
        # TODO : Add a mark about peak height and smoothness of original signal ? Peak window seems really zoomed
        #  to really assess height and for sign of derivation to have a real impact on the quality mark
        quality_mark_derivation = abs(
            mean_sign_derivation_before * mean_sign_derivation_after
        )

        # Adding the Quality Mark to the row of the extremum
        row_extremum["PeakQuality"] = quality_mark_derivation  # * DeltaExtremumWindow
        row_extremum["Extremum"] = type_extremum

        # Storing the row of the extremum in the DataFrame
        df_peak = pd.concat([df_peak, row_extremum], axis=0)

    return df_peak
