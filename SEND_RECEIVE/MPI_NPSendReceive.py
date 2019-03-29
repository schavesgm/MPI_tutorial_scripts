from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if __name__ == '__main__':

    # In this case we do need to define the objects before
    if rank == 0:
        data = np.linspace( 0, 10, 100, dtype = 'i' )
        comm.Send( [data, MPI.INT], dest = 1, tag = 77 )

    elif rank == 1:
        recvData = np.empty( 100, dtype = 'i' )
        comm.Recv( [recvData, MPI.INT], source = 0, tag = 77 )
        print( recvData )

    # If we do not define which kind of variable we are sending
    # it is obviously much less efficient
    if rank == 0:
        mySecondData = np.arange( 10, dtype = np.float64 )
        comm.Send( mySecondData, dest = 1, tag = 13 )

    elif rank == 1:
        recvData = np.empty( 10, dtype = np.float64 )
        comm.Recv( recvData, source = 0, tag = 13 )
        print( recvData ) 
