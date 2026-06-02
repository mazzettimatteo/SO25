#include<stdio.h>
#include<stdlib.h>
#include<limits.h>
#include<sys/types.h>
#include<dirent.h>
#include<fcntl.h>
#include<string.h>
#include<unistd.h>


/*Chiamiamo file dir ricorsivo un file che contiene una sequenza
di byte identica al pathname completo di un file della directory corrente. Il candidato scriva il
programma search_drec (senza parametri) che deve scorrere la directory corrente e elencare tutti i file
dir ricorsivi.*/
//passo un param così il programma è più bello: la dir su cui fare la ricerca
//Io ho capito che devo cercare solo nella dir corrente, non nelle sottodir, 
//altrimenti si utilizzerebbe la stessa logica ma rendendola una funzione ricorsiva

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use ./search_drec <dir/>");
        return 1;
    }

    

    DIR * currDir=opendir(argv[1]);
    struct dirent *dp;
    DIR * currDir_internal=opendir(argv[1]);
    struct dirent *dp_internal;
    


    while((dp=readdir(currDir))!=NULL){

        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        int trovato=0;

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

            rewinddir(currDir_internal); 
            /*La funzione readdir fa avanzare il puntatore di lettura dello stream a ogni iterazione. 
            Quando il ciclo while(dp_internal=...) termina, il puntatore si trova alla fine della dir (End Of File).
            Al passaggio alla riga successiva (o al file successivo), il ciclo riparte ma readdir
            restituisce immediatamente NULL perché il puntatore non è stato ripristinato all'inizio.*/
            
            while((dp_internal=readdir(currDir_internal)) && trovato!=1){
                if(strcmp(dp_internal->d_name, ".")==0 || strcmp(dp_internal->d_name, "..")==0) continue;

                char temp[1024]={0};
                snprintf(temp,sizeof(temp),"%s/%s", argv[1], dp_internal->d_name);
                char content[1024]={0};
                realpath(temp, content);

                if(strstr(lineBuf,content)!=NULL){
                    printf("%s\n", dp->d_name);
                    trovato=1;
                }
            }
            

            
        }
        free(lineBuf);
        fclose(currFile);

    }
    closedir(currDir);
    closedir(currDir_internal);

    return 0;
}