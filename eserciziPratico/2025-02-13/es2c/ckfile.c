#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include<fcntl.h>
#include <dirent.h>
#include <unistd.h>


/*Scrivere un programma ckfile che dati il pathname di un file f e di una directory d stampi, a seconda
di una opzione:
• l'elenco dei link simbolici che puntano a f presenti nel sottoalbero del file system generato
dalla directory d, (opzione -s),
ckfile -s /tmp/file /tmp
• l'elenco dei link fisici di f presenti nel sottoalbero del file system generato dalla directory d
(opzione -l),
ckfile -l /tmp/file /tmp   */

/*estendere il programma dell'esercizio 1 con ulteriori opzioni per stampare:
• l'elenco dei file che hanno lo stesso contenuto di f presenti nel sottoalbero del file system
generato dalla directory d (privo di opzione)
ckfile /tmp/file /tmp
• l'elenco dei file presenti nel sottoalbero del file system generato dalla directory d che hanno
come contenuto la parte iniziale del file f (opzione -p seguita dalla lunghezza del prefisso
comune).
ckfile -p 100 /tmp/file /tmp
stampa l'elenco dei file che coincidono nei primi 100 byte con f,*/

void recursiveSearch(char *_dir, char *_target, char calledWith){
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


        if(calledWith=='s' && S_ISLNK(queryLStat.st_mode)!=0 && queryStat.st_ino==targetStat.st_ino){
            printf("%s\n",query);
        }
        else if(calledWith=='l' && S_ISLNK(queryLStat.st_mode)==0 && queryLStat.st_ino==targetStat.st_ino){
            printf("%s\n",query);
        }

        if(S_ISDIR(queryStat.st_mode)) recursiveSearch(query,_target,calledWith);
    }
    closedir(currDir);
}

void recursiveSearchP(char *_dir, char *_target, int sizeToSearch){
    char target[1024]={0};
    realpath(_target, target);

    struct stat targetStat;
    stat(target,&targetStat);

    char targetContent[sizeToSearch];

    int targetFd=open(target, O_RDONLY);
    if(targetFd==-1) return;    
    size_t targetRead=read(targetFd, targetContent, sizeof(targetContent));
    close(targetFd);
    if(targetRead!=sizeToSearch) return;

    DIR * currDir=opendir(_dir);
    struct dirent *dp;
    if(currDir==NULL) {printf("lelele\n");
        return;}

    while((dp=readdir(currDir))!=NULL){
        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;
        

        char query[1024]={0};
        snprintf(query,sizeof(query),"%s/%s",_dir,dp->d_name);

        struct stat queryStat;
        stat(query,&queryStat);

        char queryContent[sizeToSearch];

        int fd=open(query, O_RDONLY);
        if(fd==-1) continue;     
                
        size_t queryRead=read(fd, queryContent, sizeof(queryContent));
        if(queryRead==sizeToSearch){
            if(memcmp(queryContent, targetContent,sizeToSearch)==0) printf("%s\n",query);
        }

        if(S_ISDIR(queryStat.st_mode)) recursiveSearchP(query,_target,sizeToSearch);

        close(fd);
    }
    closedir(currDir);
}



void recursiveSearchAll(char *_dir, char *_target){
    char target[1024]={0};
    realpath(_target, target);

    struct stat targetStat;
    stat(target,&targetStat);

    int targetFd=open(target, O_RDONLY);
    if(targetFd==-1) return;    
    char targetContent[targetStat.st_size];

    size_t targetRead=read(targetFd, &targetContent, sizeof(targetContent));
    close(targetFd);
    if(targetRead!=targetStat.st_size) return;
    


    DIR * currDir=opendir(_dir);
    struct dirent *dp;
    if(currDir==NULL) {printf("lelele\n");
        return;}

    while((dp=readdir(currDir))!=NULL){
        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char query[1024]={0};
        snprintf(query,sizeof(query),"%s/%s",_dir,dp->d_name);

        struct stat queryStat;
        stat(query,&queryStat);

        char queryContent[queryStat.st_size];

        int fd=open(query, O_RDONLY);
        if(fd==-1) continue;     
                
        size_t queryRead=read(fd, queryContent, sizeof(queryContent));
        if(queryRead==queryStat.st_size){
            if(memcmp(queryContent, targetContent, targetStat.st_size)==0) printf("%s\n",query);
        }

        if(S_ISDIR(queryStat.st_mode)) recursiveSearchAll(query,_target);
        
        close(fd);
    }
    closedir(currDir);
}


int main(int argc, char * argv[]){

    if(argc!=4 && argc!=3 && argc!=5){
        printf("Use \nckfile -s /dir file \nckfile -l /dir file\n");
        printf("Use \nckfile -p <num_of_bytes> /dir file \nckfile /dir file\n");
        return 1;
    }

    // MODIFICA: L'ordine dei parametri passati alle funzioni era invertito. 
    // La firma delle tue funzioni richiede (char *_dir, char *_target).

    if(argc > 1 && strcmp(argv[1],"-s")==0) 
        recursiveSearch(argv[3], argv[2], 's'); // argv[3] è la dir, argv[2] è il file target

    else if(argc > 1 && strcmp(argv[1],"-l")==0)  
        recursiveSearch(argv[3], argv[2], 'l'); // MODIFICA: corretto errore di battitura reqcursiveSearch -> recursiveSearch

    else if(argc > 1 && strcmp(argv[1],"-p")==0) 
        recursiveSearchP(argv[4], argv[3], atoi(argv[2])); // argv[4] è la dir, argv[3] è il file target

    else if(argc==3) 
        recursiveSearchAll(argv[2], argv[1]); // argv[2] è la dir, argv[1] è il file target

    return 0;
}