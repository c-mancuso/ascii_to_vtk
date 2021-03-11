#!/bin/python3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Convert XYZ Ascii to Rectinlinear VTK
Assumes min node closest to origin is cell value (last rows discarded)
Written in Python 3.8.5
By Chris Mancuso
March 08 2021

IN:		file.asc
		-Comma delimited
		-Formatted as x, y, z, scalar (e.g. Cloud Compare Output)
		-1 row of Header Values
		
OUT:	file.vtk

USAGE:	From Unix command line
		Uses positional args in order:
		 filename num-x num-y num-z attribute
		Example:
		 python3 asc_to_vtk-cell.py file.asc num_x num_y num_z attribute > file.vtk
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
import numpy as np

fname=sys.argv[1]
x_pt,y_pt,z_pt=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
attribute=sys.argv[5]

header=1		#to discard - can add to args later
delimiter=','	#can add to args later

ascii_in=np.genfromtxt(fname, delimiter=delimiter, dtype=[('x', '<f8'),
 ('y', '<f8'), ('z', '<f8'), ('d', '<f8')])[header:]
 
ascii_in.sort(order=["z", "y", "x"], kind='merge')
n_pts=ascii_in.shape[0]

x=ascii_in[ascii_in['y']==np.min(ascii_in['y'])]
x=x[x['z']==np.min(ascii_in['z'])]

y=ascii_in[ascii_in['z']==np.min(ascii_in['z'])]
y=y[y['x']==np.min(ascii_in['x'])]

z=ascii_in[ascii_in['y']==np.min(ascii_in['y'])]
z=z[z['x']==np.min(ascii_in['x'])]

n_cells=(x_pt-1)*(y_pt-1)*(z_pt-1)

print('# vtk DataFile Version 3.1',flush=True)
print(str(fname)+attribute,flush=True)
print('ASCII',flush=True)
print('DATASET RECTILINEAR_GRID',flush=True)
print('DIMENSIONS ' + str(x_pt) +' '+ str(y_pt) +' '+ str(z_pt))
print('X_COORDINATES '+ str(x_pt) + ' float',flush=True)
np.savetxt(sys.stdout.buffer, x['x'], newline=' ', fmt='%i')
print('\nY_COORDINATES '+ str(y_pt) + ' float',flush=True)
np.savetxt(sys.stdout.buffer, y['y'], newline=' ', fmt='%i')
print('\nZ_COORDINATES '+ str(z_pt) + ' float',flush=True)
np.savetxt(sys.stdout.buffer, z['z'], newline=' ', fmt='%i')

cells=np.reshape(ascii_in['d'],(z_pt,y_pt,x_pt))
cells=cells[:z_pt-1,:y_pt-1,:x_pt-1].reshape(n_cells)

print('\nCELL_DATA '+str(n_cells), flush=True)

print('SCALARS Cell_'+attribute +' FLOAT',flush=True)
print('LOOKUP_TABLE default',flush=True)
np.savetxt(sys.stdout.buffer, cells.T, fmt='%.3f')
