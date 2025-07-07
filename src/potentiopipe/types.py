"""
Types Declaration for the potentiopipe package

Structures:
    ParametersPeakDetection (namedtuple)
"""


###############
# - IMPORTS - #
###############

# Libraries
from collections import namedtuple


##############################
# - STRUCTURES DECLARATION - #
##############################

# Defining the Named tuple for the parameters of the peak detection
ParametersPeakDetection = namedtuple(
    "ParametersPeakDetection",
    [
        "half_width_min",
        "width_max",
        "derivation_width",
        "derivation_sensitivity",
    ],
)
ParametersPeakDetection.__doc__ = """
    Description:
        Parameters for the peak detection
    
    Attributes:
        half_width_min (type: float) : Minimum half width of the peak to be detected (in unit of X)
        width_max (type: float) : Maximum width of the peak to be detected (in unit of X)
        derivation_width (type: float) : Horizon on which the derivation is performed (in unit of X)
        derivation_sensitivity (type: float) : Sensitivity of the derivation for the detection, minimum height variation
            of Y in span of HalfWidthMin of X (unit Y/X)
"""
