#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<sys/stat.h>//libreria per stat
#include<stdlib.h>//libreria per exit

//systemcall: lstat


/*esercizio completo in 15--11-2025/LSTAT/lstat.c !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*/

int main(int argc, char *argv[]){//esegui con ./es3 file.txt per vedere le stat di file.txt	
	struct stat buf;

	int err=lstat(argv[1], &buf);
	if(err==-1){
		perror("stat");
		exit(255);
	}
	printf("nlink = %d\n",buf.st_nlink);
	printf("uid = %d\n",buf.st_uid);
	printf("gid = %d\n",buf.st_gid);
	printf("permessi = %o\n",buf.st_mode & 07777);//al posto di 07777 potevo mettere 0xfff

	switch(buf.st_mode & S_IFMT)
		case S_IFBLK: printf("");
		/*...*/ 
	
	

	return 0;
}
