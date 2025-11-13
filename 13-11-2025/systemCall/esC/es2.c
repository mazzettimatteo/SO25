#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<sys/stat.h>//libreria per stat
#include<stdlib.h>//libreria per exit

//systemcall: stat

int main(int argc, char *argv[]){//esegui con ./es2 file.txt per vedere le stat di file.txt	
	struct stat buf;

	int err=stat(argv[1], &buf);
	if(err==-1){
		perror("stat");
		exit(255);
	}
	printf("nlink = %d\n",buf.st_nlink);
	printf("uid = %d\n",buf.st_uid);
	printf("gid = %d\n",buf.st_gid);
	printf("permessi = %o\n",buf.st_mode & 07777);
	
	

	return 0;
}
