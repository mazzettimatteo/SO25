#include<stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include<unistd.h>
#include <stdlib.h>
#include<string.h>
#include<openssl/evp.h>

#define BUFFER_SIZE 4096

/*Scrivere un programma sha1index che ha al più unparametro. 
(se non ha parametro opera sulla directory corrente, altrimenti sulla directory indicata dal parametro)
Per ogni file f ordinario nella directory il programma crea un link simbolico in una sottodirectory
nascosta di nome “.sha1index” che punta al file e ha come nome la hash sha1 del contenuto.
Es. data nella dir corrente due file f1 e f2, il programma sha1index crea nella directory .sha1index
due link simbolici:
.sha1index/5e180efdd44e3a3585834b6bd618ef7c5a462d9a che punta a f1 e
.sha1index/82442bcd9a1e36899d43c04f79491cd616f7b30a che punta a f2
(i valori delle hash sono solo a titolo di esempio, rappresentano le hash del contenuto di f1 e di f2)*/
/*Scrivere un programma sha1update che aggiorna i file creati dal
programma dell’esercizio 1. Per ogni link simbolico presente nella directory nascosta .sha1index (se c’è)
possono verificarsi due casi:
• il file è stato cancellato (il link punta a un file inesistente), viene cancellato il link
• il file è stato modificato più recentemente della data di creazione del link, occorre aggiornare il
link simbolico (si ricalcola la hash e si ricrea il link simbolico)*/

//A CAUSA DELLA FUNZIONE CHE CALCOLA SHA1 COMPILA COSÌ: gcc sha1index.c -o sha1index -lcrypto
/* Funzione per calcolare lo SHA-1 di un file */
int calculate_sha1(const char *path, char outputBuffer[41]) {
    FILE *file = fopen(path, "rb");
    if (!file) return -1;

    EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
    if (mdctx == NULL) {
        fclose(file);
        return -1;
    }

    if (1 != EVP_DigestInit_ex(mdctx, EVP_sha1(), NULL)) {
        EVP_MD_CTX_free(mdctx);
        fclose(file);
        return -1;
    }

    unsigned char buffer[BUFFER_SIZE];
    size_t bytesRead = 0;

    while ((bytesRead = fread(buffer, 1, BUFFER_SIZE, file)) != 0) {
        if (1 != EVP_DigestUpdate(mdctx, buffer, bytesRead)) {
            EVP_MD_CTX_free(mdctx);
            fclose(file);
            return -1;
        }
    }

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int lengthOfHash = 0;

    if (1 != EVP_DigestFinal_ex(mdctx, hash, &lengthOfHash)) {
        EVP_MD_CTX_free(mdctx);
        fclose(file);
        return -1;
    }

    EVP_MD_CTX_free(mdctx);
    fclose(file);

    // Converte in stringa esadecimale
    for (unsigned int i = 0; i < lengthOfHash; i++) {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }
    outputBuffer[40] = '\0';

    return 0;
}


int main(int argv, char * argc[]){

    char hiddenDir[256]={0};
    realpath(".sha1index/",hiddenDir);

    DIR *currDir=opendir(hiddenDir);
    struct dirent *dp;
    while((dp=readdir(currDir))!=NULL){

        if(strcmp(dp->d_name, ".") == 0 || strcmp(dp->d_name, "..") == 0) continue;

        char fullPath[256]={0};
        snprintf(fullPath, sizeof(fullPath), "%s/%s", hiddenDir,dp->d_name);

        char src[4096]={0};
        int lettura=readlink(fullPath, src, sizeof(src)-1); //ritorna numero di caaratteri copiati, o -1 se non riesce a leggere
        src[lettura]='\0';

        if(lettura==-1){
            //C'è un errore, elimino questo link
            unlink(fullPath);
            continue;
        }
        
        struct stat srcStat;
                
        if(stat(src, &srcStat)==-1){
            unlink(fullPath);
            continue;
        }
        struct stat linkStat;
        lstat(fullPath, &linkStat);

        if(srcStat.st_mtime>linkStat.st_mtime){
            char hash[41]={0};
            if(calculate_sha1(src, hash)==0){
                if(strcmp(dp->d_name,hash)==0){
                    //hash uguale ma ci sono state modifiche: elimino e ricreo
                    unlink(fullPath);
                    symlink(src,fullPath);
                }
                else{
                    char newName[256]={0};
                    snprintf(newName, sizeof(newName), "%s/%s", hiddenDir, hash);
                    symlink(src,newName);
                    unlink(fullPath);                    
                }
            }
        }


    }
    closedir(currDir);

    return 0;
}