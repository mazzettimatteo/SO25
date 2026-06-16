#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>

/*Scrivere un programma C rilancia: che esegua il programma indicato in argv[1] con i relativi parametri
(in argv[2] e seguenti):
es: rilancia tr a-z A-Z
esegue il comando tr coi parametri.
Se il programma lanciato termina senza errori (non per colpa di un segnale e con valore di ritorno 0)
rilancia deve rieseguire il programma (nell'esempio tr) con i medesimi parametri.*/

int main(int argc, char * argv[]){

    int notKilled;
    int retValue=0;
    int negIfNotCmd;

    while(retValue==0){
        int status;
        int son1=fork();
        if(son1==0){
            negIfNotCmd=execvp(argv[1], &argv[1]); 
            if(negIfNotCmd==-1) return 1; 
        }
        else{
            waitpid(son1,&status,0);
            notKilled=WIFEXITED(status);
            if(notKilled) retValue=WEXITSTATUS(status);
            else break;
        }
    }


    return 0;
}