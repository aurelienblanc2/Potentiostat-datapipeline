"""
Test files for the proper package import check

    Modules:
        cli : CLI for the potentiopipe package
        data_processing : Data processing functions for the potentiostat
        signal_processing : General Signal processing functions used for data processing of the potentiostat
        types : Types Declaration for the potentiopipe package
        visualization : Visualization of the potentiostat data
"""


def test_package_import() -> None:
    """Test that the potentiopipe package can be imported."""
    import potentiopipe

    assert hasattr(potentiopipe, "__version__")
    assert isinstance(potentiopipe.__version__, str)

    assert hasattr(potentiopipe, "cli")
    assert hasattr(potentiopipe, "data_processing")
    assert hasattr(potentiopipe, "signal_processing")
    assert hasattr(potentiopipe, "types")
    assert hasattr(potentiopipe, "visualization")
