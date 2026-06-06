#include<stdio.h>
#include<unistd.h>

int main(int argc, char * argv[]){

    printf("%d\n",getpid());

    for(int i=0; i<argc; i++) printf("%s ",argv[i]);
    printf("\n");

    while(1){
        
    }

    return 0;
}