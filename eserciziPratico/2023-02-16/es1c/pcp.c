#include<stdio.h>
#include<fcntl.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/wait.h>
#include<sys/stat.h>

/*Fare un programma di copia parallelo di file.
pcp file1 file2
pcp deve creare due processi figli; mentre un processo copia la prima meta’ del file, l'altro deve
copiare l’altra meta’*/

int main(int argc, char * argv[]){

    if(argc!=3){
        printf("Use: ./pcp <src_file> <dest_file>");
        return 1;
    }

    int copyFd=creat(argv[2],0644);//secondo arg: permessi del file

    struct stat srcStat;
    stat(argv[1],&srcStat);
    
    int len=srcStat.st_size;  
    int halfSize=len/2;


    int sonPid1=fork();
    if(sonPid1==0){
        int fd=open(argv[1],O_RDONLY);

        char *content=malloc(halfSize);
        if(fd!=-1){
            read(fd,content,sizeof(content));
        }


        pwrite(copyFd,content,halfSize,0); //ultimo param è l'offset da cui partire per scivere nel file
        exit(0);
    }
    int sonPid2=fork();
    if(sonPid2==0){
        int fd=open(argv[1],O_RDONLY);

        char *content=malloc(len-halfSize);
        if(fd!=-1){
            pread(fd,content,sizeof(content),halfSize); //partial read: what to read, where to save it, where to start reading
        }


        pwrite(copyFd,content,len-halfSize,halfSize);
        exit(0);
    }
    else{
        waitpid(sonPid1,NULL,0);
        waitpid(sonPid2,NULL,0);
        printf("File copiato\n");
        
    }

    return 0;
}