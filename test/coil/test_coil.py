from coilpy import Coil
import numpy as np
from pathlib import Path
from tempfile import TemporaryDirectory


TEST_DIR = Path(__file__).resolve().parent

# read
ellipse = Coil.read_makegrid(str(TEST_DIR / "ellipse.coils"))
assert ellipse.num == 16, "Coil number is read incorrectly!"
assert len(ellipse.data[0].x) == 129, "Segment number is read incorrectly!"
assert ellipse.data[15].I == -1e6, "Coil current is read incorrectly!"
assert ellipse.data[10].group == 3, "Coil group is read incorrectly!"

# plot
ellipse.plot(irange=range(0, 16, 4))
ellipse.plot(irange=range(0, 16, 4), enginer="plotly", plot2d=True)

# save as VTK files
with TemporaryDirectory() as tmpdir:
    vtk_base = Path(tmpdir) / "ellipse"
    ellipse.toVTK(str(vtk_base))
    label = []
    for icoil in list(ellipse):
        zsign = icoil.z[:-1] > 0
        label += zsign.astype(int).tolist()
    ellipse.toVTK(
        str(vtk_base.with_suffix(".vtk")),
        line=False,
        width=0.05,
        height=0.05,
        cell_data={"z_sign": [label]},
    )

# calculate B field
b = np.array([-5.85704462e-04, 2.94453517e-03, -1.63013362e-18])
assert np.allclose(ellipse.data[0].bfield([0, 0, 0]), b)

# misc
ellipse.data[1].interpolate()
ellipse.data[1].magnify(ratio=2.0)

# save
with TemporaryDirectory() as tmpdir:
    ellipse.save_makegrid(str(Path(tmpdir) / "test.coils"))
