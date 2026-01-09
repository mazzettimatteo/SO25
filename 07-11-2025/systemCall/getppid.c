#include<stdio.h>
#include<unistd.h>

int main(){

    printf("getpid previous to fork: %d \n",getpid());

    if(fork()){
        printf("getpid when fork is true: %d \n",getpid());
        printf("getppid when fork is true: %d \n",getppid());
    }
    else{
        printf("getpid when fork is false: %d \n",getpid());
        printf("getppid when fork is false: %d \n",getppid());
    }

    printf("getpid after fork: %d \n",getpid());
    printf("getppid after fork: %d \n",getppid());


    return 0;
}