#define _GNU_SOURCE

#include<stdio.h>
#include<stdlib.h>
#include <sys/timerfd.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <poll.h>
#include <signal.h>

/*Scrivere un programma timeout che esegua un programma e lo termini se supera una durata
massima prefissata. timeout ha almeno due argomenti: il primo è la durata massima in millisecondi, i
parametri dal secondo in poi sono il programma da lanciare coi rispettivi argomenti.
Es:
timeout 5000 sleep 2
temina in due secondi (sleep termina in tempo).
timeout 3000 sleep 5
passati tre secondi il programma sleep viene terminato.
Tmeout deve essere scritto usando le system call poll, pidfd_open, timerfd**/
//Test with:    ./timeout 50000 ls -la           ./timeout 1 ls -la  

int main(int argc, char * argv[]){

    if(argc<3){
        printf("Use: ./timeout <time_in_ms> <command> [command_args]");
        return 1;
        }
    int maxTime=atoi(argv[1]);

    int sonFd, timerFd;

    int sonPid=fork(); //Sdoppio l'esecuzione: padre-figlio
    if(sonPid==0){ //Processo figlio
        execvp(argv[2], &argv[2]); //Esegui comando passato come argv[2] usando come argmoneti tutto ciò che vine dopo l'argv2
    }
    else{ //Parent process
        
        //sonFd=pidfd_open(sonPid,0);
        sonFd = syscall(SYS_pidfd_open, sonPid, 0); //Gemini dice di usare questa per sicurezza: su certi kernel linux pidfd_open è troppo recente

        timerFd=timerfd_create(CLOCK_MONOTONIC,0); 
        /*I timer possono essere di più tipi, 
        REALTIME, tempo di sistema in sec/nsec da 1 gen 1970 =>Si usa quando deve attivarsi un evento come in un calendario 
        MONOTONIC, non dipende dall'orologio di sistema, è quello che nella vita di tutti giorni in effetti chiamiamo timer
        BOOTTIME, come monotonic, ma continua ad andare anche se il sistema è in standby
        */

        struct itimerspec uTimer;
        uTimer.it_value.tv_sec=maxTime/1000; //Tempo impostato nel timer in secondi
        uTimer.it_value.tv_nsec=(maxTime%1000)*1000000; //Tempo che resta dalla divisione per i secondi 

        uTimer.it_interval.tv_nsec=0; //Ogni quanto ripetere il timer: 0=>non ripeterlo
        uTimer.it_interval.tv_sec=0;

        timerfd_settime(timerFd,0,&uTimer,NULL); //Avvia il timer

        struct pollfd fds[2]; //Array per mantenere gli eventi dei filedersciptors
        fds[0].fd=timerFd;
        fds[0].events=POLLIN; //sono in lettura(IN) dall' fd di timer
        /*Usi POLLIN se vuoi sapere quando ci sono dati da leggere,
         POLLOUT se vuoi sapere quando il buffer è libero per scrivere*/

        fds[1].fd=sonFd;
        fds[1].events=POLLIN; //sono in lettura(IN) dall' fd del figlio
        
        poll(fds, 2, -1); //Attendi eventi sull' array di filedescriptors, di dim 2, resta bloccato(-1) nel mentre

        if(fds[1].revents & POLLIN){ //Tutto ok, il figlio ha terminato in tempo
            printf("The son process has ended succesfully\n");
        }
        else if(fds[0].revents & POLLIN){
            kill(sonPid, SIGKILL); //Interrompiamo il figlio killando il suo pid
            printf("The son process died because of timeout\n");
        }
         
    }

    

    return 0;
}