
import numpy as np
import netCDF4 as nc4

# Define data arrays.
# They will be organized in the H5 container this way
#   root / field -> field [:]
#   root / mesh / x-coor -> x [:]
#   root / mesh / indices -> idx[:]
#   root / mesh / mesh_transform -> transform[:]
#
#   root -> variables = (field)
#   root -> mesh -> variables = (x-coor, indices)
#   root -> mesh -> mesh_transform -> variables = (transform)


x = np.linspace(0, 1.0, 16)
idx = np.arange(16)
field = x**2 + 3.3 * x + 1.0
transform = np.arange(16)



nf = nc4.Dataset("data.nc", "w", format="NETCDF4")
nf.title = "Example NetCDF file"

# Create dimension / variable in the root
nf.createDimension("field", len(field))
nc_field = nf.createVariable("field", 'f8', "field", zlib=True)
nc_field.units = 'm/s'
nc_field[:] = field


# Create group, insert two variables
grp1 = nf.createGroup("mesh")
grp1.createDimension("x", len(x))
nc_x = grp1.createVariable("x-coor", 'f8', "x", zlib=True)
nc_x.units = 'm'
nc_x[:] = x # The "[:]" at the end of the variable instance is necessary

grp1.createDimension("idx", len(idx))
nc_idx = grp1.createVariable("indices", 'i4', "idx", zlib=True)
nc_idx.units = '-'
nc_idx[:] = idx # The "[:]" at the end of the variable instance is necessary


# Create a nested group mesh/mesh_transform
grp2 = grp1.createGroup("mesh_transform")
grp2.createDimension("tform", len(idx))
nc_transform = grp2.createVariable("transform", 'i4', "tform", zlib=True)
nc_transform.units = '-'
nc_transform[:] = transform


nf.close()
