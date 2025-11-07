#include<stdio.h>
#include<unistd.h>


int main(){

    printf("child process after fork will sleep for 2 sec.\n");
    if(fork()){
        printf("parent pid %d\n",getpid());
    }
    else{
        sleep(2);
        printf("child pid after 2 secs %d\n",getpid());
    }

    

    return 0;
}