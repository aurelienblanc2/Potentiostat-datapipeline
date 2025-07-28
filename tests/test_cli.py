"""
Test files for the potentiopipe package

Modules: cli

    Functions:
        process_raw_cli
        peak_detection_proc_cli
"""

import pytest
import io
import sys
import pandas as pd

###################
# - Import test - #
###################


def test_cli_import_functions():
    """Test that the cli module exposes expected functions."""
    from potentiopipe import cli

    assert hasattr(cli, "process_raw_cli")
    assert hasattr(cli, "peak_detection_proc_cli")


##################
# Functions test #
##################

# process_raw_cli


@pytest.mark.parametrize("custom_columns", [None, ["T", "V", "C", "I", "D", "R"]])
def test_cli_process_raw_cli_valid_input(monkeypatch, custom_columns):
    from potentiopipe.cli import process_raw_cli
    from potentiopipe import cli

    example_csv = "0,0.1,1.2,1,0,1\n1,0.2,1.3,1,0,1\n2,0.3,1.4,2,0,1"
    raw_stream = io.StringIO(example_csv)

    argv = ["process_raw_cli", raw_stream]
    if custom_columns:
        argv += custom_columns

    # MonkeyPatch sys.argv
    monkeypatch.setattr(sys, "argv", argv)

    def mock_process_raw(df: pd.DataFrame) -> pd.DataFrame:
        return df

    # MonkeyPatch process_raw
    monkeypatch.setattr(cli, "process_raw", mock_process_raw)

    df_result = process_raw_cli()

    assert isinstance(df_result, pd.DataFrame)
    assert df_result.shape == (3, 6)
    assert df_result.iloc[0, 2] == 1.2

    if custom_columns:
        expected_columns = custom_columns
    else:
        expected_columns = ["Time", "Voltage", "Current", "Cycle", "Dummy", "Reference"]

    assert list(df_result.columns) == expected_columns


def test_cli_process_raw_cli_invalid_input(monkeypatch):
    from potentiopipe.cli import process_raw_cli

    argv = ["process_raw_cli", "invalid_input"]

    # MonkeyPatch sys.argv
    monkeypatch.setattr(sys, "argv", argv)

    with pytest.raises(TypeError, match="Input is not a file-like object"):
        process_raw_cli()


# peak_detection_proc_cli


def test_cli_peak_detection_proc_cli_valid_input(monkeypatch):
    from potentiopipe.cli import peak_detection_proc_cli
    from potentiopipe import cli

    example_csv = "Time,Voltage,Current,Cycle,Dummy,Reference\n0,0.1,1.2,1,0,1\n1,0.2,1.3,1,0,1\n2,0.3,1.4,2,0,1"
    proc_stream = io.StringIO(example_csv)

    argv = ["peak_detection_proc_cli", proc_stream]

    # MonkeyPatch sys.argv
    monkeypatch.setattr(sys, "argv", argv)

    def mock_peak_detection_proc(df: pd.DataFrame) -> pd.DataFrame:
        return df

    # MonkeyPatch process_raw
    monkeypatch.setattr(cli, "peak_detection_proc", mock_peak_detection_proc)

    df_result = peak_detection_proc_cli()

    assert isinstance(df_result, pd.DataFrame)
    assert df_result.shape == (3, 6)
    assert df_result.iloc[0, 2] == 1.2


def test_cli_peak_detection_proc_cli_invalid_input(monkeypatch):
    from potentiopipe.cli import peak_detection_proc_cli

    argv = ["peak_detection_proc_cli", "invalid_input"]

    # MonkeyPatch sys.argv
    monkeypatch.setattr(sys, "argv", argv)

    with pytest.raises(TypeError, match="Input is not a file-like object"):
        peak_detection_proc_cli()
