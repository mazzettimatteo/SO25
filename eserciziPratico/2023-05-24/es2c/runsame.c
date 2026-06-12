#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

/*Scrivere un programma che dato il numero di un processo attivo ne lanci uno uguale (lo stesso
eseguibile con gli stessi parametri, lo stesso environment e nella stessa directory corrente.
(hint: cercare nella directory del processo da clonare in /proc)*/

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use: ./runsame <PID>\n");
        return 1;
    }

    char exe[1024]={0};
    snprintf(exe,sizeof(exe),"/proc/%s/exe",argv[1]);
    char cmdline[1024]={0};
    snprintf(cmdline,sizeof(cmdline),"/proc/%s/cmdline",argv[1]);
    char environ[1024]={0};
    snprintf(environ,sizeof(environ),"/proc/%s/environ",argv[1]);
    char cwdLink[1024]={0};
    snprintf(cwdLink,sizeof(cwdLink),"/proc/%s/cwd",argv[1]);
    
    char currDir[1024];
    int len=readlink(cwdLink,currDir,sizeof(currDir)-1);
    if(len<0) return 1;
    currDir[len]='\0';

    char args[1024]={0};
    char env[1024]={0};

    char *new_argv[256];
    char *new_env[256];
    int cmdLen = 0;
    int envLen = 0;

    int cmdFD=open(cmdline,O_RDONLY);
    if(cmdFD!=-1){
        cmdLen=read(cmdFD,args,sizeof(args));
        if(cmdLen<0) return 1;
        close(cmdFD);
    }

    //Parsing del buffer args in new_argv
    int arg_idx = 0;
    char *p_arg = args;
    while (p_arg < args + cmdLen) {
        new_argv[arg_idx] = p_arg;
        arg_idx++;
        p_arg += strlen(p_arg) + 1;
    }
    new_argv[arg_idx] = NULL;


    int envFD=open(environ,O_RDONLY);
    if(envFD!=-1){
        envLen=read(envFD,env,sizeof(env));
        if(envLen<0) return 1;
        close(envFD);
    }

    int env_idx = 0;
    char *p_env = env;
    while (p_env < env + envLen) {
        new_env[env_idx] = p_env;
        env_idx++;
        p_env += strlen(p_env) + 1;
    }
    new_env[env_idx] = NULL;


    int sonPid=fork();
    if(sonPid==0){ 
        chdir(currDir);
        
        execve(exe, new_argv, new_env);
    }
    else{//padre
        waitpid(sonPid,NULL,0);
        printf("HO ESEGUITO: %s\n",exe);
    }

    return 0;
}