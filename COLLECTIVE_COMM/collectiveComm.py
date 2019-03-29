from mpi4py import MPI

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()
size = COMM.Get_size()

if __name__ == '__main__':
    
    ## BROADCAST DATA -- EVERYONE GETS THE SAME COPY

    ## Rank number 0 will have some data
    if( rank == 0 ):
        myData = [2,'Hello',3.14,'Sergio is nice']
    else:   
        myData = None       ## It is a good practice to declare the variable

    ## Let's see the data before broadcasting it
    # print( myData )

    ## Now let's broadcast it 
    myData = COMM.bcast( myData, root = 0 )
    # print( myData )


    ## SCATTER DATA -- WE SEND A PORTION OF AN ARRAY TO EACH RANK

    ## Rank number 0 will have some initial data
    ## which we will use to calculate the average
    if( rank == 0 ):
        mySamples = [ 1, 2, 3, 4, 1, 2, 3, 3, 2, 3, 1, 2, 3, 1 ]
        
        ## We have to split it
        div = int( len( mySamples ) / size )
        
        scatArray = []
        for i in range( size ):
            scatArray.append( mySamples[i*div:div*(i+1)] ) 

        ## Take into account the rest
        if( div * size != len( mySamples ) ):
            for i in range( div * size, len(mySamples) ):
                scatArray[0].append( mySamples[i] )

    else:
        scatArray = []

    scatArray = COMM.scatter( scatArray, root = 0 )
    print( 'Rank', rank, 'data', scatArray )
    COMM.barrier()

    ## Now lets calculate the sum at each rank
    partAverage = 0
    for i in range( len(scatArray) ):
        partAverage += scatArray[i]

    print( 'Rank', rank, 'sum of average', partAverage, len( scatArray ) )
    COMM.barrier()

    ## And of course, gather the result at master rank
    partAverage = COMM.gather( partAverage, root = 0 )
    
    ## We just sum the data obtained
    if( rank == 0 ):
        print( 'The result is', sum( partAverage ) / len( mySamples ) )







