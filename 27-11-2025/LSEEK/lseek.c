//foto con segno ARANCIONE

#include<stdio.h>
#include<unistd.h>
#include<fcntl.h>

#define BUFSIZE 128

int main(int argc, char *argv[] ){	//esegui con ./mycp fileDaCopiare fileNuovo
	//man 2 read
	//man 2 open
	//man 2 colse	
	int fdin=open(argv[1], O_RDONLY);
	int fdout= open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0666);
	
	unsigned char buf[BUFSIZE];
	ssize_t n;
	
	while((n=read(fdin, buf, BUFSIZE))>0)
		write(fdout, buf, n);

	close(fdin);
	close(fdout);

}


