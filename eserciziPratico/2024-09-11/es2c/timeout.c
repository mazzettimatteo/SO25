#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <sys/timerfd.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <poll.h>
#include <signal.h>
#include <sys/wait.h>
#include <stdint.h> // Necessario per uint64_t utilizzato dalla read del timer

/*Scrivere un programma timeout che esegua un programma e lo termini se supera una durata
massima prefissata. timeout ha almeno due argomenti: il primo è la durata massima in millisecondi, i
parametri dal secondo in poi sono il programma da lanciare coi rispettivi argomenti.

Estendere l'esercizio 1 per fare in modo che se prima del timeout il programma termina con un errore,
al termine del timeout il programma venga riattivato.*/

int main(int argc, char * argv[]){

    if(argc < 3){
        printf("Use: ./timeout <time_in_ms> <command> [command_args]\n");
        return 1;
    }
    
    int maxTime = atoi(argv[1]);

    // Configurazione del timer
    int timerFd = timerfd_create(CLOCK_MONOTONIC, 0); 
    struct itimerspec uTimer;
    uTimer.it_value.tv_sec = maxTime / 1000;
    uTimer.it_value.tv_nsec = (maxTime % 1000) * 1000000; 
    uTimer.it_interval.tv_sec = 0; 
    uTimer.it_interval.tv_nsec = 0;

    int sonPid = fork(); 
    if(sonPid == 0){ // Processo figlio
        execvp(argv[2], &argv[2]);
        // Se execvp fallisce (es. il comando non esiste), forziamo l'uscita con errore
        exit(1); 
    }
    
    // Processo padre
    int sonFd = syscall(SYS_pidfd_open, sonPid, 0);

    // Avvio del timer
    timerfd_settime(timerFd, 0, &uTimer, NULL); 

    // Configurazione della struct per la poll
    struct pollfd fds[2]; 
    fds[0].fd = timerFd;
    fds[0].events = POLLIN; 
    fds[1].fd = sonFd;
    fds[1].events = POLLIN; 
    
    int restartPending = 0; // Flag di stato per il supervisore

    // Loop principale di monitoraggio
    while(1){
        poll(fds, 2, -1); 

        // 1. EVENTO TIMER: Il tempo a disposizione è scaduto
        if(fds[0].revents & POLLIN){
            
            // Consuma i byte generati dal timer per resettare l'evento ed evitare loop infiniti
            uint64_t expirations;
            read(timerFd, &expirations, sizeof(uint64_t));

            if(restartPending == 0){
                // Nessun errore pregresso: il figlio ha esaurito il tempo e va interrotto
                kill(sonPid, SIGKILL); 
                printf("The son process died because of timeout\n");
                break; // Uscita dal programma supervisore
            }
            else {
                // Il figlio è andato in errore precedentemente. Scaduto il timeout, lo riavviamo.
                printf("The son process gave an error, so it's being re-run after the timeout\n");
                
                // Nuova esecuzione
                sonPid = fork();
                if(sonPid == 0){
                    execvp(argv[2], &argv[2]);
                    exit(1);
                }
                
                // Aggiornamento dei file descriptor del padre per monitorare il nuovo figlio
                close(sonFd); 
                sonFd = syscall(SYS_pidfd_open, sonPid, 0);
                
                fds[1].fd = sonFd; // Riattiva l'ascolto per il nuovo processo
                restartPending = 0; // Reset del flag
                
                // Riavvolgimento e riattivazione del timer per il nuovo processo
                timerfd_settime(timerFd, 0, &uTimer, NULL);
            }
        }
        
        // 2. EVENTO FIGLIO: Il processo ha terminato l'esecuzione
        if(fds[1].revents & POLLIN){ 
            int status;
            waitpid(sonPid, &status, 0); // Lettura dello stato di uscita del figlio
            
            if(WIFEXITED(status) && WEXITSTATUS(status) == 0){
                // Terminazione corretta prima della scadenza del timer
                printf("The son process has ended successfully\n");
                break; // Uscita dal programma supervisore
            }
            else {
                // Terminazione anomala o codice di errore restituito
                printf("The son process encountered an error before timeout.\n");
                restartPending = 1; // Imposta il flag per il riavvio
                
                // Fondamentale: impedisce alla poll di ascoltare ulteriormente un processo morto
                fds[1].fd = -1;     
            }
        }
    }

    // Pulizia finale
    close(timerFd);
    if(sonFd != -1) close(sonFd);

    return 0;
}