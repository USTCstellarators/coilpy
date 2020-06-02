"""
This is a cutomized python package for plotting and data processing in stellarator optimization.

how to use:

"""
"""
# some dependant libraries
from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab # to overrid plt.mlab
import warnings
import sys
from pyevtk.hl import gridToVTK, pointsToVTK
import pandas as pd
"""

# local packages
from .misc import colorbar, get_figure, kwargs2dict, map_matrix, print_progress, toroidal_period, vmecMN, xy2rp
from .hdf5 import HDF5
from .surface import FourSurf
from .dipole import Dipole
from .focushdf5 import FOCUSHDF5
from .coils import Coil, SingleCoil
from .stellopt import STELLout, VMECout


