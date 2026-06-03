#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>



/*Scrivere un programma ckfile che dati il pathname di un file f e di una directory d stampi, a seconda
di una opzione:
• l'elenco dei link simbolici che puntano a f presenti nel sottoalbero del file system generato
dalla directory d, (opzione -s),
ckfile -s /tmp/file /tmp
• l'elenco dei link fisici di f presenti nel sottoalbero del file system generato dalla directory d
(opzione -l),
ckfile -l /tmp/file /tmp   */

void recursiveSearch(char *_dir, char *_target, int calledWithS){
    char target[1024]={0};
    realpath(_target, target);

    struct stat targetStat;
    stat(target,&targetStat);
        
    DIR * currDir=opendir(_dir);
    struct dirent *dp;
    if(currDir==NULL) {printf("lelele\n");
        return;}

    while((dp=readdir(currDir))!=NULL){
        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char query[1024]={0};
        snprintf(query,sizeof(query),"%s/%s",_dir,dp->d_name);

        struct stat queryLStat;
        lstat(query,&queryLStat);

        struct stat queryStat;
        stat(query,&queryStat);


        if(calledWithS==1 && S_ISLNK(queryLStat.st_mode)!=0 && queryStat.st_ino==targetStat.st_ino){
            printf("%s\n",query);
        }
        else if(calledWithS==0 && S_ISLNK(queryLStat.st_mode)==0 && queryLStat.st_ino==targetStat.st_ino){
            printf("%s\n",query);
        }

        if(S_ISDIR(queryStat.st_mode)) recursiveSearch(query,_target,calledWithS);
    }
    closedir(currDir);
}


int main(int argc, char * argv[]){

    if(argc!=4){
        printf("Use \nckfile -s /tmp/file /tmp \nckfile -l /tmp/file /tmp\n");
        return 1;
    }

    int calledWithS;
    if(strcmp(argv[1],"-s")==0) calledWithS=1;
    else  calledWithS=0;

    recursiveSearch(argv[2], argv[3], calledWithS);

    return 0;
}