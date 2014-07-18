__author__ = 'Kamil Koziara & Taiyeb Zahir'

import cProfile
import numpy
from utils import generate_pop, HexGrid, draw_hex_grid
from stops_ import Stops2

secretion = numpy.array([5, 6, 7])
reception = numpy.array([3, 4, 2])
receptors = numpy.array([1, -1, -1])
bound=numpy.array([1,1,1,1,1,1,1,1])

base1=numpy.array([0,0,1,0,0,0,0,0])
base2=numpy.array([0,0,0,0,0,0,0,0])


trans_mat = numpy.array([[0,-10,0,0,0,0,10,0], #notch
                         [0,0,0,0,0,1,0,0], #Delta
                         [0,1,0,0,0,0,0,0.1], #basal
                         [0.005,0,0,0,0,0,0,0], #delta receptor
                         [-10,0,0,0,0,0,0,0], #notch receptor
                         [0,0,0,0,0,0,0,0], #ligand_delta
                         [0,0,0,0,0,0,0,0], #ligand_notch
                         [0,0,0,0,0,0,0,0] #ligand_basal
                        ])

init_pop = generate_pop([(50, base1), (2450, base2)])
grid = HexGrid(50, 50, 1)

def color_fun(row):
    if row[0]==1:
        return 1
    elif row[4]==1:
        return 0.75
    elif row[1]==1:
        if row[3]==1:
            return 0.55
        else:
            return 0.3
    else:
        if row[2]==1:
            return 0.2
        else:
            return 0.

sims=1
errors_with=[]

def run():
    global errors_with
    for j in range(sims):
        entry=0 
	err=[]
        x = Stops2(trans_mat, init_pop, grid.adj_mat, bound, secretion, reception, receptors, secr_amount=6, leak=0, max_con=6, max_dist=1.5, opencl=False)
        for i in range(1300):
            x.step()
            print j,i
            if (i+1)%1300 == 0:
                draw_hex_grid("pics/with%04d.png"%j, x.pop, grid, color_fun)
                for m in range(x.pop_size):
		    if x.pop[m,4]==1:
			indices = [i for i, t in enumerate(x.adj_mat[m,:]) if t < 1.5 and t > 0]
			truth=[]
			for p in indices:
			    truth.append(x.pop[p,0]==1)
			if not any(truth):
      	    		    err.append(m)
	        print err
		for a in range(1,len(err)):
		    rtruth=[]
		    for b in range(a):
			rtruth.append(0<x.adj_mat[err[a],err[b]]<1.5)
			if not any(rtruth):
			    entry+=1
			
		errors_with.append(entry)     



cProfile.run("run()")
print errors_with





































