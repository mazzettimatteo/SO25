#include<stdio.h>
#include<stdlib.h>
#include<limits.h>
#include<sys/types.h>
#include<dirent.h>
#include<fcntl.h>
#include<string.h>
#include<unistd.h>


/*hiamiamo file path ricorsivo un file che contiene
una sequenza di byte identica al proprio pathname completo. Ad esempio un file myfile nella
directory /tmp/mydir è path ricorsivo se contiene la sequenza /tmp/mydir/myfile. Il candidato scriva il
programma search_prec (senza parametri) che deve scorrere la directory corrente e elencare tutti i file
path ricorsivi.*/
//passo un param così il programma è più bello: la dir su cui fare la ricerca
//Io ho capito che devo cercare solo nella dir corrente, non nelle sottodir, 
//altrimenti si utilizzerebbe la stessa logica ma rendendola una funzione ricorsiva

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use ./search_prec <dir/>");
        return 1;
    }

    

    DIR * currDir=opendir(argv[1]);
    struct dirent *dp;

    while((dp=readdir(currDir))!=NULL){

        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char query[1024]={0};
        snprintf(query,sizeof(query),"%s/%s", argv[1], dp->d_name);
        
        char fullPath[1024]={0};
        realpath(query, fullPath);

        int fd=open(fullPath, O_RDONLY);
        if(fd==-1) continue;     
        FILE * currFile=fdopen(fd, "r");
        if(currFile==NULL){
            close(fd);
            continue;
        }

        char *lineBuf=NULL;
        size_t bufDim=0;
        ssize_t readBytes;

        while((readBytes=getline(&lineBuf,&bufDim, currFile))!=-1){
            if(strstr(lineBuf,fullPath)!=NULL){
                printf("%s\n", dp->d_name);
            }
        }
        free(lineBuf);
        fclose(currFile);

    }
    closedir(currDir);

    return 0;
}