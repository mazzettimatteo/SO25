#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<dirent.h>
#include<string.h>
#include<sys/stat.h>
#include <unistd.h>

/*scrivere un programma cprl che si comporti come il comando "cp -rl". cprl ha due parametri:
cprl a b
deve copiare l'intera struttura delle directory dell'albero che ha come radice a in un secondo albero
con radice b. I file non devono essere copiati ma collegati con link fisici.
(l'operazione deve essere fatta dal codice C, senza lanciare altri programmi/comandi*/

void recCopy(char * src, char *dst){

    DIR * srcDir=opendir(src);
    struct dirent *dp;

    while((dp=readdir(srcDir))!=NULL){
        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath,sizeof(dpPath),"%s/%s", src, dp->d_name);

        struct stat dpStat;
        lstat(dpPath,&dpStat);

        char destination[1024]={0};
        snprintf(destination,sizeof(destination),"%s/%s",dst,dp->d_name);

        if(S_ISDIR(dpStat.st_mode)){
            mkdir(destination, S_IRWXU);
            recCopy(dpPath, destination);
        }
        else{
            link(dpPath,destination);
        }

    }
    closedir(srcDir);


}


int main(int argc, char * argv[]){

    if(argc!=3){
        printf("Use: ./cplr <src_dir/> <dest_dir/>");
        return 1;
    }

    DIR *dest=opendir(argv[2]);
    if(dest==NULL){
        mkdir(argv[2],S_IRWXU); 
    }
    else{
        closedir(dest);
    }
    recCopy(argv[1], argv[2]);

    return 0;
}