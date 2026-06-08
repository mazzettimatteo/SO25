#include<stdio.h>
#include<dirent.h>
#include<string.h>
#include<unistd.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<sys/wait.h>
#include<fcntl.h>
/*Il programma run_name deve cercare nel sottoalbero della directory corrente tutti i file eseguibili con
un nome file specifico (primo parametro di run_name) e li deve mettere in esecuzione uno dopo l'altro
passando i successivi parametri.
Ad esempio il comando:
./run_name testprog a b c
deve cercare i file eseguibili chiamati testprog nell'albero della directory corrente. Poniamo
siano ./testprog, ./dir1/testprog, ./dir/dir3/testprog, run_name deve eseguire
testprog a b c
per 3 volte. Nella prima esecuzione la working directory deve essere la dir corrente '.', la seconda
deve avere come working directory './dir1' e la terza './dir2/dir3'*/

void recursiveSearch(char *query, char * dir, char *params[],int numOfParams){
    
    DIR * currDir=opendir(dir);
    if(currDir==NULL) return;
    struct dirent * dp;

    while((dp=readdir(currDir))!=NULL){

        if(strcmp(dp->d_name, ".")==0 || strcmp(dp->d_name, "..")==0) continue;

        char dpPath[1024]={0};
        snprintf(dpPath, sizeof(dpPath), "%s/%s", dir, dp->d_name);

        struct stat dpStat;
        stat(dpPath,&dpStat);

        if((dpStat.st_mode & S_IXUSR) && strcmp(dp->d_name,query)==0){
            int fd=open(dpPath, O_RDONLY);
            char content[4];
            int len=read(fd,content,sizeof(content)); 
            if(len<0) continue;
            else{
                if(content[0]=='#' && content[1]=='!') {
                    
                    int sonPid=fork();
                    if(sonPid==0){
                        chdir(dir);//Perché viene richiesto cambio della dir di esecuzione

                        char *parameters[1024];
                        parameters[0]=dp->d_name;
                        int j=1;
                        for(int i=3;i<numOfParams;i++){
                            parameters[j]=params[i];
                            j++;
                        }
                        parameters[j]=NULL;
                        
                        char dpPath_son[1024]={0};
                        snprintf(dpPath_son,sizeof(dpPath_son),"./%s",dp->d_name);

                        execv(dpPath_son,parameters); 
                    }
                    else{
                        waitpid(sonPid,NULL,0);
                    }

                }
                else if(content[0]==0x7f && content[1] == 'E' && content[2] == 'L' && content[3] == 'F') {
                    int sonPid=fork();
                    if(sonPid==0){
                        chdir(dir);

                        char *parameters[1024];
                        parameters[0]=dp->d_name;
                        int j=1;
                        for(int i=3;i<numOfParams;i++){
                            parameters[j]=params[i];
                            j++;
                        }
                        parameters[j]=NULL;

                        char dpPath_son[1024]={0};
                        snprintf(dpPath_son,sizeof(dpPath_son),"./%s",dp->d_name);

                        execv(dpPath_son,parameters);
                    }
                    else{
                        waitpid(sonPid,NULL,0);
                    }
                }
                close(fd);
            }
            
               
        }
    
        if(S_ISDIR(dpStat.st_mode)){
            recursiveSearch(query, dpPath, params,numOfParams);
        }

    }
    closedir(currDir);

}



int main(int argc, char * argv[]){

    //Facciamo che voglio specificare la directory di partenza da cui cercare

    if(argc<4){
        printf("Use: ./run_name <string_to_search> <dir/> <param_1> ... <param_n>");
        return 1;
    }

    recursiveSearch(argv[1], argv[2], argv, argc); //Ricorda che i parametri, che sono gli stessi per tutti, iniziano dalla posizione 3

    return 0;
}