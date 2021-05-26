from mpi4py import MPI
import numpy as np
import numba as nb

@nb.jit(nopython=True)
def nb_sum(x):
    sum = 0
    for i in x:
        sum += i
    return sum

def psum(x):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank==0:
        data = np.array_split(x,size)
    else:
        data = None

    data = comm.scatter(data,root=0)
    local_sum = nb_sum(data)
    all_sum = comm.reduce(local_sum,root=0,op=MPI.SUM)

    if rank==0:
        return all_sum
    else:
        return rank