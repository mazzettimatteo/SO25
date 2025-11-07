#include<stdio.h>
#include<unistd.h>

int main(){

    if(fork()){
        printf("fork() is true \n");
    }
    else{
        printf("fork() is false \n");
    }


    return 0;
}