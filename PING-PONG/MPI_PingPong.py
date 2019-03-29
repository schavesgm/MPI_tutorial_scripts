from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def getMovement( pFail ):
    rollNum = np.random.rand()
    if 0 <= rollNum <= pFail:
        return 'FAIL'
    else:
        return 'NICE'

if __name__ == '__main__':

    ## We will generate a ping-pong script
    ## There will be a chance to fail the ball
    
    pFail = 0.1
    pingPongCount = 0
    partner = ( rank + 1 ) % 2
    failFlag = 0

    while True:
        
        if ( rank == pingPongCount % 2 ):
            ## We use module two so we only have ranks 0 and 1 playing
            shoot = getMovement( pFail )
            print( 'Rank', rank, 'shot the ball in the touch number', pingPongCount )
            pingPongCount += 1
            if shoot == 'NICE':
                comm.send( pingPongCount, dest = partner, tag = 1 )
            else:
                print( 'Rank', rank, 'failed the ball' )
                
        
        else:
            ## Receive the ball from the previous rank
            pingPongCount = comm.recv( source = partner, tag = 1 )
            print( 'Rank', rank, 'received the ball from rank', partner )
    

    
