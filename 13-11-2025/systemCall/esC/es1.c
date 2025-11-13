#include<stdio.h>
#include<unistd.h>

#include<errno.h>

int main(int argc, char *argv[]){//argc = num parametri, arcv=vettorre dei parametri
	int err=execvp(argv[1],argv+1);	//execvp ha come parametri il comando da lanciare e l'array degli argomenti
	//sto usando l'aritmetica dei puntatori: se chiamo da shell es1 ls / in pratica faccio ls
	//se faccio argv+1 scalo il vettore. In pratica lancio ciò che gli ho passato come parametro. 

	printf("l'errore err = %d\n",err); //se i parametri sono errati stampo questo

	//come faccioa capire qual è l'errore preciso? uso la libreria errno
	printf("errno=%d\n",errno);
	
	//per avvisare l'utente
	if(err==-1)
		perror("execerr");

	return 0;
}
