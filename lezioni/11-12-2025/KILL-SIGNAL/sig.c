
#include<stdio.h>
#include<unistd.h>
#include<signal.h>
#include<stdlib.h>

void handler(int signo){
	printf("sig %d\n",signo);
}


int main(int argc, char * argv[]){
	printf("pid %d\n",getpid());
	signal(SIGUSR1, handler);
	for(int i=0;;i++){
		printf("waiting %d\n",i);
		sleep(1);
	}


}
