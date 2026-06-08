#include<stdio.h>
#include<string.h>
#include<unistd.h>

/*Scrivere un programma argsend che converta i parametri del programma (da argv[1] in poi) in una
unica sequenza di caratteri: vengono concatenati i parametri (compreso il terminatore della stringa).
Esempio di funzionamento:
$ ./argsend ls -l /tmp | od -c
0000000 l s \0 - l \0 / t m p \0
0000013
Scrivere un secondo programma argrecv che preso in input l'output di argsend esegua il comando
con gli argomenti passati a argsend. Per esempio:
$ ./argsend ls -l /tmp | ./argrecv
total 8988
-rw-r--r-- 1 renzo renzo 150532 Jan 9 16:57 ....
.....*/

//SENDER
int main(int argc, char * argv[]){

    int currSize=0;

    char buf[1024]={0};
    for(int i=1;i<argc;i++){
        for(int j=0; j<strlen(argv[i])+1;j++){ //+1 perché altrimenti esclude il terminatore
            buf[currSize]=argv[i][j];
            currSize++;
        }
    }

    write(STDOUT_FILENO, buf, currSize); //Non si può usare printf perché quella termina appena incontra il primo "\0"


    return 0;
}