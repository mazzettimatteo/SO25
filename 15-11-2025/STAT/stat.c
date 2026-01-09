#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<stdlib.h>
#include<sys/stat.h>

int main(int argc, int * argv[]){ //esegui questo file con ./stat mettendo come arg un file dal folder di prova

	struct stat buf; //variabile di tipo statche contiene campi come st_mode, uid, gi ecc.. 
						  //verrà riempita con la systemCall stat() con le informazioni su file/percorso indicato
	int err=stat(argv[1],&buf); //riempio buf chiamando stat(char * path, struct stat buf), err=codice di uscita di stat()
	if(err==-1){ //se stat ha fallito
		perror("stat"); //stampa "stat: contenuto_di_errno"
		exit(89); //termino process usando come codice di uscita 89
	}
	printf("nlink %d\n",buf.st_nlink); //stampa num link fisici al file
	printf("uid %d\n",buf.st_uid); //stampa user ID del file
	printf("gid %d\n",buf.st_gid); //stampa group ID del file
	printf("perm %o\n",buf.st_mode & 07777); 
	/*
	st_mode è un campo bitwise che coniene sia il tipo di file sia i bit di permesso e altri bit speciali.
	La maschera 07777 seleziona i 12 bit meno significativi  rilevanti per permessi e bit speciali:
	- i 3 gruppi di permessi
	- bit speciali: set-user-ID, set-group-ID, sticky bit
	07777 in ottale = 111111111111
	%o stampa il numero in ottale
	*/
	switch(buf.st_mode & S_IFMT){ //S_IFMT è una mask che indicano il tipo si file da st_mode, stampiamo che tipo di file è
		case S_IFBLK: printf("block device\n");				break;
		case S_IFCHR: printf("charachter device\n");			break;
		case S_IFDIR: printf("directory\n");					break;
		case S_IFIFO: printf("FIFO/pipe\n");					break;
		case S_IFLNK: printf("symbolic link(soft)\n");		break;
		case S_IFREG: printf("regular file\n");				break;
		case S_IFSOCK: printf("socket\n");						break;
		default:		  printf("unknown \n");						break;
	}

}
