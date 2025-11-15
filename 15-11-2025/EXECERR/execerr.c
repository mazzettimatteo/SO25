#include<stdio.h>
#include<unistd.h>
#include<errno.h>

int main(int argc, int * argv[]){	//esegui file con ./execerr ls / 
/*
	questo programma esegue il comando passato come primo argomento(ls)
	execvp ritornerà solo se cìè un errore, perché altrimenti execvp sostituisce il processo corrente
*/

	int err=execvp(argv[1],argv+1);
	printf("err=%d errno=%d \n",err,errno);//se il prog va in errore allora stampa err e errno(error Number)
	if(errno==ENOENT)
//ENOENT è il codice di errore(quindi un int) corrispondente all'errore "the filepathname does not exist"  
//per leggere tutti gli errori fai man 2 execve
		printf("non esiste\n");
	if(err==-1)
		perror("execerr");//messaggio associato a errno

}
