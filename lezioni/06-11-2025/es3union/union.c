#include<stdio.h>
#include<string.h>
#include<stdint.h>
/*UNION
Definisci una union chiamata Number che possa contenere: int i, float
f, array di 4 char bytes. Scrivi un programma che:
o assegni un valore a i e mostri come cambia la rappresentazione nei
bytes;
o assegni un valore a f e osservi i bytes;*/

union Number{
    int32_t i;
    float f;
    unsigned char bytes[4];
};

//funzione che legge da memoria
void print_bytes(const unsigned char * b, size_t n){
    for(size_t k=0;k<n;k++){
        printf("%02X ",b[k]);//il puntatore b è il puntatore all'array di char
        printf("\n");
    }
}


int main(){
    union Number n;
    n.i=0x01020304;
    printf("i=0x%08x ->bytes: \n",(unsigned) n.i); 
    //così stiamo ottenendo il valore esattamente come l'abbiamo salvato 
    //ma non lo stiamo leggendo dalla memoria. Lo capiamo perché otteniamo una cosa big-endian 
    //e dovrebbe essere invece little-endian, usiamo una funzione che legga come sono veramente i bye salvati in memoria
    print_bytes(n.bytes,sizeof(n.bytes));
    //da questa stampa capiamo che stiamo utilizzando little-endian

    //se io adesso vado a memorizzare un float piuttosto che un intero dove lo comunico all'interno del programma?
    //usiamo una struct con un enum che mi dice queale dato della union è al momento attivo
    printf("f=%.6f ->bytes: \n",n.f);
    n.f=1.0f;
    print_bytes(n.bytes,sizeof(n.bytes));

    //ma se io pensassi che stessimo ancora usando gli interi?
    //vediamo cosa succede nella stampa:
    printf("intero: %d \n",n.i);
    //dato che mi esce una roba assurda, è meglio usare una struct per tenere nota di quale tipo è attivo al momento
    
    return 0;
}