from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()

if __name__ == '__main__':
    
    ## BROADCAST DATA -- EVERYONE GETS THE SAME COPY

    ## Rank number 0 will have some Numpy object
    if( rank == 0 ):
        npData = np.linspace( 0, 25, 10, dtype = 'f' )
    else:   
        npData = np.empty( 10, dtype = 'f' )

    ## Now let's Numpy broadcast it
    COMM.Bcast( npData, root = 0 )
    COMM.Barrier()
    # print( npData )

    ### SCATTER DATA -- WE SEND A PORTION OF AN ARRAY TO EACH RANK
    
    ## Declare the Numpy object globally
    npSamples = None
    
    ## Micro-bootstrap model

    numBoot = 1e5
    numData = 1000

    contData = np.empty( 2 * size )

    for i in range( 2 ):

        if( rank == 0 ):
            ## We would like 25 items per rank
            npSamples = np.empty( [size, numData], dtype = 'f' )
            npSamples[:,:] = np.random.rand( size, numData )
        
        rcvSamples = np.empty( numData, dtype = 'f' )
        COMM.Scatter( npSamples, rcvSamples, root = 0 )

        ## Calculate the mean value of your samples at each rank
        meanVal = np.mean( rcvSamples )

        ## Gather all the mean values inside the master rank
        getMean = None
        if( rank == 0 ):
            getMean = np.empty( size, dtype = 'f' )
        COMM.Gather( meanVal, getMean, root = 0 )
        
        ## Store these means into a container
        if( rank == 0 ):
            contData[i*size:size*(i+1)] = getMean[:]
    
    if( rank == 0 ):
        print( 'Value obtained', np.mean( contData ), '+-', np.std( contData ) )
    


