from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()

def matMult( partA, B ):
    rows_A = partA.shape[0]
    cols_A = partA.shape[1]
    rows_B = B.shape[0]
    cols_B = B.shape[1]

    # Create the result matrix
    # Dimensions would be rows_A x cols_B
    C = np.zeros( [rows_A, cols_B], dtype = 'i' )

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                pass
                C[i,j] += partA[i,k] * B[k,j]
    return C

if __name__ == '__main__':
    
    ## Each rank must have a copy of each second matrix
    ## and several lines the first matrix

    B = np.array( [ [10,2,3], [1,1,4] ] )
    divMat, rows, cols = None, None, None

    A = None
    if( rank == 0 ):
        A = np.array( [ [1,3], [2,5], [3,2] ], dtype = 'i' )
        divMat = int( A.shape[0] / size )
        rows = A.shape[0]
        cols = A.shape[1]
    
    divMat = COMM.bcast( divMat, root = 0 )
    rows = COMM.bcast( rows, root = 0 )
    cols = COMM.bcast( cols, root = 0 )
    
    ## Now let's scatter the data
    recvA = np.empty( [divMat, cols], dtype = 'i' )
    COMM.Scatter( A, recvA, root = 0 )
    COMM.Barrier()
    
    partMult = matMult( recvA, B )

    ## Gather the data into rank number 0
    getValues = None
    if( rank == 0 ):
        getValues = np.empty( [rows, B.shape[1]], dtype = 'i' )
    
    COMM.Gather( partMult, getValues, root = 0 )

    if( rank == 0 ):
        print( 'Python' )
        print( A @ B )
        print( 'Our creation' )
        print( getValues )





    
