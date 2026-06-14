#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <fcntl.h>
#include <string.h>

/* AGGIUNTA: Funzione handler che viene eseguita quando il processo riceve SIGUSR1 */
void handler(int sig){
    printf("SUCCESSO! Ho ricevuto il segnale %d (SIGUSR1)\n", sig);
}

int main(int argc, char *argv[]){

    if(argc != 2){
        printf("Use: ./prova <fifo_path>\n");
        return 1;
    }

    /* AGGIUNTA: Registriamo l'handler per SIGUSR1 prima di eseguire altre operazioni, 
       altrimenti il processo verrebbe terminato di default alla ricezione del segnale. */
    signal(SIGUSR1, handler);

    pid_t myPid = getpid();

    /* AGGIUNTA: Creiamo un buffer di caratteri e usiamo snprintf per formattare la stringa 
       esattamente come richiesto. Questo sostituisce itoa (che non è standard C) 
       e l'intera logica della execvp. */
    char buffer[256];
    snprintf(buffer, sizeof(buffer), "%d %d\n", myPid, SIGUSR1);

    /* AGGIUNTA: Apriamo la FIFO direttamente in sola scrittura */
    int fd = open(argv[1], O_WRONLY);
    if(fd == -1){
        printf("Errore nell'apertura della FIFO\n");
        return 1;
    }

    /* AGGIUNTA: Scriviamo la stringa formattata nel file descriptor della FIFO */
    write(fd, buffer, strlen(buffer));
    close(fd);

    printf("Inviato alla FIFO: %sMi metto in attesa del segnale...\n", buffer);

    /* AGGIUNTA: pause() sospende l'esecuzione del processo finché non riceve un segnale. 
       In questo modo il programma non termina prima che fifosig abbia il tempo di rispondergli. */
    pause();

    return 0;
}