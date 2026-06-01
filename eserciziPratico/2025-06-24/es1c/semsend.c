#define _POSIX_C_SOURCE 199309L

#include<stdio.h>
#include<sys/types.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include<unistd.h>

/*crivere due programmi C: semsend e semrecv.
Il programma semrecv stampa il proprio pid e si pone in attesa. Il programma semsend ha due
parametri: il pid del processo semrecv e una stringa.
La stringa passata come ultimo parametro a semsend deve essere trasferita a semrecv e da
quest'ultimo stampata.
Ogni carattere della stringa (incluso il terminatore) deve essere spedito bit a bit usando i segnali
SIGUSR1 e SIGUSR2.*/
void useless(){}

int main(int argc, char * argv[]){

    if(argc!=3){
        printf("Use ./semsend <pid> <string>");
        return 1;
    }

    pid_t dest=(pid_t) atoi(argv[1]);
    char msg[1024]={0};
    snprintf(msg, sizeof(msg), "%s", argv[2]);
    int len=strlen(msg);

    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags=0;
    sa.sa_handler=useless;
    sigaction(SIGUSR1, &sa, NULL);


    for(int i=0;i<=len;i++){    //<= perché inoltro anche il terminatore
        for(int j=7; j>=0; j--){ //invio bit dal più significativo al meno
            int bit=(msg[i]>>j) & 1;
            if(bit==0) kill(dest, SIGUSR1);
            else kill(dest, SIGUSR2);

            pause();
        }
        
    }

    
    return 0;
}