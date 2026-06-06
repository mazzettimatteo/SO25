#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include <fcntl.h>

/*Scrivere un programma cloneproc dato il pid di un processo passato come unico parametro, è in
grado di eseguirne una copia. (deve rieseguire lo stesso file con lo stresso argv.
consiglio: cercare in /proc/pid/exe e /proc/pid/cmdline le informazioni necessarie (dove pid è il numero
di processo.
scrivere inoltre un semplice programma che ne dimostri il funzionamento.*/

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use: ./cloneproc <pid>");
        return 1;
    }

    char procPidExe[1024]={0};
    snprintf(procPidExe, sizeof(procPidExe), "/proc/%s/exe", argv[1]);
    char procPidCmdline[1024]={0};
    snprintf(procPidCmdline, sizeof(procPidCmdline), "/proc/%s/cmdline", argv[1]);
    
    char commandPath[1024]={0};
    int len1=readlink(procPidExe,commandPath,sizeof(commandPath)-1);
    if(len1<0) { printf("len1\n"); return 1; }
    commandPath[len1]='\0';

    int fd=open(procPidCmdline, O_RDONLY); 
    char buf[1024]={0};
    int len2=read(fd,buf,sizeof(buf)); 
    if(len2<0){ printf("len2\n"); return 1; }

    //printf("%s\n%s\n",commandPath,buf);


    //Buf è formattato con tutti gli argomenti separati da char '\0'
    //Io per far partire il comado ho bisogno invece di un array di puntatori a char, 
    //ogni puntatore deve puntare ad un argomento di quelli in buf
    char * newArgv[128];
    int argCont=0;

    newArgv[0]=&buf[0];
    argCont++;
    for(int i=1; i<len2 -1; i++){
        if(buf[i]=='\0'){
            newArgv[argCont]=&buf[i+1];
            argCont++;
        }
    }

    newArgv[argCont]=NULL;

    execv(commandPath, newArgv);


    return 0;
}