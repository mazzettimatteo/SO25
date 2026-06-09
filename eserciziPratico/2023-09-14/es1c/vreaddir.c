#include<stdio.h>
#include<stdlib.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<dirent.h>
#include<string.h>
#include <fcntl.h>

/*Scrivere la funzione:
char **vreaddir(const char *path)
che restituisca l'elenco dei nomi dei file in una directory come vettore di stringhe terminato con un
puntatore NULL. (lo stesso formato di argv o envp).
Il vettore e le stringhe dei nomi sono allocate dinamicamente.
completare l'esercizio con un programma principale che testi il corretto funzionamento della funzione
vreaddir.*/

char ** vreaddir(const char * path){

    DIR * currDir=opendir(path);
    struct dirent *dp;

    char **result=NULL; 
    int size=0;

    while((dp=readdir(currDir))!=NULL){
        char file[1024]={0};
        snprintf(file,sizeof(file),"%s/%s",path,dp->d_name);

        struct stat fileStat;
        stat(file,&fileStat);

        if(S_ISREG(fileStat.st_mode)){
            char **temp=realloc(result, (size+1)*sizeof(char *)); //allarga di 1 il vettore result, salvando nelle prime posizioni i contenuti di result

            if(temp==NULL) return NULL;

            result=temp; //sovrascivi result con il nuovo vettore più grande

            result[size]=strdup(file); //inserisci il path del file dentro result

            size++;
            
        }


    }
    closedir(currDir);

    result=realloc(result,(size+1)*sizeof(char *));
    result[size]=NULL;

    return result;

}


void test(char *testDirPath){

    int testDir=mkdir(testDirPath, S_IRWXU);

    char f1[1024]={0};
    snprintf(f1,sizeof(f1),"%s/file1.txt",testDirPath);
    char f2[1024]={0};
    snprintf(f2,sizeof(f2),"%s/file2.txt",testDirPath);
    char f3[1024]={0};
    snprintf(f3,sizeof(f3),"%s/file3.md",testDirPath);


    int fd1=creat(f1, S_IRWXU);
    int fd2=creat(f2, S_IRWXU);
    int fd3=creat(f3, S_IRWXU);

    printf("Output shold be somethink like:\n");
    printf("%s\n",f1);
    printf("%s\n",f2); 
    printf("%s\n",f3);


}

int main(int argc, char * argv[]){

    test(argv[1]);

    char ** result=vreaddir(argv[1]);
    
    printf("Output:\n");
    for(int i=0;result[i]!=NULL;i++){
        printf("%s\n",result[i]);
    }
    
    for(int i=0;result[i]!=NULL;i++) free(result[i]);
    free(result);
    
    return 0;
}