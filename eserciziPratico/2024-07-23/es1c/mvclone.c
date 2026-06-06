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

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use ./undomvclone <dir/>");
        return 1;
    }

    char startingDir[1024]={0};
    realpath(argv[1], startingDir);

    char cloneDir[1024]={0};
    snprintf(cloneDir, sizeof(cloneDir), "%s/...", startingDir);
    mkdir(cloneDir,S_IRWXU);

    DIR * _startingDir=opendir(startingDir);
    struct dirent *dp;

    while((dp=readdir(_startingDir))!=NULL){

        if(strcmp(dp->d_name,".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath,sizeof(dpPath),"%s/%s",startingDir,dp->d_name);

        struct stat dpStat;
        lstat(dpPath, &dpStat);

        if(S_ISREG(dpStat.st_mode)){

            char dpNewPath[1024]={0};
            snprintf(dpNewPath,sizeof(dpNewPath),"%s/%s",cloneDir,dp->d_name);
            char dpNewRelPath[1024]={0};
            snprintf(dpNewRelPath,sizeof(dpNewRelPath),".../%s",dp->d_name); //Perché la consegna vuole che la dir passata sia path relativo

            link(dpPath,dpNewRelPath); //Così ho hardlink sia nella dir corrente che nella nuova

            char tempPath[1024]={0};
            snprintf(tempPath, sizeof(tempPath), "%s.temp",dpPath); 

            symlink(dpNewPath, tempPath); //Creo link del nuovo file nella dir attuale con nome temp

            rename(tempPath, dpPath); //sovrascrivo tempPath con nome vero

        }
        
    }
    closedir(_startingDir);

    return 0;
}