#include<stdio.h>
#include<fcntl.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/wait.h>
#include<sys/stat.h>
#include <getopt.h>

/*Fare un programma di copia parallelo di file.
pcp file1 file2
pcp deve creare due processi figli; mentre un processo copia la prima meta’ del file, l'altro deve
copiare l’altra meta’*/
/*usando “getopt” consentire di scegliere il grado di parallelismo voluto:
pcp -j 8 file1 file2
deve creare 8 processi, ogni processo copia 1/8 del file.*/

int main(int argc, char * argv[]){

    int nProcs=2; //default value
    int opt;

    while((opt=getopt(argc,argv, "j:"))!=-1){
        switch(opt){
            case 'j':
                nProcs=atoi(optarg);
                if(nProcs<=0) return 1;
                break;
            default:
                return 1;
            }
    }

    if(optind+2!=argc){
        printf("Use: ./pcp [-j num_procs] <src_file> <dest_file>");
        return 1;
    }

    int copyFd=creat(argv[optind+1],0644);//secondo arg: permessi del file
    //if(copyFd==-1) printf("llelele\n");

    struct stat srcStat;
    stat(argv[optind],&srcStat);
    
    int len=srcStat.st_size;  
    
    int slice=len/nProcs;

    int *sonPid=malloc(nProcs*sizeof(int));

    for(int i=0;i<nProcs;i++){
        sonPid[i]=fork();
        if(sonPid[i]==0){
            int offset=i*slice;
            int fd=open(argv[optind],O_RDONLY);

            if(i==nProcs-1){ //L'ultimo proc deve copiare risultato della divisione+resto
                slice+=(len%nProcs);
            }


            char *content=malloc(slice);
            if(fd!=-1){
                pread(fd,content,slice,offset); //Lettura parziale: leggo slice caratteri partendo da i*slice
            }
            pwrite(copyFd,content,slice,offset); //ultimo param è l'offset da cui partire per scivere nel file
            exit(0);
        }
        else{
            printf("Slice %d copiata\n",i);
        }
    }

    for(int i=0;i<nProcs;i++){
        waitpid(sonPid[i],NULL,0);
    }


    return 0;
}