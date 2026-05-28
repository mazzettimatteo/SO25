//Questi define servono solo per non farmi segnalare da intellisense errori che non ci sono
#define _POSIX_C_SOURCE 199309L


#include<stdio.h>
#include<stdlib.h>
#include <signal.h>
#include <string.h>
#include<sys/types.h>
#include<unistd.h>
/*Dato un sistema a 64bit, scrivere due programmi C, sigtx e sigrx: sigtx deve trasferire a sigrx stringhe
di max 8 caratteri usando i valori assegnati ai segnali (il parametro value della funzione sigqueue).
Il programma sigrx deve per prima cosa stampare il proprio pid e attendere segnali.
il programma sigtx ha due parametri, il pid di sigrx e il messaggio.
es: sigtx 22255 provasig
(posto che sigrx sia in esecuzione con pid 22255, sigrx deve stampare provasig). */
/*Estendere i programmi dell'es.1 per consentire il trasferimento di stringhe di lunghezza arbitraria
(iterando il procedimento 8 caratteri alla volta e con la gestione di una conferma (ack) prima di
mandare i successivi 8 caratteri).*/



void useless(){} //Serve solo per non far terminare il programma dopo la ricezione di USRSIG2

int main(int argc, char * argv[]){
//argv[] preso in input conterrà PID e "stringa_da_inviare_8char"

    pid_t pid=(pid_t) atoi(argv[1]);
    char *str=argv[2];
    int len=strlen(str);


    struct sigaction s;
    s.sa_flags=0;
    sigemptyset(&s.sa_mask);
    s.sa_sigaction=useless; 
    sigaction(SIGUSR2,&s,NULL); 


    union sigval value;
    value.sival_int=0;
    
    
    for(int i=0;i<len;i+=8){
        value.sival_ptr=NULL;

        int fragmentSize= (len-i > 8) ? 8 : (len-i);

        memcpy(&value.sival_ptr, str+i, fragmentSize);

        sigqueue(pid, SIGUSR1, value);
        pause();
            
            
    }
    

    return 0;
}