from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()
if __name__ == '__main__':
    
    ## Rank number 0 will have some data
    if( rank == 0 ):
        myData = [2,'Hello',3.14,'Sergio is nice']
        COMM.send( myData, dest = 1, tag = 1 )
    ## Rank number 1 will receive some data
    elif( rank == 1 ):
        myData = COMM.recv( source = 0, tag = 1 )
        print( myData, 'from rank', rank )


