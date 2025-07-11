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
