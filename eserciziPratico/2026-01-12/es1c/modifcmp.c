#include<stdio.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<dirent.h>
#include<string.h>

/*Scrivere il programma C modifcmp che confronta il tempo dell’ultima modifica fra file
modifcmp ammette molteplici modalità di funzionamento,
a) se viene chiamato con il pathname di un file come solo argomento elenca i pathname di tutti i
file nel sottoalbero della directory corrente aggiornati più recentemente rispetto al file passato
come parametro (es: modifcmp myfile)
b) se viene chiamato con i pathname di due file come parametri stampa il pathname del
secondo file se è stato aggiornato più recentemente del primo (es: modifcmp myfile1
tmp/myfile2)
c) se viene chiamato con un pathname di un file e uno di una directory elenca il pathname di
tutti i file nel sottoalbero che ha come radice il secondo pathname aggiornati più
recentemente rispetto al file passato come primo parametro (es: modifcmp myfile mydir)*/

void recExplore(char * startingDir, time_t baseTime){
    DIR *currDir=opendir(startingDir);
    struct dirent *dp;
    

    while((dp=readdir(currDir))!=NULL){

        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char fullPath[1000]={0};

        snprintf(fullPath, sizeof(fullPath), "%s/%s", startingDir, dp->d_name);


        struct stat buf;
        stat(fullPath, &buf);

        if(S_ISDIR(buf.st_mode)) recExplore(fullPath, baseTime);
        else if(S_ISREG(buf.st_mode)){
            if(buf.st_mtime - baseTime >0) printf("%s\n", fullPath);
        }

        
    }

    closedir(currDir);
}



int main (int argc, char * argv[]){

    if(argc==2){ //(a)
        struct stat statbuf;
        stat(argv[1], &statbuf);

        time_t baseTime=statbuf.st_mtime;

        recExplore(".", baseTime);
    }
    else if(argc==3){
        struct stat arg1;
        stat(argv[1], &arg1);
        struct stat arg2;
        int retVal=stat(argv[2], &arg2);
        if(S_ISDIR(arg2.st_mode)){ //(c)
            time_t baseTime=arg1.st_mtime;
            recExplore(argv[2], baseTime);
        }
        else if(S_ISREG(arg2.st_mode)){
            time_t baseTime=arg1.st_mtime;
            time_t time2=arg2.st_mtime;
            if (time2-baseTime>0) printf("%s", argv[2]);

        }

    }

    

    return 0;
}
