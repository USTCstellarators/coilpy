from .hdf5 import HDF5
from .misc import get_figure, map_matrix
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


class FOCUSHDF5(HDF5):
    """FOCUS output hdf5 file"""

    # initialization, test = FOCUSHDF5('focus_test.h5')
    def __init__(self, filename, periodic=False, **kwargs):
        """Initialization

        Keyword arguments:
            filenmae -- string, path and name to FOCUS output hdf5 file,
                        usually in the format of 'focus_*.h5'
            periodic -- logical, map all 2D surface data automatically,
                        (default: True)
        """
        # read data
        super().__init__(filename)
        # print version
        try:
            abc = ""
            for i in self.version:
                abc += i.decode("utf-8")
            self.version = abc
            print("FOCUS version: " + self.version)
        except AttributeError:
            print(filename + " is not a valid FOCUS output. Please check.")
            raise
        # add additional colume and row for plotting
        if periodic:
            self.xsurf = map_matrix(self.xsurf)
            self.ysurf = map_matrix(self.ysurf)
            self.zsurf = map_matrix(self.zsurf)
            self.nx = map_matrix(self.nx)
            self.ny = map_matrix(self.ny)
            self.nz = map_matrix(self.nz)
            self.nn = map_matrix(self.nn)
            self.Bx = map_matrix(self.Bx)
            self.By = map_matrix(self.By)
            self.Bz = map_matrix(self.Bz)
            self.Bn = map_matrix(self.Bn)
            self.plas_Bn = map_matrix(self.plas_Bn)
        return

    # convergence plot
    def convergence(self, term="bnorm", iteration=True, axes=None, **kwargs):
        # get figure
        fig, axes = get_figure(axes)
        # set default plotting parameters
        kwargs["linewidth"] = kwargs.get("linewidth", 2.5)  # line width
        # kwargs['marker'] = kwargs.get('marker', 'o') # extent
        # get iteration data
        if iteration:
            abscissa = 1 + np.arange(self.iout)
            _xlabel = "iteration"
        else:
            abscissa = self.evolution[0, :]  # be careful; DF is not saving wall-time
            _xlabel = "wall time [Second]"
        # plot data
        if term.lower() == "chi":
            data = self.evolution[1, :]
            kwargs["label"] = kwargs.get("label", r"$\chi^2$")  # line label
        elif term.lower() == "gradient":
            data = self.evolution[2, :]
            kwargs["label"] = kwargs.get(
                "label", r"$|d \chi^2 / d {\bf X}|$"
            )  # line label
        elif term.lower() == "bnorm":
            data = self.evolution[3, :]
            kwargs["label"] = kwargs.get("label", r"$f_{B_n}$")  # line label
        elif term.lower() == "bharm":
            data = self.evolution[4, :]
            kwargs["label"] = kwargs.get("label", r"$f_{B_{mn}}$")  # line label
        elif term.lower() == "tflux":
            data = self.evolution[5, :]
            kwargs["label"] = kwargs.get("label", r"$f_{\Psi}$")  # line label
        elif term.lower() == "ttlen":
            data = self.evolution[6, :]
            kwargs["label"] = kwargs.get("label", r"$f_L$")  # line label
        elif term.lower() == "cssep":
            data = self.evolution[7, :]
            kwargs["label"] = kwargs.get("label", r"$f_{CS}$")  # line label
        elif term.lower() == "curv":
            data = self.evolution[8, :]
            kwargs["label"] = kwargs.get("label", r"$f_{curv}$")  # line label
        elif term.lower() == "all":
            lines = []
            lines.append(
                self.convergence(
                    term="chi",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-",
                    color="k",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="gradient",
                    iteration=iteration,
                    axes=axes,
                    linestyle="--",
                    color="k",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="bnorm",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-.",
                    color="r",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="tflux",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-.",
                    color="g",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="bharm",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-.",
                    color="b",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="ttlen",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-.",
                    color="c",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="cssep",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-.",
                    color="m",
                    **kwargs
                )
            )
            lines.append(
                self.convergence(
                    term="curv",
                    iteration=iteration,
                    axes=axes,
                    linestyle="-.",
                    color="y",
                    **kwargs
                )
            )
            # fig.legend(loc='upper right', frameon=False, ncol=2, prop={'size':16})
            plt.legend()
            return lines
        else:
            raise ValueError("unsupported option for term")
        line = axes.semilogy(abscissa, data, **kwargs)
        axes.tick_params(axis="both", which="major", labelsize=15)
        axes.set_xlabel(_xlabel, fontsize=15)
        axes.set_ylabel("cost functions", fontsize=15)
        # fig.legend(loc='upper right', frameon=False, prop={'size':24, 'weight':'bold'})
        plt.legend()
        return line

    # poincare plot
    def poincare_plot(self, color=None, prange="full", **kwargs):
        """Poincare plot from FOCUS output.
        Args:
             color (matplotlib color, or None): dot colors. Defaults to None (rainbow).
             prange (str, optional): Plot range, one of ["upper", "lower", "all"]. Defaults to "full".
             kwargs : matplotlib scatter keyword arguments

        Returns:
             None
        """
        import matplotlib.pyplot as plt
        from matplotlib import cm

        # get figure and ax data
        if plt.get_fignums():
            fig = plt.gcf()
            ax = plt.gca()
        else:
            fig, ax = plt.subplots()

        # get colors
        if color is None:
            colors = cm.rainbow(np.linspace(1, 0, self.pp_ns))
        else:
            colors = [color] * self.pp_ns
        kwargs["s"] = kwargs.get("s", 0.1)  # dotsize
        # scatter plot
        for i in range(self.pp_ns):
            # determine whether plot upper or lower
            if prange == "upper":
                cond = self.ppz[:, i] > 0
            elif prange == "lower":
                cond = self.ppz[:, i] < 0
            else:
                cond = np.ones_like(self.ppz[:, i], dtype=bool)
            ax.scatter(
                self.ppr[:, i][cond], self.ppz[:, i][cond], color=colors[i], **kwargs
            )
        plt.axis("equal")
        plt.xlabel("R [m]", fontsize=20)
        plt.ylabel("Z [m]", fontsize=20)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        return

    # Bnorm plot
    def Bnorm(self, plottype="2D", source="all", axes=None, flip=False, **kwargs):
        """Plot Bn distribution.

        Keyword arguments:
            plottype -- string, '2D' (default) or '3D', determine the plottype
            source -- string, 'coil', 'plasma', 'sum' or 'all' (default), data source
            axes  -- matplotlib.pyplot or mayavi.mlab axis, axis to be
                     plotted on  (default None)
            flip -- logical, determine how to calculate Bn from coil,
                    True: coil_Bn = Bn - plas_Bn; False: coil_Bn = Bn + plas_Bn

        Returns:
           obj -- matplotlib.pyplot or mayavi.mlab plotting object
        """
        obj = []
        # check coil_Bn
        if flip:
            coil_Bn = self.Bn - self.plas_Bn
        else:
            coil_Bn = self.Bn + self.plas_Bn
        # 2D plots
        if plottype.lower() == "2d":
            # prepare coordinates
            ntheta = self.Nteta
            nzeta = self.Nzeta
            nt, nz = self.Bn.shape
            if self.IsSymmetric == 0:
                zeta_end = 2 * np.pi
            elif self.IsSymmetric == 1:
                zeta_end = 2 * np.pi / self.Nfp
            elif self.IsSymmetric == 2:
                zeta_end = np.pi / self.Nfp
            else:
                raise ValueError("Something wrong with IsSymmetric.")

            def theta(x, pos):
                return "{:3.2f}".format(np.pi / ntheta + x * (2 * np.pi) / ntheta)

            def zeta(x, pos):
                return "{:3.2f}".format(0.5 * zeta_end / nzeta + x * zeta_end / nzeta)

            theta_format = FuncFormatter(theta)
            zeta_format = FuncFormatter(zeta)
            # planar plotting
            if source.lower() == "all":
                fig, axes = get_figure(axes, ncols=3, sharex=True)
                axes = np.atleast_1d(axes)
                # kwargs['aspect'] = kwargs.get('aspect', nt/(2.0*nz*self.Nfp))
                kwargs["aspect"] = kwargs.get("aspect", "auto")
            else:
                fig, axes = get_figure(axes)
                axes = np.atleast_1d(axes)
                kwargs["aspect"] = kwargs.get("aspect", float(nt / nz))
            # prepare axes
            for ax in axes:
                ax.xaxis.set_major_formatter(zeta_format)
                ax.yaxis.set_major_formatter(theta_format)
            # set default plotting parameters
            kwargs["cmap"] = kwargs.get("cmap", "RdBu_r")  # colormap
            kwargs["origin"] = kwargs.get("origin", "lower")  # number of contours
            kwargs["extent"] = kwargs.get("extent", [0, nt, 0, nz])  # extent
            plt.subplots_adjust(hspace=0.05)
            # imshow
            if source.lower() == "coil":
                obj.append(axes[0].imshow(np.transpose(coil_Bn), **kwargs))
                axes[0].set_title("Bn from coils", fontsize=15)
                axes[0].set_ylabel(r"$\theta$", fontsize=14)
                axes[0].set_xlabel(r"$\phi$", fontsize=14)
            elif source.lower() == "plasma":
                obj.append(axes[0].imshow(np.transpose(self.plas_Bn), **kwargs))
                axes[0].set_title("Bn from plasma", fontsize=15)
                axes[0].set_ylabel(r"$\theta$", fontsize=14)
                axes[0].set_xlabel(r"$\phi$", fontsize=14)
            elif source.lower() == "sum":
                obj.append(axes[0].imshow(np.transpose(self.Bn), **kwargs))
                axes[0].set_title("Residual Bn", fontsize=15)
                axes[0].set_ylabel(r"$\theta$", fontsize=14)
                axes[0].set_xlabel(r"$\phi$", fontsize=14)
            elif source.lower() == "all":
                vmin = np.min([self.plas_Bn, self.Bn, coil_Bn])
                vmax = np.max([self.plas_Bn, self.Bn, coil_Bn])
                obj.append(
                    axes[0].imshow(
                        np.transpose(self.plas_Bn), vmin=vmin, vmax=vmax, **kwargs
                    )
                )
                # plt.setp(axes[0].get_xticklabels(), visible=False)
                axes[1].set_title(
                    "Bn from plasma (left), coil (mid), overall(right).", fontsize=14
                )
                obj.append(
                    axes[1].imshow(
                        np.transpose(coil_Bn), vmin=vmin, vmax=vmax, **kwargs
                    )
                )
                # axes[1].set_title('Bn from coils', fontsize=15)
                plt.setp(axes[1].get_yticklabels(), visible=False)
                obj.append(
                    axes[2].imshow(
                        np.transpose(self.Bn), vmin=vmin, vmax=vmax, **kwargs
                    )
                )
                plt.setp(axes[2].get_yticklabels(), visible=False)
                # axes[2].set_title('Residual Bn', fontsize=15)
                axes[0].set_ylabel(r"$\theta$", fontsize=14)
                # axes[1].set_ylabel(r'$\theta$', fontsize=14)
                # axes[2].set_ylabel(r'$\theta$', fontsize=14)
                axes[0].set_xlabel(r"$\phi$", fontsize=14)
                axes[1].set_xlabel(r"$\phi$", fontsize=14)
                axes[2].set_xlabel(r"$\phi$", fontsize=14)
            else:
                raise ValueError("unsupported option for source")
            fig.subplots_adjust(right=0.85)
            cbar_ax = fig.add_axes([0.86, 0.10, 0.04, 0.8])
            fig.colorbar(obj[0], cax=cbar_ax)
        return obj

    # Bmod plot
    def Bmod(self):
        return

    def plot(
        self, engine="plotly", scalars="bn", fig=None, ax=None, show=True, **kwargs
    ):
        """Plot 3D field on the plasma from FOCUS ouput

        Args:
            engine (str, optional): 3D plot engine, one of ["mayavi", "pyplot", "plotly"]. Defaults to "plotly".
            scalars (str, optional): Scalar function on the surface, one of ["Bn", "B", "plas_Bn"] or 2D arrays. Defaults to "bn".
            fig (, optional): Figure to be plotted on. Defaults to None.
            ax (, optional): Axis to be plotted on. Defaults to None.
            show (bool, optional): If show the plotly figure immediately. Defaults to True.
            kwargs: optional keyword arguments for plotting.
        Raises:
            ValueError: Plot engine should be one value of ["mayavi", "pyplot", "plotly"].
        """
        full = True if self.IsSymmetric == 0 else False
        xsurf = map_matrix(self.xsurf, first=full)
        ysurf = map_matrix(self.ysurf, first=full)
        zsurf = map_matrix(self.zsurf, first=full)
        label = "plasma"
        if scalars.lower() == "bn":
            scalars = self.Bn
            label = "Bn"
        elif scalars.lower() == "plas_bn":
            scalars = self.plas_Bn
            label = "Bn_plasma"
        elif scalars.lower() == "b":
            scalars = np.sqrt(self.Bx ** 2 + self.By ** 2 + self.Bz ** 2)
            label = "|B|"
        scalars = map_matrix(scalars, first=full)
        if engine == "pyplot":
            import matplotlib.pyplot as plt

            # plot in matplotlib.pyplot
            if ax is None or ax.name != "3d":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection="3d")
            kwargs.setdefault("cmap", "coolwarm")
            ax.plot_surface(xsurf, ysurf, zsurf, c=scalars, **kwargs)
            ax.set_title(label)
            fig.colorbar()
        elif engine == "mayavi":
            # plot 3D surface in mayavi.mlab
            from mayavi import mlab  # to overrid plt.mlab

            kwargs.setdefault("colormap", "coolwarm")
            mlab.mesh(xsurf, ysurf, zsurf, scalars=scalars, **kwargs)
            mlab.colorbar(title=label)
        elif engine == "plotly":
            import plotly.graph_objects as go

            kwargs.setdefault("colorbar", go.surface.ColorBar(title=label))
            if fig is None:
                fig = go.Figure()
            fig.add_trace(
                go.Surface(x=xsurf, y=ysurf, z=zsurf, surfacecolor=scalars, **kwargs)
            )
            fig.update_layout(scene_aspectmode="data")
            if show:
                fig.show()
        else:
            raise ValueError("Invalid engine option {pyplot, mayavi, noplot}")

    # write vtk
    def toVTK(self, name=None, full=False, **kwargs):
        """Save surface and magnetic field data into VTK file
        Arguments:
          name -- string, VTK file name. default: None, if None, using self.filename
          full -- boolean, if save the entire torus
          **kwargs -- external data will be saved in VTK file

        Return:
          VTK file name
        """
        from pyevtk.hl import gridToVTK

        # automatically get a file name, focus_*.h5 -> vtk_*
        if name is None:
            name = self.filename[:-3].replace("focus_", "vtk_")
        xx = self.xsurf
        yy = self.ysurf
        zz = self.zsurf
        Bx = self.Bx
        By = self.By
        Bz = self.Bz
        Bn = self.Bn
        plas_Bn = self.plas_Bn
        toroidal = full
        xx = np.atleast_3d(map_matrix(xx, first=toroidal))
        yy = np.atleast_3d(map_matrix(yy, first=toroidal))
        zz = np.atleast_3d(map_matrix(zz, first=toroidal))
        Bn = np.atleast_3d(map_matrix(Bn, first=toroidal))
        plas_Bn = np.atleast_3d(map_matrix(plas_Bn, first=toroidal))
        B = (
            np.atleast_3d(map_matrix(Bx, first=toroidal)),
            np.atleast_3d(map_matrix(By, first=toroidal)),
            np.atleast_3d(map_matrix(Bz, first=toroidal)),
        )
        if full:
            pass
        data = {"Bn": Bn, "plas_Bn": plas_Bn, "B": B}
        data.update(kwargs)
        return gridToVTK(name, xx, yy, zz, pointData=data)

    def curvature(
        self,
        iteration=True,
        vlines=True,
        shift_ind=0,
        axes=None,
        icoil=1,
        NS=128,
        **kwargs
    ):
        """Curvature ploting for the FOCUS-spline paper [arXiv:2107.02123] by N. Lonigro

        Args:
            iteration (bool, optional): [description]. Defaults to True.
            vlines (bool, optional): [description]. Defaults to True.
            shift_ind (int, optional): [description]. Defaults to 0.
            axes ([type], optional): [description]. Defaults to None.
            icoil (int, optional): [description]. Defaults to 1.
            NS (int, optional): [description]. Defaults to 128.

        Returns:
            [type]: [description]
        """
        import math

        # get figure
        max_ind = -1
        min_ind = -1
        fig, axes = get_figure(axes)
        # set default plotting parameters
        kwargs["linewidth"] = kwargs.get("linewidth", 2.5)  # line width
        # kwargs['marker'] = kwargs.get('marker', 'o') # extent
        # get iteration data
        if iteration:
            abscissa = np.arange(NS)
            _xlabel = "Segment number"
        else:
            abscissa = self.evolution[0, :]  # be careful; DF is not saving wall-time
            _xlabel = "wall time [Second]"
        # plot data
        data = object.__getattribute__(self, "curvature_{:}".format(icoil))
        data_s = object.__getattribute__(self, "straight_{:}".format(icoil))

        if (data_s[0] == 0) and (data_s[NS - 1] != 0) and (data_s[k + 1] == 0):
            max_ind = 0
        if (data_s[0] == 0) and (data_s[1] != 0) and (data_s[k - 1] == 0):
            min_ind = 0
        if (data_s[NS - 1] == 0) and (data_s[NS - 2] != 0) and (data_s[0] == 0):
            max_ind = NS - 1
        if (data_s[NS - 1] == 0) and (data_s[0] != 0) and (data_s[NS - 2] == 0):
            min_ind = NS - 1
        for k in range(1, len(data_s) - 2):
            if (data_s[k] == 0) and (data_s[k - 1] != 0) and (data_s[k + 1] == 0):
                max_ind = np.max([max_ind, k])
            if (
                (data_s[k] == 0)
                and (data_s[k + 1] != 0)
                and (data_s[k - 1] == 0)
                and min_ind != -1
            ):
                min_ind = np.min([min_ind, k])
            if (
                (data_s[k] == 0)
                and (data_s[k + 1] != 0)
                and (data_s[k - 1] == 0)
                and min_ind == -1
            ):
                min_ind = k
        if max_ind > min_ind and shift_ind == 0:
            shift_ind = math.floor(0.5 * (NS - max_ind - min_ind))
        if max_ind < min_ind and shift_ind == 0:
            shift_ind = math.floor(0.5 * NS + 0.5 * (NS - max_ind - min_ind))
        lines = []
        data = np.concatenate((data[-shift_ind:], data[:-shift_ind]))
        kwargs["label"] = kwargs.get("label", r"$curvature$")
        lines.append(axes.plot(abscissa, data, **kwargs))
        if max_ind > min_ind and vlines:
            lines.append(
                plt.vlines(
                    math.floor(0.5 * (NS - max_ind + min_ind)),
                    0,
                    np.max(data),
                    colors="black",
                    linestyles="dashed",
                    linewidth=5.0,
                )
            )
            lines.append(
                plt.vlines(
                    math.floor(0.5 * (NS + max_ind - min_ind)),
                    0,
                    np.max(data),
                    colors="black",
                    linestyles="dashed",
                    linewidth=5.0,
                )
            )
        if max_ind < min_ind and vlines:
            lines.append(
                plt.vlines(
                    math.floor(0.5 * (NS - max_ind - NS + min_ind)),
                    0,
                    np.max(data),
                    colors="black",
                    linestyles="dashed",
                    linewidth=5.0,
                )
            )
            lines.append(
                plt.vlines(
                    math.floor(0.5 * (NS + max_ind + NS - min_ind)),
                    0,
                    np.max(data),
                    colors="black",
                    linestyles="dashed",
                    linewidth=5.0,
                )
            )
        axes.tick_params(axis="both", which="major", labelsize=15)
        axes.set_xlabel(_xlabel, fontsize=15)
        axes.set_ylabel("curvature", fontsize=15)
        axes.set_title("Curvature of coil " + str(icoil))
        # fig.legend(loc='upper right', frameon=False, prop={'size':24, 'weight':'bold'})
        plt.legend()
        return [shift_ind, max_ind - min_ind]
