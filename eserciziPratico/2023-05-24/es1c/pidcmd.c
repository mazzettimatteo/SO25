#include<stdio.h>
#include<dirent.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include<string.h>

/*Scriveere un programma pidcmd che stampi i pid dei processi attivi lanciati con una specifica riga di
comando. (Devono coincidere tutti gli argomenti)
es: ll comando "pidcmd less /etc/hostname" deve stampare il numero di processo dei processi attivi
che sono stati lanciati con "less /etc/hostname"
(hint: cercare nelle directory dei processi in /proc i "file" chiamati cmdline)*/

int main(int argc, char *argv[]){


    char argomenti[1024];
    size_t target_len = 0;
    for(int i = 1; i < argc; i++){
        size_t arg_len = strlen(argv[i]);
        memcpy(argomenti + target_len, argv[i], arg_len);
        target_len += arg_len;
        argomenti[target_len] = '\0';
        target_len++;
    }


    DIR * proc=opendir("/proc");
    struct dirent *dp;

    while((dp=readdir(proc))!=NULL){

        if(strcmp(dp->d_name,".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath,sizeof(dpPath),"/proc/%s",dp->d_name);

        struct stat dpStat;
        stat(dpPath,&dpStat);

        int currPid=atoi(dp->d_name);

        if(S_ISDIR(dpStat.st_mode) && currPid!=0){ //atoi su stinga non numerica ritorna 0
                
            char cmdlinePath[1024]={0};
            snprintf(cmdlinePath,sizeof(cmdlinePath),"%s/cmdline",dpPath);

            //ora devo aprire il file cmdline, sò già che c'è, lo apro SUBITO senza scansionare la dir
            int fd=open(cmdlinePath,O_RDONLY);
            if(fd!=-1){
                char content[1024];
                int len=read(fd,content,sizeof(content));
                if(len<0) continue;

                //se content==argv stampa currPid
                if(len==target_len && memcmp(argomenti,content,target_len)==0){
                    printf("%d\n",currPid);
                }
                close(fd);
            }

        }

    }
    closedir(proc);
    

    return 0;
}