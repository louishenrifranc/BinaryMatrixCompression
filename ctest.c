#include <stdio.h>
#include <stdlib.h>



void matmul(const int8_t* X, const double* W, const size_t nb_in, const size_t nb_out, const size_t nb_hidden, double* Y) {
    // Check if parallelism work
   freopen("test.out","w",stdout);
   {
        int i;
        #pragma omp parallel for private(i)
        for(i = 0;i < nb_in*nb_hidden;i++){
            printf("%d ",X[i]);
        }
        printf("\n");
        #pragma omp parallel for private(i)
        for(i = 0;i < nb_out*nb_hidden;i++){
            printf("%lf ",W[i]);
        }
        printf("\n");
        #pragma omp parallel for private(i)
        for(i = 0;i < nb_in*nb_out;i++){
            printf("%lf ",Y[i]);
        }
        printf("\n");
   }

}