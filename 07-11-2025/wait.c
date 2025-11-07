#include<stdio.h>
#include<unistd.h>
#include <sys/wait.h>

int main(){


    printf("pre %d parent %d\n",getpid(),getppid());
    if(fork()){
        int status;
        pid_t stchild;
        printf("parent pid %d\n",getpid());
        stchild=wait(&status); //Purpose: Makes the parent process wait until one of its child processes finishes.
        printf("child has terminated so now parent can continue\n");
        printf("stchild %d terminated with WEXITSTATUS(gets exit status, if all is good it should be 0): %d \n",stchild, WEXITSTATUS(status));
    }
    else{
        sleep(2);
        printf("child pid after 2 secs %d\n",getpid());
    
    }

    

    return 0;
}