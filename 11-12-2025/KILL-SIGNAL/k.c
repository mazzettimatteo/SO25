#include<stdio.h>
#include<unistd.h>
#include<signal.h>
#include<stdlib.h>

void usr1hand(int signo){
	printf("sig %d\n",signo);
}


int main(int argc, char * argv[]){ //esegui con ./k <pid di sig.c> <numero> dopo aver eseguito ./sig

	pid_t pid=atoi(argv[1]);
	int sig = atoi(argv[2]);

	int rv = kill(pid,sig);
	if(rv<0) perror("pid");


}
