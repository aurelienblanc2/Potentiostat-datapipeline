"""
Package focused on data processing, analysis and visualization of the potentiostat data

Modules:

    cli : CLI for the potentiopipe package

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

    types : Types Declaration for the potentiopipe package
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

__version__ = "0.0.1"

from potentiopipe.cli import (
    process_raw_cli,
    peak_detection_proc_cli,
)

from potentiopipe.data_processing import (
    process_raw,
    peak_detection_proc,
)

from potentiopipe.signal_processing import (
    peak_detection,
    slicing_ramp,
)

from potentiopipe.types import (
    ParametersPeakDetection,
)

from potentiopipe.visualization import (
    plot_potentiostat_raw,
    plot_potentiostat_proc,
)


__all__ = [
    "process_raw_cli",
    "peak_detection_proc_cli",
    "process_raw",
    "peak_detection_proc",
    "peak_detection",
    "slicing_ramp",
    "ParametersPeakDetection",
    "plot_potentiostat_raw",
    "plot_potentiostat_proc",
]
