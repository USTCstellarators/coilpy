Overview
========

CoilPy is a plasma-physics utility library focused on stellarator data processing,
coil geometry, equilibrium post-processing, and visualization.

Highlights
----------

- Read and manipulate coil sets, surfaces, VMEC outputs, BOOZ_XFORM data, and STELLOPT results.
- Evaluate magnetic fields from discrete coils with both Python and Fortran-backed routines.
- Export geometry and field data for visualization workflows such as VTK and Plotly.
- Work with dipoles, current-potential results, and mesh-based magnetic design utilities.

Main modules
------------

- ``coilpy.coils``: Coil geometry, interpolation, magnetic-field evaluation, plotting, and export helpers.
- ``coilpy.surface``: Fourier surface representation and related geometry tools.
- ``coilpy.vmec`` and ``coilpy.booz_xform``: Equilibrium and Boozer-coordinate post-processing.
- ``coilpy.stellopt`` and ``coilpy.current_potential``: Optimization output readers and design utilities.
- ``coilpy.misc``: Shared numerical helpers used across the package.
