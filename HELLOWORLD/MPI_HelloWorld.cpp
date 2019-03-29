#include <iostream>
#include "mpi.h"

int main( ) {
    
    // Initialize the MPI environment
    MPI_Init( NULL, NULL );     // You can use different communicators,
                                // I have some lack of knowdlegde on it.
    
    // Get the number of processes/workers
    int size;
    MPI_Comm_size( MPI_COMM_WORLD, &size ); // We fill the memory with the size of communicator
    // The size is a constant value for all the workers/processors

    // Get the rank of each processor - label/name of each processor
    int rank;
    MPI_Comm_rank( MPI_COMM_WORLD, &rank ); // We fill the memory with the rank of each process
    // The rank of each process is independent and unique 
    
    // NOT NEEDED: We can get the name of each processor, maybe nice for debugging
    char name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name( name, &name_len );
    
    // GENERATE THE HELLO WORLD
    
    std::cout << "Hey amigo, my name is " << name << " and my label is " << rank << 
                 ". I salute you one time out of " << size << std::endl;
    
    if( rank == 0 ) { 
        std::cout << "I am the master of all these kids, therefore I salute you twice from " <<
                     "rank number " << rank << std::endl;
    }
    
    if( rank == 1 ) {
        std::cout << "Psst, I salute you twice from rank number " << rank << std::endl;
    // IMPORTANT : We need to finalize the MPI enviroment
    MPI_Finalize();

return 0;
}
