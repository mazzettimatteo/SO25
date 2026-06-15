#include<stdio.h>
#include<sys/wait.h>
#include<string.h>
#include<unistd.h>
#include<stdlib.h>
#include<fcntl.h>

/*Scrivere il programma stdin2pipe che prenda in input due righe di testo, ogni riga contiene un
comando coi rispettivi parametri. Il programma deve lanciare entrambi i comandi in modo tale
l'output del primo diventi input del secondo.
Per esempio, dato il file cmds:
ls -l
awk '{print $1}'
l'esecuzione di:
stdin2pipe < cmds
sia equivalente al comando:
ls -l | awk '{print $1}'*/


//IO ALL'ESAME SE ESCE UN ES SIMILE: ●█▀█▄⊂==8 *inculato*



int main(int argc, char * argv[]){
    //Gli imput presi con < da shell vengono inseriti non nell'argv ma nel file descriptor 0,
    //ossia quello di questo programma qui, quindi se leggo con read devo usare fd=0, 
    //atrimenti leggo con fgets dallo stdin

    char cmd1[1024]={0};
    char cmd2[1024]={0};

    fgets(cmd1, sizeof(cmd1),stdin); //Mi struttura l'input così: "testo \n altro_testo"
    fgets(cmd2, sizeof(cmd2),stdin);


    char *args1[1024];
    int i=0;
    args1[i]=strtok(cmd1," \n");

    while(args1[i]!=NULL){
        i++;
        args1[i]=strtok(NULL, " \n");
    }


    char *args2[1024];
    int j=0;
    args2[j]=strtok(cmd2," \n");
    while(args2[j]!=NULL){
        j++;
        args2[j]=strtok(NULL, " \n");
    }
    


    int p[2]; //scrivo in p1 e leggo in p0
    if(pipe(p)<0) return 1;

    int sonPid=fork();

    if(sonPid==0){ 
        dup2(p[1],1); //duplica il fd, quello vecchio è p[1], quello nuovo è il secondo arg, in queso caso 1
        //Quindi dopo dup2 il file descriptor 1 punterà al file descriptor p[1] 
        //siccome fd=1 è lo stdout e execvp eredita la tabella dei file descriptor allora lo stdout di execvp sarà la pipe(in entrata)
        close(p[0]);
        close(p[1]);
        execvp(args1[0],args1); //
    }
    else{
        int secondSon=fork();
        if(secondSon==0){
            dup2(p[0],0); //0 è il fd che corrisponde allo stdin,
            // così sto dicendo che il nuovo stdin sarà l'uscita della pipe
            close(p[0]);
            close(p[1]);
            execvp(args2[0],args2);//siccome execvp eredita i fd l'input di execvp sarà l'output della pipe, ossia il comando precedente
        }
        else{
            close(p[0]);
            close(p[1]);

            waitpid(sonPid,NULL,0);
            waitpid(secondSon,NULL,0);
        }

    }


    return 0;
}