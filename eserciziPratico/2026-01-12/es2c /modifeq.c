#define _POSIX_C_SOURCE 200809L

#include<stdio.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<dirent.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>
#include<time.h>

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

/*2. Scrivere il comando modif= che opera come modifcmp ma invece di controllare i file modifcati più di
recente, elenca i pathname dei file che hanno il tempo di modifica uguale a quella del file indicato nel
primo parametro che non sia un link fisico o logico di tale file. Occorre mostrare anche come
costruire un esempio per testare il programma. */

void recExplore(char * startingDir, time_t baseTime, ino_t targetNode){
    DIR *currDir=opendir(startingDir);
    struct dirent *dp;
    

    while((dp=readdir(currDir))!=NULL){

        
        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char fullPath[1000]={0};

        snprintf(fullPath, sizeof(fullPath), "%s/%s", startingDir, dp->d_name);


        struct stat buf;
        lstat(fullPath, &buf);

        ino_t currNode =buf.st_ino;
        if(S_ISLNK(buf.st_mode) || currNode==targetNode) continue;
        else if(S_ISDIR(buf.st_mode)) recExplore(fullPath, baseTime, targetNode); 
        else if(S_ISREG(buf.st_mode)){
            if(buf.st_mtime - baseTime ==0) printf("%s\n", fullPath);
        }

        
    }

    closedir(currDir);
}

void buildTestDir(){
    if(mkdir("./testDir/", S_IRWXU)==0){
        int f1=creat("./testDir/target.txt", S_IRWXU);
        close(f1);
        int f2=creat("./testDir/clone.txt", S_IRWXU);
        close(f2);
        symlink("./testDir/target.txt", "./testDir/symlink.txt");
        link("./testDir/target.txt", "./testDir/hardlink.txt");
        int f4=creat("./testDir/different.txt", S_IRWXU);
        close(f4);

        //Creo nuovo file con stessi metadati(mtime compreso) di target.txt

        struct stat targetbuf;
        stat("./testDir/target.txt", &targetbuf);

        struct timespec times[2];
        times[0]=targetbuf.st_atim;
        times[1]=targetbuf.st_mtim;
        utimensat(AT_FDCWD, "./testDir/clone.txt", times, 0);

        struct timespec differentTimes[2];
        differentTimes[0]=times[0];
        differentTimes[1]=times[1];
        differentTimes[1].tv_sec-=10;
        utimensat(AT_FDCWD, "./testDir/different.txt", differentTimes, 0);


    }

}


int main (int argc, char * argv[]){


    buildTestDir();



    if(argc==2){ //(a)
        struct stat statbuf;
        lstat(argv[1], &statbuf);

        time_t baseTime=statbuf.st_mtime;
        ino_t targetNode=statbuf.st_ino;


        recExplore(".", baseTime, targetNode);
    }
    else if(argc==3){
        struct stat arg1;
        lstat(argv[1], &arg1);
        struct stat arg2;
        lstat(argv[2], &arg2);
        if(S_ISDIR(arg2.st_mode)){ //(c)
            time_t baseTime=arg1.st_mtime;
            ino_t targetNode=arg1.st_ino;
            recExplore(argv[2], baseTime, targetNode);
        }
        else if(S_ISREG(arg2.st_mode)){
            time_t baseTime=arg1.st_mtime;
            ino_t targetNode1=arg1.st_ino;
            time_t time2=arg2.st_mtime;
            ino_t targetNode2=arg2.st_ino;
            if (time2-baseTime==0 && targetNode1 != targetNode2) printf("%s", argv[2]);

        }

    }

    

    return 0;
}
