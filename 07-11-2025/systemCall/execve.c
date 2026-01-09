#include<stdio.h>
#include<unistd.h>
#include <sys/wait.h>

/*
Una chiamata di sistema viene fatta vosì: si fa una fork() dentro un if the else, 
nel ramo if(quello del parent) si fa una wait mentre nel ramo child  si fa una execve
*/

int main(){

    char *exec_argv[]={
        "ls", "-l", "/",NULL
        //ls is argv[0], -l is argv[1] and so on
        //NULL is not a string but a nullptr says that the argv list is finished
    };


    printf("pre %d\n",getpid());
    execve("/usr/bin/ls", exec_argv,NULL);//execve sostituisce il codice che quel processo sta eseguendo:
    // rimane lo stesso processo ma cmabia in toto il codice
    //eseguire questo file è come fare ls -l /

    printf("post %d\n",getpid());//questa print se l'exec ha successo non apparirà mai
    
    return 0;
}