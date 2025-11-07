#include<stdio.h>
#include<unistd.h>

int main(){

    if(fork()){
        printf("fork() is true with pid %d\n",getpid());
    }
    else{
        printf("fork() is false with pid %d\n",getpid());
        printf("i will now kill the else case process with _exit\n");
        _exit(89);  //89 is just the exit code, it does not have to macth with the process id
                    //_exit already knows at what process he should relate 

    }

    printf("this should only print for the parentt process which has %d as pid\n",getpid());

    return 0;
}