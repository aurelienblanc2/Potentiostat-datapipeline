# Potentiostat Driver - pyBEEP

Welcome to **potentiopipe** – a Python library for processing and plotting potentiostat data

This driver is designed to be used alongside the following:
- Potentiostat [**firmware**](https://github.com/aurelienblanc2/Potentiostat-firmware)
- Potentiostat python package driver [**pyBEEP**](https://github.com/aurelienblanc2/Potentiostat-driver-pyBEEP)

If you’d like to share or explore all three related repositories together, here is a [**link**](https://github.com/stars/aurelienblanc2/lists/potentiostat)

Below, an image of the Potentiostat device:
![Potentiostat](docs/Potentiostat.png)

---

# Overview

potentiopipe provides:
- Digital filtering
- Voltage ramp slicing to decompose measurement cycles
- Peak Detection
- Optional plotting and data visualization

---

# Main Functionalities

section in progress

---

# Installation

Clone this repository and install using pip:

```bash
git clone https://github.com/aurelienblanc2/Potentiostat-datapipeline
cd pyBEEP
pip install .
```

---

# Example of use

```python
in progress
```

---

# File Structure

```
Potentiostat-datapipeline/
├── project.toml                 # Project configuration
├── README.md                    # This file
├── docs                         # Folder for the ressources used by the README.md
├── LICENSE                      # MIT
├── requirements.txt             # Python dependencies
├── uv.lock                      # Lockfile used by UV for reproducible builds
├── .pre-commit-config.yaml      # Pre-commit configuration for developing this package
│
├── examples/                    # Example scripts for running datapipeline
│   ├── example1.py
│   ├── example2.py
│   └── data
│
├── src/
│   └── potentiopipe/
│       ├── __init__.py
│       ├── cli.py               # Command Line Interface
│       ├── data_processing.py   # Data processing functions
│       ├── signal_processing.py # General Signal processing functions
│       ├── types.py             # Types Declaration
│       └── visualization.py     # Data plotting utilities
│
└── tests/
    ├── test_init.py             # Test files for the proper package import check
    └── test_potentiopipe        # Unit test for the package modules
```

---

# Bugs & Support

If you encounter a bug, have a feature request, or need help:
- contact: aurelien.blanc@utoronto.ca

---

# Contributing

Contributions are very welcome!  
If you’d like to add features, fix bugs, or improve documentation, please submit a merge request or open an issue to discuss your ideas.

---

# License

MIT License

# Author

Aurelien Blanc - aurelien.blanc@utoronto.ca

---
