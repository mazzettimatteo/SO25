#include<stdio.h>
#include<sys/types.h>
#include<dirent.h>
#include<string.h>
#include<sys/stat.h>

/*l programma da realizzare si chiama tree mostra un sottoalbero del file system.
es data una directory A che contiene una sottodirectory B e un file C; B contiene i file E F e G:
tree A dovrebbe produrre:
B
    E
    F
    G
C
*/

void recExplore(char * dir, int depth){

    DIR * currDir=opendir(dir);
    struct dirent *dp;

    while((dp=readdir(currDir))!=NULL){
        if(strcmp(dp->d_name,".")==0 || strcmp(dp->d_name,"..")==0) continue;
        for(int i=0;i<depth;i++){
            printf(" ");
            printf(" ");
            printf(" ");
        }
        printf("%s\n",dp->d_name);

        char dpPath[1024]={0};
        snprintf(dpPath,sizeof(dpPath),"%s/%s",dir,dp->d_name);

        struct stat dpStat;
        stat(dpPath,&dpStat);

        if(S_ISDIR(dpStat.st_mode)) {
            
            recExplore(dpPath,depth+1);
        }

    }
    closedir(currDir);

}



int main(int argc, char * argv[]){

    printf("%s\n",argv[1]);
    recExplore(argv[1],1);

    return 0;
}
