#include<stdio.h>
#include<unistd.h>
#include <sys/wait.h>

int main(){


    printf("pre %d parent %d\n",getpid(),getppid());
    if(fork()){
       int status;
       pid_t stchild;
       sleep(30);//parent process sleeps for 30 secs but his childe terminates quickly so it becomes a zombie
       printf("parent pid: %d \n",getpid());
       stchild=wait(&status);//after this operation is done the zombie process can actually die
       printf("%d terminated (%d) \n", stchild, WEXITSTATUS(status));

    }
    else{       
        printf("child pid who will get killed: %d\n",getpid());
        _exit(42);
        //a zombie process is a process who, even if he has terminated his execution, still has i PID 
        //that PID is needed by the parent so he can read the child(zombie) process exit output
    }

    printf("post %d",getpid());    
    //to check whether a process is a zombie you can open another terminal and run ps -el | grep Z
    return 0;
}