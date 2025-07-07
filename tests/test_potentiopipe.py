"""
Test files for the potentiopipe package

Modules:
    cli : CLI for the sub-package datapipeline
        Functions:
            process_raw_cli
            peak_detection_proc_cli

    data_processing : Data processing functions for the potentiostat
        Functions:
            process_raw
            peak_detection_proc
        Nested Functions:
            _cleaning_raw

    signal_processing : General Signal processing functions used for data processing of the potentiostat
        Functions:
            peak_detection
            slicing_ramp
        Nested Functions:
            _merge_neighbor_idx
            _non_consecutive_idx
            _find_candidate_extremum
            _extract_row_extremum

    types : Types Declaration for the sub-package datapipeline
        Structures:
            ParametersPeakDetection

    visualization : Visualization of the potentiostat data
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

# import pytest
#
# from potentiostat.datapipeline.cli import (
#     process_raw_cli,
#     peak_detection_proc_cli,
# )
#
# from potentiostat.datapipeline.data_processing import (
#     process_raw,
#     peak_detection_proc,
#     _cleaning_raw,
# )
#
# from potentiostat.datapipeline.signal_processing import (
#     peak_detection,
#     slicing_ramp,
#     _merge_neighbor_idx,
#     _non_consecutive_idx,
#     _find_candidate_extremum,
#     _extract_row_extremum,
# )
#
# from potentiostat.datapipeline.types import (
#     ParametersPeakDetection,
# )
#
# from potentiostat.datapipeline.visualization import (
#     plot_potentiostat_raw,
#     plot_potentiostat_proc,
#     _plot_ramp,
#     _plot_cycle,
# )


class cli:
    def test_something(self):
        pass


#
# ##################
# # - VALIDATION - #
# ##################
#
# if __name__ == "__main__":
#     FullChain = False
#     # FullChainSplit = False
#     PeakDetection = False
#
#     # Full Chain Validation
#     #######################
#
#     if FullChain:
#         FolderIn = os.path.join("../data_20240718", "rawdata")
#         FolderOut = os.path.join("../data_20240718", "procdatatest")
#
#         if not os.path.isdir(FolderIn):
#             print("Input folder does not exist")
#             sys.exit(1)
#         else:
#             List_Files = os.listdir(FolderIn)
#
#         for File in List_Files:
#             if File.find("_CDPV_") >= 0:
#                 FilePath = os.path.join(FolderIn, File)
#                 FileStream = open(FilePath, "r")
#                 DataFrameProc, DataFramePeaks = DataProcessingPotentiostat(FileStream)
#
#                 # Naming the datas to save
#                 FileTemp = File.split("_")
#                 for i in range(len(FileTemp)):
#                     if FileTemp[i] == "raw":
#                         FileTemp[i] = "proc"
#                 FileOutProc = "_".join(FileTemp)
#
#                 FileTemp = FileOutProc.removesuffix(".csv")
#                 FileOutPeaks = FileTemp + "_peaks.csv"
#
#                 # Path to the processed Data
#                 PathOutProc = os.path.join(FolderOut, FileOutProc)
#                 PathOutPeak = os.path.join(FolderOut, FileOutPeaks)
#
#                 # Save the processed Data
#                 DataFrameProc.to_csv(PathOutProc, index=False)
#                 DataFramePeaks.to_csv(PathOutPeak, index=False)
#
#                 # Plotting the results
#                 PlotDataProcessingPotentiostat(
#                     FilePath, PathOutProc, PathOutPeak, FolderOut, Plot="Display"
#                 )
#
#     # Full Chain Validation
#     #######################
#
#     # if FullChainSplit:
#     #
#     #     FolderIn = os.path.join('../data_20240718', 'rawdata')
#     #     FolderOut = os.path.join('../data_20240718', 'procdatatest')
#     #
#     #     if not os.path.isdir(FolderIn):
#     #         print('Input folder does not exist')
#     #         sys.exit(1)
#     #     else:
#     #         List_Files = os.listdir(FolderIn)
#     #
#     #     for File in List_Files:
#     #         if File.find('_CDPV_') >= 0:
#     #
#     #             # Naming the datas to save
#     #             FileTemp = File.split('_')
#     #             for i in range(len(FileTemp)):
#     #                 if FileTemp[i] == 'raw':
#     #                     FileTemp[i] = 'proc'
#     #             FileOutProc = "_".join(FileTemp)
#     #
#     #             FileTemp = FileOutProc.removesuffix('.csv')
#     #             FileOutPeaks = FileTemp + '_peaks.csv'
#     #
#     #             # Path to the processed Data
#     #             PathOutProc = os.path.join(FolderOut, FileOutProc)
#     #             PathOutPeak = os.path.join(FolderOut, FileOutPeaks)
#     #
#     #             # Data processing
#     #             FilePath = os.path.join(FolderIn, File)
#     #             FileStream = open(FilePath, "r")
#     #             DataFrameProc = DataProcessingRawPotentiostat(FileStream)
#     #             DataFrameProc.to_csv(PathOutProc, index=False)
#     #
#     #             # Peak detection
#     #             FileStream2 = open(PathOutProc, "r")
#     #             DataFramePeaks = DataProcessingPeakPotentiostat(FileStream2)
#     #             DataFramePeaks.to_csv(PathOutPeak, index=False)
#     #
#     #             # Plotting the results
#     #             PlotDataProcessingPotentiostat(FilePath, PathOutProc, PathOutPeak, FolderOut, Plot='Display')
#
#     # Peaks Detection Validation
#     ############################
#
#     if PeakDetection:
#         FolderProcData = os.path.join("../data_20240718", "TestDetection")
#
#         if not os.path.isdir(FolderProcData):
#             print("Input folder does not exist")
#             sys.exit(1)
#         else:
#             List_Files = os.listdir(FolderProcData)
#
#         for File in List_Files:
#             if (File.find(".csv") != -1) and (File.find("_peaks") == -1):
#                 FilePath = os.path.join(FolderProcData, File)
#                 DataFrame = pd.read_csv(FilePath, na_values="NAN", header=0)
#
#                 NumRamp = 0
#                 while len(DataFrame[DataFrame["Ramp"] == NumRamp]) > 0:
#                     SubDataFrame = DataFrame[DataFrame["Ramp"] == NumRamp]
#
#                     # Parameters Detection
#                     NamesDetection = ["Voltage", "Current"]
#                     HalfWidthMin = 0.1  # Volt 0.05
#                     WidthMax = 0.3  # Volt
#                     DerivationSensitivity = 0.00004  # Ampere/Volt  0.00005
#                     DerivationWidth = 0.05  # Volt 0.1
#
#                     if (
#                         SubDataFrame.Voltage.iloc[-1] - SubDataFrame.Voltage.iloc[0]
#                     ) > 0:
#                         SubDataFramePeaks = sp.PeakDetection(
#                             SubDataFrame,
#                             NamesDetection,
#                             HalfWidthMin,
#                             WidthMax,
#                             DerivationWidth,
#                             DerivationSensitivity,
#                             TypeExtremum="Max",
#                         )
#                     else:
#                         SubDataFramePeaks = sp.PeakDetection(
#                             SubDataFrame,
#                             NamesDetection,
#                             HalfWidthMin,
#                             WidthMax,
#                             DerivationWidth,
#                             DerivationSensitivity,
#                             TypeExtremum="Min",
#                         )
#
#                     NameExperiment = File.removesuffix(".csv")
#                     _PlotRamp(
#                         SubDataFrame,
#                         SubDataFramePeaks,
#                         NumRamp,
#                         FolderProcData,
#                         NameExperiment,
#                         "Display",
#                     )
#
#                     NumRamp = NumRamp + 1
