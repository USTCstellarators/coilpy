project('coilpy', 'c', version : '0.4.2',  meson_version: '>= 0.64.0',
)

add_languages('fortran', native: false)

fortran_compiler = meson.get_compiler('fortran')

f90flags = []
if fortran_compiler.get_id() == 'g95'
    f90flags += '-ffree-line-length-none'
endif

f90flags += '-O3'

biotsavart = files('coilpy/fortran/biotsavart.f90')

py3 = import('python').find_installation(pure: false)
py3_dep = py3.dependency()

incdir_numpy = run_command(
    py3, '-c',
    'import numpy; print(numpy.get_include())',
    check: true,
).stdout().strip()

inc_np = include_directories(incdir_numpy)

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

# Share this object across multiple modules.
fortranobject_lib = static_library('_fortranobject',
  fortranobject_c,
  dependencies: py3_dep,
  include_directories: [inc_np, inc_f2py],
)
fortranobject_dep = declare_dependency(
  link_with: fortranobject_lib,
  include_directories: [inc_np, inc_f2py],
)


f2py = [py3, '-m', 'numpy.f2py', '@INPUT@', '--build-dir', '@OUTDIR@']



translated = custom_target('coilpy_fortran',
  input : biotsavart,
  output: 'coilpy_fortranmodule.c',
  command : [py3, '-m', 'numpy.f2py', '@INPUT@', '-m', 'coilpy_fortran'],
  install : true,
  install_dir : py3.get_install_dir()
)

py3.extension_module('coilpy_fortran', 
                     biotsavart, translated,
                     dependencies: fortranobject_dep,
                     install: true)

py3.install_sources(
            'coilpy/booz_xform.py',
            'coilpy/coils.py',
            'coilpy/current_potential.py',
            'coilpy/dipole.py',
            'coilpy/focushdf5.py',
            'coilpy/hdf5.py',
            'coilpy/__init__.py',
            'coilpy/magnet.py',
            'coilpy/magtense_interface.py',
            'coilpy/mgrid.py',
            'coilpy/misc.py',
            'coilpy/netcdf.py',
            'coilpy/pm4stell.py',
            'coilpy/sortedDict.py',
            'coilpy/stellopt.py',
            'coilpy/surface.py',
            'coilpy/vmec.py',
            subdir: 'coilpy', 
)







