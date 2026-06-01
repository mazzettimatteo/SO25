#define _POSIX_C_SOURCE 199309L

#include<stdio.h>
#include<sys/types.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include<unistd.h>
#include <ucontext.h>

/*crivere due programmi C: semsend e semrecv.
Il programma semrecv stampa il proprio pid e si pone in attesa. Il programma semsend ha due
parametri: il pid del processo semrecv e una stringa.
La stringa passata come ultimo parametro a semsend deve essere trasferita a semrecv e da
quest'ultimo stampata.
Ogni carattere della stringa (incluso il terminatore) deve essere spedito bit a bit usando i segnali
SIGUSR1 e SIGUSR2.*/

int cont=0;
char currChar=0;

void handler(int sig, siginfo_t *info, void* ucontext){
    currChar=currChar<<1;
    if(sig==SIGUSR2) currChar = currChar | 1 ; //Se ho inviato un 1
    cont++;

    if(cont==8) {
        //printf("%c", currChar);
        write(STDOUT_FILENO,&currChar,1);
        cont=0;
        if(currChar=='\0')  write(STDOUT_FILENO,"\n",1);  //printf("\n");
        currChar=0;
    }


    pid_t sender=info->si_pid;
    kill(sender, SIGUSR1); //invio Ack
}


int main(int argc, char * argv[]){

    pid_t myPid=getpid();
    printf("%d\n", myPid);

    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags=SA_SIGINFO;
    sa.sa_sigaction=handler;

    sigaction(SIGUSR1,&sa,NULL);
    sigaction(SIGUSR2,&sa,NULL);

    while(1){
        pause();
    }


    return 0;
}