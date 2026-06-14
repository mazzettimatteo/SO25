#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<string.h>
#include<unistd.h>

/*Scrivere un programma fifotext che:
* crei una named pipe (FIFO) al pathname indicato come primo (e unico) argomento.
* apra la named pipe in lettura
* stampi ogni riga di testo ricevuta
* se la named pipe viene chiusa la riapra
* se riceve la riga "FINE" termini cancellando la named pipe.
Esempio:
fifotext /tmp/ff
....
se in un altra shell si fornisce il comando: "echo ciao > /tmp/ff", fifotext stampa ciao e rimane in attesa
(questo esperimento si può provare più volte). Con il comando "echo FINE > /tmp/ff" fifotext termina.*/

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use: ./fifotext <fifo_path>");
        return 1;
    }

    mkfifo(argv[1],0644);

    int fd=open(argv[1],O_RDONLY);
    if(fd==-1) return 1;

    while(1){

        char input[1024];
        int len=read(fd,input,sizeof(input));
        if(len<0) return 1;
        else if(len==0){
            //La FIFO è stata chiusa dallo scrittore
            close(fd);
            fd=open(argv[1],O_RDONLY);
            continue;
        }
        else{
            input[len]='\0'; //read non mette il terminatore di stringa

            if(strcmp(input,"FINE\n")==0){ // Uso "FINE\n" perché usando echo lo \n viene inserito autoaticamente 
                close(fd);
                remove(argv[1]);
                break;
            }

            printf("%s\n",input);

        }

    }


    return 0;
}