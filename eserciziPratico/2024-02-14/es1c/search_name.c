#include<stdio.h>
#include<dirent.h>
#include<string.h>
#include<unistd.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<fcntl.h>
/*Scrivere un programma search_name che deve cercare nel sottoalbero della directory corrente tutti i
file eseguibili con un nome file specifico passato come primo e unico parametro indicando per ogni
file il tipo di eseguibile (script o eseguibile binario).
Ad esempio il comando:
./search_name testprog
deve cercare i file eseguibili chiamati testprog nell'albero della directory corrente. Poniamo
siano ./testprog, ./dir1/testprog, ./dir/dir3/testprog, search_name deve stampare:
. /testprog: script
./dir1/testprog: ELF executable
./dir/dir3/testprog: ELF executable*/

void recursiveSearch(char *query, char * dir){
    
    DIR * currDir=opendir(dir);
    if(currDir==NULL) return;
    struct dirent * dp;

    while((dp=readdir(currDir))!=NULL){

        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath, sizeof(dpPath), "%s/%s", dir, dp->d_name);

        struct stat dpStat;
        stat(dpPath,&dpStat);

        if((dpStat.st_mode & S_IXUSR) && strcmp(dp->d_name,query)==0){
            int fd=open(dpPath, O_RDONLY);
            char content[4];
            int len=read(fd,content,sizeof(content)); 
            if(len<0) continue;
            else{
                if(content[0]=='#' && content[1]=='!') printf("%s: script\n",dpPath);
                else if(content[0]==0x7f && content[1] == 'E' && content[2] == 'L' && content[3] == 'F') 
                    printf("%s: ELF exec\n",dpPath);
                close(fd);
            }
            
               
        }
    
        if(S_ISDIR(dpStat.st_mode)){
            recursiveSearch(query, dpPath);
        }

    }
    closedir(currDir);

}



int main(int argc, char * argv[]){

    //Facciamo che voglio specificare la directory di partenza da cui cercare

    if(argc!=3){
        printf("Use: ./search_name <string_to_search> <dir/>");
        return 1;
    }

    recursiveSearch(argv[1], argv[2]);

    return 0;
}