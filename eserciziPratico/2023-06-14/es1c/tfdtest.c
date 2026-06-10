#define _GNU_SOURCE

#include<stdio.h>
#include<stdlib.h>
#include <sys/timerfd.h>
#include<string.h>
#include <unistd.h>
#include <stdint.h>

/*facendo uso dei timerfd (vedi timerfd_create) scrivere un programma che stampi una stringa a
intervalli regolari. (il parametro ha tre campi separati da virgola: il numero di iterazioni, l'intervallo fra
iterazione e la stringa da salvare:
tfdtest 4,1.1,ciao
deve stampare ciao quattro volte, rispettivamente dopo 1.1 secondi, 2.2 secondi, 3.3 secondi 4.4
secondi e terminare. L'esecuzione dovrebbe essere simile alla seguente:
$ tfdtest 4,1.1,ciao
1.100267 ciao
2.200423 ciao
3.300143 ciao
4.400053 ciao*/

int main(int argc, char * argv[]){
    //2 metodi, o far ripartire il timer ogni volta dentro il for, oppure impostare l'interval del timer in modo che riparta da solo

    char *_times;
    char *_interval;
    char *text;

    _times=strtok(argv[1],",");
    _interval=strtok(NULL,",");
    text=strtok(NULL,",");

    //printf("%s %s %s\n", arg1,arg2,arg3);

    int times=atoi(_times);
    float interval=atof(_interval);
    int timerFd=timerfd_create(CLOCK_MONOTONIC,0);

    struct itimerspec uTimer;
    uTimer.it_value.tv_sec= (time_t) interval; //Tempo impostato nel timer in secondi
    uTimer.it_value.tv_nsec=(interval-uTimer.it_value.tv_sec)*1000000000; //Tempo che resta dalla divisione per i secondi 
    
    uTimer.it_interval.tv_nsec=0; //Ogni quanto ripetere il timer: 0=>non ripeterlo, 
    //se avessi scelto di farlo ripetere ogni interval secondi avrei dovuto porli = al campo it_value.tv_(n)sec
    uTimer.it_interval.tv_sec=0;

    

    for(int i=0;i<times;i++){

        timerfd_settime(timerFd,0,&uTimer,NULL); //Avvia il timer

        u_int64_t expiration; //parametro per endere la read bloccante
        read(timerFd,&expiration,sizeof(expiration)); 
        /*read(timerFd,NULL,0) non funziona:
        Prima di avviare tutta la logica di interazione con lo scheduler e le code di attesa appena descritta, 
        il kernel esegue dei controlli preliminari e rigorosi sui parametri passati alla system call. 
        L'implementazione di timerfd impone che il buffer di lettura sia tassativamente di almeno 8 byte.
        Avendo ricevuto NULL e una dimensione di 0, il kernel faceva fallire la read all'istante 
        restituendo l'errore EINVAL (argomento non valido). Questo causava l'uscita prematura dalla system call
        prima ancora di poter valutare se bloccare o meno il processo.
        */
        printf("------------------------------%s\n",text);
    }


    return 0;
}