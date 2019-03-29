from mpi4py import MPI

## Generate the communicator
COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()

if __name__ == '__main__':

    print( "I salute you from rank number", rank, "out of", size )

    if( rank == 0 ):
        print( "I am again the master of these kids, therefore I salute you twice",\
               "from rank number", rank )

    if( rank == 1 ):
        print( "Tsss, the master is stupid, I also salute you. Don't let him know." )
