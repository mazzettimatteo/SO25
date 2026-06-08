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



//RECIEVER
int main(int argc, char * argv[]){

    char buf[1024]={0};
    int currSize=0;

    int len=read(STDIN_FILENO, buf, sizeof(buf));
    if(len<0) return 1;

    char * newArgv[1024];
    int argCont=0;

    newArgv[0]=&buf[0];
    argCont++;
    for(int i=1; i<len -1; i++){
        if(buf[i]=='\0'){
            newArgv[argCont]=&buf[i+1];
            argCont++;
        }
    }

    newArgv[argCont]=NULL;

    execvp(newArgv[0], newArgv);

    
    return 0;
}