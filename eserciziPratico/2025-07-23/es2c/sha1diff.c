#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <fcntl.h>
#include <unistd.h>


int sha1(char * filepath, char outputBuf[41]){

    char command[1024]={0};
    snprintf(command, sizeof(command), "sha1sum '%s'", filepath);

    FILE *fp=popen(command, "r"); //pipeopen
    if(fp==NULL){
        //Errore in popen
        return -1;
    }

    char buf[256];

    if(fgets(buf, sizeof(buf), fp)!=NULL){
        strncpy(outputBuf, buf, 40);
        outputBuf[40]='\0';
    }
    else{
        pclose(fp);
        return -1;
    }

    pclose(fp);

    return 0;

}

/*Scrivere un programma sha1dir con due argomenti:
il primo è il pathname di una directory, il secondo un pathname inesistente dove poter creare una
directory.
Il programma deve ricostruire nella directory creata una struttura ad albero identica a quella che ha
come radice il primo parametro. I nodi che nell'albero della prima directory sono file regolari
corrispondono nel secondo albero a file che contengono la hash sha1 del file della primo albero.*/

/*Scrivere un programma sha1diff che usando gli stessi parametri
passati precedentemente al programma sha1dir dell'esercizio 1 e mette in output l'elenco dei file che
sono stati modificati (la hash sha1 non corrisponde).*/

void recursiveTree(const char *sourceDir, const char *destDir){

    DIR * dir=opendir(sourceDir);
    struct dirent *dp;
    struct stat statBuf;

    while((dp=readdir(dir))!=NULL){
        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char sourcePath[4096];
        snprintf(sourcePath, sizeof(sourcePath), "%s/%s", sourceDir, dp->d_name);

        char destPath[4096];
        snprintf(destPath, sizeof(destPath), "%s/%s", destDir, dp->d_name);


        stat(sourcePath,&statBuf);
        if(S_ISREG(statBuf.st_mode)){
            char sourceSha[41]={0};
            char cloneSha[41]={0};
            int f=open(destPath, O_RDONLY);
            if(f!=-1){
                read(f, cloneSha, sizeof(cloneSha)-1);
                if(sha1(sourcePath,sourceSha)==0){
                    if(strcmp(sourceSha, cloneSha)!=0) printf("Modified: %s\n", sourcePath);
                }
                close(f);
            }
            
        }
        else if(S_ISDIR(statBuf.st_mode)){
            recursiveTree(sourcePath, destPath);
        }
    }
    closedir(dir);


}

int main(int argc, char * argv[]){

    if(argc!=3){
        printf("Use ./sha1dir <existing_dir/> <path_for_new_dir/>");
        return 1;
    }

    char targetDir[4096]={0};
    if(realpath(argv[1], targetDir)==NULL) return 1;

    recursiveTree(targetDir, argv[2]);


    return 0;
}