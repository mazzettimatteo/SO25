//Syestem call:
//funzioni come mkdir sono funzoni wrapper a systemcall.
//Tutte le systemcall restituiscono un numero itntero: se questo è positivo(o zero) la systemcall ha avuto successo, altrimenti no.

#include<stdio.h>
#include<unistd.h>
#include <sys/wait.h>

int main(){

	printf("pre %d \n",getpid());//getpid ottiene il Process identifier del processo attuale


	if(fork()){	//fork() è una systemcall che crea una forca: arrivati a questo punto il processo diventa due processi identici, entrambe le copie dei processi partono dalla chiamata della fork
	//l'unica differenza sono i valori di ritorno dei due processi: il processo padre ha valore di ritorno TRUE, il figlio FALSE
	//questi due processi sono a memoria privata
		
		//facciamo ora aspettare il padre, codice segnato con ###
		int status;//###
		pid_t stchild;//###
		
		printf("true\n");
		printf("parent %d \n",getpid());

		stchild=wait(&status);//### 
		//status mi permette di capire com'è terminato wait
		printf("%d terminated (%d)  \n",stchild,WEXITSTATUS(status));//###

	}
	else{
		//aggiungiamo un attesa di 2 sec al processo figlio
		sleep(2);
		printf("false\n");
		printf("child %d \n",getpid());
		_exit(2);//###


	}

	printf("post %d \n",getpid()); // post viene stampato due volte, una volta per ogni processo



	return 0;
}
