#include<stdio.h>
#include<dirent.h>
#include<string.h>
#include<sys/types.h>
#include<sys/stat.h>
#include <limits.h>
#include <stdlib.h>

/*Scrivere un programma che presi come parametri i pathname di
un file f e di una directory d stampi l'elenco dei link simbolici che puntano a f presenti nel sottoalbero
del file system generato dalla directory d.*/

void recursiveSearch(char * _target, char * _dir){

    char target[1024]={0};
    realpath(_target, target);
    struct stat targetStat;
    stat(target,&targetStat);
    

    DIR * currDir=opendir(_dir);
    if(currDir==NULL) {
        printf("lelele\n");
        return;
    }
    struct dirent * dp;

    while((dp=readdir(currDir))!=NULL){
        if(strcmp(dp->d_name,".")==0 || strcmp(dp->d_name,"..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath,sizeof(dpPath),"%s/%s",_dir,dp->d_name); 

        struct stat dpStat;
        stat(dpPath, &dpStat);
        struct stat dpLStat;
        lstat(dpPath,&dpLStat);

        if(S_ISLNK(dpLStat.st_mode) && dpStat.st_ino==targetStat.st_ino) printf("%s\n",dpPath);

        if(S_ISDIR(dpStat.st_mode)) recursiveSearch(_target, dpPath);

    }
    closedir(currDir);

}

int main(int argc, char *argv[]){

    if(argc!=3){
        printf("Use: ./findsyslink <file> <dir/>");
        return 1;
    }

    recursiveSearch(argv[1], argv[2]);

    return 0;
}

