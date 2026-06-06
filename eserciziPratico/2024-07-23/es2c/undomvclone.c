#include<stdio.h>
#include<string.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

/*Scrivere un programma che crei nella directory passata come arg (se non esiste già) una sottodirectory di
nome ... (tre punti).
Tutti i file (regolari) presenti nella directory devono essere spostati nella sottodirectory ... (tre punti) e
ogni file deve essere sostituito nella dir passata come arg con un link simbolico (relativo, non assoluto) alla
nuova locazione. Usare la system call rename per fare la sostituzione in modo atomico (in nessun
istante il file deve risultare inesistente)*/
/*(UNDO) Scrivere un programma che sostituisca tutti i link simbolici presenti nella
directory corrente che puntano a ... /nomefile con i veri file che l'esercizio 1 aveva spostato nella
directory tre punti. Usare la system call rename per fare la sostituzione in modo atomico (in nessun
istante il file deve risultare inesistente)*/

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use ./undomvclone <dir/> dove dir è la dir passata come arg a ./mvclone");
        return 1;
    }

    char startingDir[1024]={0};
    realpath(argv[1], startingDir);

    char cloneDir[1024]={0};
    snprintf(cloneDir, sizeof(cloneDir), "%s/...", startingDir);

    DIR * _startingDir=opendir(startingDir);
    struct dirent *dp;

    while((dp=readdir(_startingDir))!=NULL){

        if(strcmp(dp->d_name,".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath,sizeof(dpPath),"%s/%s",startingDir,dp->d_name);

        struct stat dpStat;
        lstat(dpPath, &dpStat);

        if(S_ISLNK(dpStat.st_mode)){

            char linkSrc[1024]={0};
            readlink(dpPath,linkSrc,sizeof(linkSrc)-1);
            if(strncmp(linkSrc, ".../",4)==0){ //Controllo che sia un link generato da mvclone, quindi che link qualcosa nella dir .../
                char dpNewPath[1024]={0};
                snprintf(dpNewPath,sizeof(dpNewPath),"%s/%s",cloneDir,dp->d_name);
        
                rename(dpNewPath, dpPath); 
            }

        }
        
    }
    closedir(_startingDir);

    return 0;
}