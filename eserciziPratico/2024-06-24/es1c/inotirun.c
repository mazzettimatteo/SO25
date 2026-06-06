#include<stdio.h>
#include<limits.h>
#include<unistd.h>
#include<sys/inotify.h>
#include<string.h>
#include<sys/wait.h>

/*Usando inotify scrivere un programma inotirun che ha come parametro il pathname di una
directory vuota che chiameremo D. Quando vengono inseriti file in D questi vengono eseguiti (uno
alla volta) e cancellati. I file in D hanno il seguente formato:
* il pathname dell'eseguibile
* una riga per ogni elemento di argv.
Es:
/bin/ls
ls
-l
/tmp*/

int main(int argc, char * argv[]){

    if(argc!=2){
        printf("Use: ./inotirun <dir/>");
        return 1;
    }

    int fd=inotify_init(); //Inizializzo
    if(fd<0) return 1;

    char D[1024]={0};
    realpath(argv[1],D);

    int wd=inotify_add_watch(fd, D, IN_CLOSE_WRITE); //osservo gli eventi di "fine scrittura di file" dentro D
    if(wd==-1) return 1;

    while(1){

        char buffer[4096];
        int length=read(fd,buffer, sizeof(buffer)); //memorizzo in buffer i vari eventi avvenuti(aggiunta in scrittura di file) 
        if(length<0) return 1;

        struct inotify_event * event= (struct inotify_event *) buffer; 


        if(event->len > 0 && (event->mask & IN_CLOSE_WRITE)){ //Se è avvenuto l'evento che mi interessava
            char filePath[1024]={0};
            snprintf(filePath, sizeof(filePath), "%s/%s", D, event->name); //Guardo su che file è avvenuto

            FILE * file=fopen(filePath, "r");
            char line[1024];

            char *cmd_args[100];
            int arg_count = 0;

            while(fgets(line, sizeof(line), file) != NULL){ //Di quel file leggo una riga alla volta
                
                int idxOfNewline=strlen(line)-1; //lunghezza della stinga escluso "\n"
                line[idxOfNewline] = '\0'; //e sostituisco il char newline con il terminatore "\0"
                
                cmd_args[arg_count] = strdup(line); //Ogni riga è un argomento per execvp
                arg_count++;
            }
            
            cmd_args[arg_count] = NULL; //Execvp vuole ultimo argomento NULL 

            int sonPid = fork(); //Divido l'esecuzione in modo che il figlio esegua l comando mentre il padre continui a scansionare i file in D
            if(sonPid == 0){
                execv(cmd_args[0], cmd_args);
                exit(1); 
            } 
            else if(sonPid > 0) {
                waitpid(sonPid, NULL, 0);
            }

            // Pulizia delle risorse e cancellazione del file
            fclose(file);
            unlink(filePath);

            for(int i = 0; i < arg_count; i++){
                free(cmd_args[i]);
            }           

        }

    }

    return 0;
}