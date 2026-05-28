//Questi define servono solo per non farmi segnalare da intellisense errori che non ci sono
#define _POSIX_C_SOURCE 199309L


#include<stdio.h>
#include<stdlib.h>
#include <signal.h>
#include <string.h>
#include<sys/types.h>
#include<unistd.h>
#include <ucontext.h>

/*Dato un sistema a 64bit, scrivere due programmi C, sigtx e sigrx: sigtx deve trasferire a sigrx stringhe
di max 8 caratteri usando i valori assegnati ai segnali (il parametro value della funzione sigqueue).
Il programma sigrx deve per prima cosa stampare il proprio pid e attendere segnali.
il programma sigtx ha due parametri, il pid di sigrx e il messaggio.
es: sigtx 22255 provasig
(posto che sigrx sia in esecuzione con pid 22255, sigrx deve stampare provasig). */



void handler(int sig, siginfo_t *info, void* ucontext){

    char result[9]={0};
    memcpy(result, &(info->si_value.sival_ptr), 8);
    printf("%s\n",result);

}

int main(int argc, char * argv[]){

    printf("%d\n",getpid());

    struct sigaction s;
    s.sa_flags=SA_SIGINFO;
    s.sa_sigaction=handler;
    

    sigaction(SIGUSR1,&s,NULL);


    while(pause()!=-1){
        
    }

    return 0;
}