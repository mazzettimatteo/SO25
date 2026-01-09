#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<stdlib.h>
#include<linux/limits.h>

int main(int argc, char * argv[]){ //argv[1] sarà la directory in cui voler andare, esegui con chdir altreDir/dir[1-5]

	char path[PATH_MAX]; //array di caratteri lungo PATH_MAX byte. PATH_MAX è la lunghezza massima di un percorso in linux
	if(getcwd(path, PATH_MAX)==NULL) //getcwd per ottenere current working directory
		exit(1);
	printf("current working dir(cwd): %s\n",path); //come fare pwd
	int err=chdir(argv[1]); //chdir è la systemcall per chiamare directory ad argv[1]
	if(err==-1)
		perror("execerr");
	if(getcwd(path,PATH_MAX)==NULL)
		exit(1);
	printf("cwd: %s\n",path);	 //fai pwd su dove sei ora, quindi la nuova dir in cui ti sei spostato


}
