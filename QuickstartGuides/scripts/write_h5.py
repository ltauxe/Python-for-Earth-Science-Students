
import numpy as np
import h5py as h5py

# Define data arrays.
# They will be organized in the H5 container this way
#   root / field -> field [:]
#   root / mesh / x-coor -> x [:]
#   root / mesh / indices -> idx[:]
#   root / mesh / mesh_transform -> transform[:]

x = np.linspace(0, 1.0, 16)
idx = np.arange(16)
field = x**2 + 3.3 * x + 1.0
transform = np.arange(16)

hf = h5py.File("data.h5", "w")

g1 = hf.create_group("mesh")
g1.create_dataset("x-coor", data=x)
g1.create_dataset("indices", data=idx)

g2 = g1.create_group("mesh_transform")
g2.create_dataset("transform", data=transform)

hf.create_dataset("field", data=field)

hf.close()
