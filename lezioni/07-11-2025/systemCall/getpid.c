#include<stdio.h>
#include<unistd.h>

int main(){

    printf("getpid previous to fork: %d \n",getpid());

    if(fork()){
        printf("getpid when fork is true: PARENT %d \n",getpid());
    }
    else{
        printf("getpid when fork is false: CHILD %d \n",getpid());
    }

    printf("getpid after fork: %d \n",getpid());


    return 0;
}