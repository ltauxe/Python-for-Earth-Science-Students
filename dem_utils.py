
import numpy as np


def get_cell_neighbors_cart(nx, ny):
  """
  Create a table of cell neighbors. 
  Neighbor cells are ordered as follows:
    west, east, south, north, north-east, south-east, south-west, north-west
  Cells which do not have a neighbor in a given direction (i.e. those along the boundary)
  are assigned an index of -1.
  
  Usage:
    Create the table
      cell_neigh = get_cell_neighbors_cart(10, 12)
      
    To access the neighbours of cell 4, do this
      neigh = cell_neigh[4, :]
      
    To access the east neighbor of cell 4, do this
      n_east = cell_neigh[4, 1]

  Parameters:
  -----------
  nx : int
    Number of cells in the i direction.
  ny : int
    Number of cells in the j direction.
    
  Output:
  -----------
  neigh_idx : ndarray, shape = (nx * ny, 8)
    Two dimensional array defining the indices of the 8 neighboring cells.
  """
  
  neigh_idx = np.zeros((nx*ny, 8), dtype=np.int64)
  neigh_idx[:, :] = -1
  
  _cells = np.arange(0, nx*ny)
  _cells = np.reshape(_cells, (ny, nx)).T
 
  west, east, south, north = 0, 1, 2, 3
  north_east, south_east, south_west, north_west = 4, 5, 6, 7
  
  ir = np.arange(0, nx)
  jr = np.arange(0, ny)

  # north
  cc = _cells[:, 0:ny-1]
  cn = _cells[:, 1:ny]
  neigh_idx[cc, north] = cn

  # east
  cc = _cells[0:nx-1, :]
  cn = _cells[1:nx, :]
  neigh_idx[cc, east] = cn

  # south
  cc = _cells[:, 1:ny]
  cn = _cells[:, 0:ny-1]
  neigh_idx[cc, south] = cn

  # west
  cc = _cells[1:nx, :]
  cn = _cells[0:nx-1,   :]
  neigh_idx[cc, west] = cn


  # north-east
  cc = _cells[0:nx-1, 0:ny-1]
  cn = _cells[1:nx,   1:ny]
  neigh_idx[cc, north_east] = cn

  # south-east
  cc = _cells[0:nx-1, 1:ny]
  cn = _cells[1:nx,   0:ny-1]
  neigh_idx[cc, south_east] = cn

  # south-west
  cc = _cells[1:nx,   1:ny]
  cn = _cells[0:nx-1, 0:ny-1]
  neigh_idx[cc, south_west] = cn

  # north-west
  cc = _cells[1:nx,   0:ny-1]
  cn = _cells[0:nx-1, 1:ny]
  neigh_idx[cc, north_west] = cn

  return neigh_idx


def determine_receiver(cell_neighbor, z):
  """
  Get the cell index which has the lowest elevation.
  Cells which have neighbors that are all higher (or equal) in elevation
  are assigned a receiver index of -1.
  
  Usage:
    Create the table of neighnors
      cell_neigh = get_cell_neighbors_cart(10, 12)
    Get the receiver cells
      cell_recv = determine_receiver(cell_neigh, z)
    The cell which is downstream of cell 4 is determined like this
      downstream_cell = cell_recv[4]
    Hence, `downstream_cell` receives it's information from cell 4.
  
  Parameters:
  -----------
  cell_neighbor : ndarray, shape(ncells, 8)
    Array of cell neighbors.
  z : ndarray, shape(ncells, )
    Array of elevations.
    
  Output:
  -----------
  min_n : ndarray(nx * ny, )
    Array defining the indices of the neighboring cell with the lowest elevation.
    
  Exceptions:
  -----------
  `ValueError` will be raised if a size mismatch is detected in any of the input arguments.
  """
  
  if cell_neighbor.ndim != 2:
    raise ValueError("cell_neighbor must have dimension 2, found " + str(cell_neighbor.ndim))
  if z.ndim != 1:
    raise ValueError("z must have dimension 1, found " + str(z.ndim))
  if cell_neighbor.shape[0] != z.shape[0]:
    raise ValueError("cell_neighbor (axis 0) must be the same size as z (axis 0)")

  ncells = z.shape[0]
  min_neighbour = np.zeros(ncells, dtype=np.int64)
  
  _nid = cell_neighbor.flatten()
  _IDX = _nid[_nid >= 0]
  _H = np.zeros(ncells * 8)
  _H[_nid >= 0] = z[_IDX]
  _H[ _nid == -1 ] = 1.0e10
  _H = np.reshape(_H, (ncells, 8))
  
  min_idx = np.argsort(_H, axis=1)
  min_n = cell_neighbor[ np.arange(len(cell_neighbor)), min_idx[:, 0]]
  
  min_n[ z <= z[min_n] ] = -1

  return min_n


def flow_accumulate(receiver, z, field=None):
  """
  Sum the values of field (or 1.0) in the downstream direction.
  If no value for field is provided, we sum the value of 1.0.
  In this case, the result of flow_accumulate() can be interpretted
  as counting the number of upstream cells + 1. 
  The +1 is incurred as we define that a cell always receive information from itself.
  
  Usage:
    Create the table of neighnors
      cell_neigh = get_cell_neighbors_cart(10, 12)
    Get the receiver cells
      cell_recv = determine_receiver(cell_neigh, z)
      acc = flow_accumulate(cell_recv, z)
    The number of cells upstream of cell 4 is then acc[4] - 1

  Parameters:
  -----------
  receiver : ndarray, shape(ncells, )
    Array of cell indices of the lowest cell neighbor.
  z : ndarray, shape(ncells, )
    Array of elevations.
  field (optional) : ndarray, shape(ncells, )
    Data to accumulate (sum) in the downstream direction.
  
  Output:
  -----------
  accumulate : ndarray(nx * ny, )
    Array defining the accumulation of field[] (or 1.0) obtained by summing
    in the downstream direction.
    
  Exceptions:
  -----------
  `ValueError` will be raised if a size mismatch is detected in any of the input arguments.
  """
  
  if receiver.ndim != 1:
    raise ValueError("receiver must have dimension 1, found " + str(receiver.ndim))
  if z.ndim != 1:
    raise ValueError("z must have dimension 1, found " + str(z.ndim))
  if field is not None and field.ndim != 1:
    raise ValueError("field must have dimension 1, found " + str(field.ndim))
  if receiver.shape[0] != z.shape[0]:
    raise ValueError("receiver (axis 0) must be the same size as z (axis 0)")
  if field is not None and field.shape[0] != z.shape[0]:
    raise ValueError("field (axis 0) must be the same size as z (axis 0)")

  ncells = z.shape[0]
  horder = np.argsort(z) # sorted from min to max
  r_horder = horder[-1::-1] # reverse the ordering

  accumulate = np.zeros(ncells)
  if field is None:
    accumulate[:] = 1.0
  else:
    accumulate[:] = field[:]
  
  for ck in range(ncells):
    c = r_horder[ck]
    av = accumulate[c]
    if receiver[c] != -1:
      accumulate[receiver[c]] += av

  return accumulate


def upstream_slope(x1d, y1d, receiver, z):
  """
  Compute the upstream slope.
  
  Parameters:
  -----------
  x1d : ndarray, shape(nx, )
    Array of 1D x coordinates.
  y1d : ndarray, shape(ny, )
    Array of 1D y coordinates.
  receiver : ndarray, shape(ncells, )
    Array of cell indices of the lowest cell neighbor.
  z : ndarray, shape(ncells, )
    Array of elevations.
  
  Output:
  -----------
  slope : ndarray(nx * ny, )
    Array defining the upstream slope.
  
  Exception:
  -----------
  `ValueError` will be raised if a size mismatch is detected in any of the input arguments.
  """

  if receiver.ndim != 1:
    raise ValueError("receiver must have dimension 1, found " + str(receiver.ndim))
  if z.ndim != 1:
    raise ValueError("z must have dimension 1, found " + str(z.ndim))

  nx = x1d.shape[0]
  ncells = z.shape[0]

  slope = np.zeros(ncells)
  cidx = np.arange(ncells, dtype=np.int64)
  r_flow = receiver != -1 # select cells to iterate on based on recv value
  cidx = cidx[r_flow] # get cells to traverse
  z_high = z[cidx]
  z_low = z[receiver[cidx]]
  jj = cidx / nx
  jj = jj.astype(np.int64) # cast to int
  ii = cidx - jj * nx
  njj = receiver[cidx] / nx
  njj = njj.astype(np.int64) # cast to int
  nii = receiver[cidx] - njj * nx
  dL = (x1d[ii] - x1d[nii])**2 + (y1d[jj] - y1d[njj])**2
  slope[cidx] = (z_high - z_low) / np.sqrt(dL)
  
  return slope


def _detect_pits(cell_neighbor, z):
  
  ncells = z.shape[0]
  pits = np.zeros(ncells, dtype=np.int64)

  for c in range(ncells):
    idx = cell_neighbor[c, :]
    nn = idx >= 0
    nh = z[idx[nn]]
    min_h_idx = np.argsort(nh)[0]
    max_h_idx = np.argsort(nh)[-1]
    _idx = idx[nn]
    min_h = z[_idx[min_h_idx] ]
    max_h = z[_idx[max_h_idx] ]
    if z[c] < min_h:
      pits[c] = 1

  return pits


def fill_pits(cell_neighbor, z):
  """
  Fills "pits" in the elevation field.
  A pit is filled by changing the cell elevation to that of the lowest neighbor cell.
  The input `z` is changed in-place.
  
  Parameters:
  -----------
  cell_neighbor : ndarray, shape(ncells, 8)
    Array of cell neighbors.
  z : ndarray, shape(ncells, )
    Array of elevations.

  Output:
  -------
    None
    
  Exceptions:
  -----------
  `ValueError` will be raised if a size mismatch is detected in any of the input arguments.
  """
  
  if cell_neighbor.ndim != 2:
    raise ValueError("cell_neighbor must have dimension 2, found " + str(cell_neighbor.ndim))
  if z.ndim != 1:
    raise ValueError("z must have dimension 1, found " + str(z.ndim))
  if cell_neighbor.shape[0] != z.shape[0]:
    raise ValueError("cell_neighbor (axis 0) must be the same size as z (axis 0)")

  ncells = z.shape[0]
  pits = _detect_pits(cell_neighbor, z)
  npits = pits.sum()
  if npits == 0:
    print('all pits filled')
    return

  max_iterations = 200
  iteration = 0
  print('[fill_pits] iteration', iteration, 'npits', npits)
  while npits != 0:
    z0 = np.copy(z)

    cellid = np.arange(0, ncells)
    _cells = pits == 1
    pit_cells = cellid[_cells]

    for c in pit_cells:
      idx = cell_neighbor[c, :]
      nn = idx >= 0
      nh = z[idx[nn]]
      min_h = 1.0e10
      for h in nh:
        if h < min_h:
          min_h = h
      z[c] = min_h

    pits = _detect_pits(cell_neighbor, z)
    npits = pits.sum()
    iteration += 1
    print('[fill_pits] iteration', iteration, 'npits', npits)

    if iteration == max_iterations:
      raise ValueError("fill_pits() executed maximum number of iterations without removing all pits")


def diffusion_equation_perform_one_step(dx, dy, kappa, T,
                                        source=None,
                                        dbc_left=None, dbc_right=None, dbc_top=None, dbc_bottom=None,
                                        dt_user=None, dt_max=1.0e20):
  """
  Performs a single time step of the time-dependent diffusion equation in 2-D, given by
    \partial T / \partial t = \div( k grad(T) ) + S
  The diffusion equation is solved using a finite difference method in space and time.
  The finite difference grid consists of nx x ny FD cells.
  The discrete solution of the finite difference problem is defined at the center of each cell.
  Each cell in the finite difference grid has a physical size of dx x dy.
  
  Dirichlet boundary conditions are specified by setting one (or more) of 
    dbc_left, dbc_right, dbc_top, dbc_bottom 
  to a value of True. These parameters define which side of the domain will have an imposed
  Dirichlet boundary condition. 
  When a Dirichlet boundary condition is specified, the value of the Dirichlet condition
  to use is taken from the input array `T` along the appropriate boundary segment.
  When a Dirichlet boundary conditon is not specified, a zero flux condition is assumed.
  It is recommended that at least one Dirichlet boundary condition must be specified.
  
  An optimal time-step will internally be computed and used if the caller does not
  provided a value for `dt_user`.
  
  Parameters:
  -----------
  dx : float
    The size of every finite difference cell in the x direction.
  dy : float
    The size of every finite difference cell in the y direction.
  kappa : ndarray, shape(nx, ny)
    The diffusivity (denoted by k in the equation above)
  T : ndarray, shape(nx, ny)
    The value of T at time t.
  source (optional): ndarray, shape(nx, ny)
    The source term (denoted by S in the equation above)
  dbc_left, dbc_right, dbc_top, dbc_bottom (all optional): Bool
    Flag to indicate whether the unknown should be fixed along a given
    side of the boundary.
  dt_user (optional) : float
    A user provided time-step to advance the solution forward by.
  dt_max (optional) : float
    The maximum allowable time-step.

  Output:
  -------
  dt : float
    Timestep used.
  T_next : ndarray, shape(nx, ny)
    Solution at the next time t + dt.
    
  Exceptions:
  -----------
  `ValueError` will be raised if a size mismatch is detected in any of the input arguments.
  """
  
  if T.ndim != 2:
    raise ValueError("T must have dimension 2, found " + str(T.ndim))
  if kappa.ndim != 2:
    raise ValueError("kappa must have dimension 2, found " + str(kappa.ndim))
  if source is not None and source.ndim != 2:
    raise ValueError("source must have dimension 2, found " + str(source.ndim))

  #if dbc_left is None and dbc_right is None:
  #  if dbc_top is None and dbc_bottom is None:
  #    raise ValueError("At least one of dbc_left, dbc_right, dbc_top, dbc_bottom must be specified")

  M, N = T.shape

  if dt_user is None:
    # Compute a stable time step
    dt = 0.25 * min(dx, dy)**2.0 / np.max(kappa)
    if dt_user is not None:
      dt = min(dt, dt_user)
  else:
    dt = dt_user

  if dt > dt_max:
    dt = dt_max

  T_next = np.copy(T)

  # Copy values associated with the boundary condition (top, bottom, left, right)
  T_b = np.copy(T[:  , 0])
  T_t = np.copy(T[:  , N-1])
  T_l = np.copy(T[0  , :])
  T_r = np.copy(T[M-1, :])
  
  # Compute the harmonic average of the diffusivity in the x direction
  kappa_x = np.zeros((M+1, N))
  for i in range(1, M):
    kappa_x[i, :] = (0.5/kappa[i, :] + 0.5/kappa[i-1, :])**(-1.0) # harmonic average
    #kappa_x[i, :] = 0.5*(kappa[i, :] + kappa[i-1, :]) # arithmetic average
  
  # Compute the harmonic average of the diffusivity in the y direction
  kappa_y = np.zeros((M, N+1))
  for j in range(1, N):
    kappa_y[:, j] = (0.5/kappa[:, j] + 0.5/kappa[:, j-1])**(-1.0)
    #kappa_y[:, j] = 0.5*(kappa[:, j] + kappa[:, j-1])
  
  # Compute the fluxes on the interior facets only [1, M-1] and [1, N-1]
  qx = np.zeros((M+1, N))
  for i in range(1, M):
    qx[i, :] = kappa_x[i, :] * (T[i, :] - T[i-1, :]) / dx
  
  qy = np.zeros((M, N+1))
  for j in range(1, N):
    qy[:, j] = kappa_y[:, j] * (T[:, j] - T[:, j-1]) / dy
  
  # Compute div of the flux
  F = np.zeros((M, N))
  for i in range(0, M):
    F[i, :] += (qx[i+1, :] - qx[i, :]) / dx
    # Ignore contribtions from east / west boundaries => q.n = 0
  
  for j in range(0, N):
    F[:, j] += (qy[:, j+1] - qy[:, j]) / dy
    # Ignore contribtions from north / south boundaries => q.n = 0

  # Perform Euler step
  if source is not None:
    
    if dt_user is None:
        dT = np.absolute(F) + np.absolute(source)
        delta_T_max = np.max(dT) # dT_max = dt . (F + S) < 0.1 * min(dx, dy)
        dt_source = 0.1 * min(dx, dy) / delta_T_max
        dt = min(dt, dt_source)

    if dt > dt_max:
      dt = dt_max

    T_next[:, :] += dt * (F[:, :] + source[:, :])

  else:
    T_next[:, :] += dt * F[:, :]
                      
  # Strongly impose Dirichlet boundary conditions on boundaries
  if dbc_bottom == True:
    T_next[:, 0] = T_b[:]
  if dbc_top == True:
    T_next[:, N-1] = T_t[:]
  if dbc_left == True:
    T_next[0, :] = T_l[:]
  if dbc_right == True:
    T_next[M-1, :] = T_r[:]

  return dt, T_next



import matplotlib.colors
from matplotlib import cm

# https://stackoverflow.com/questions/40895021/python-equivalent-for-matlabs-demcmap-elevation-appropriate-colormap
class FixPointNormalize(matplotlib.colors.Normalize):
  """
  Inspired by https://stackoverflow.com/questions/20144529/shifted-colorbar-matplotlib
  Subclassing Normalize to obtain a colormap with a fixpoint
  somewhere in the middle of the colormap.
  
  This may be useful for a `terrain` map, to set the "sea level"
  to a color in the blue/turquise range.
  """
  
  def __init__(self, vmin=None, vmax=None, sealevel=0, col_val = 0.21875, clip=False):
    # sealevel is the fix point of the colormap (in data units)
    self.sealevel = sealevel
    # col_val is the color value in the range [0,1] that should represent the sealevel.
    self.col_val = col_val
    matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)
  
  def __call__(self, value, clip=None):
    x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
    return np.ma.masked_array(np.interp(value, x, y))


# Combine the lower and upper range of the terrain colormap with a gap in the middle
# to let the coastline appear more prominently.
# inspired by https://stackoverflow.com/questions/31051488/combining-two-matplotlib-colormaps

def create_topo_cmap():
  colors_undersea = cm.terrain(np.linspace(0, 0.17, 56))
  colors_land = cm.terrain(np.linspace(0.25, 1, 200))
  # combine them and build a new colormap
  colors = np.vstack((colors_undersea, colors_land))
  cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)

  return cut_terrain_map
