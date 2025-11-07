#include<stdio.h>
#include<unistd.h>
#include <sys/wait.h>

int main(){

    if(fork()){
       int status;
       pid_t stchild;
       printf("parent pid: %d \n",getpid());
       sleep(1);
       _exit(89);

    }
    else{       
       
        printf("child pid (parent pid): %d (%d)\n",getpid(),getppid());
        sleep(10);
        printf("child pid (parent pid): %d (%d)\n",getpid(),getppid());
        _exit(42);
    }
    //if parent has already ended and child has not his return value is captured by init
    //so if i child is orphan the kernell will switch his ppid to the init one which is 1, 
    //or in some cases his new pid is the pid of the shell instead 
    
    return 0;
}