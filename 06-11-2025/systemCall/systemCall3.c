
#include<stdio.h>
#include<unistd.h>
#include <sys/wait.h>

int main(){

	printf("pre %d \n",getpid());	

	//processo zombie da completare con appunti sul sito del prof
	//se termina il figlio e il padre non fa la wait
	if(fork()){		
		int status;
		pid_t stchild;
		
		printf("true\n");
		printf("parent %d \n",getpid());
		printf("%d terminated (%d)  \n",stchild,WEXITSTATUS(status));

	}
	else{
		sleep(2);
		printf("false\n");
		printf("child %d \n",getpid());
		_exit(2);


	}

	printf("post %d \n",getpid()); 

	return 0;
}
