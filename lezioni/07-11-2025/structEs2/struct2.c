#include<stdio.h>

/*
Definisci due versioni di una struct chiamata Data che contengano char a,
int b, short c in ordine diverso. Scrivi un programma che:
o stampi sizeof(struct Data1) e sizeof(struct Data2);
o aggiungi, direttive di packing (#pragma pack) e confronta di nuovo le
dimensioni.

*/

typedef struct{
    char a;
    int b;
    short c;
} DataA;


typedef struct{
    int b;
    short c;
    char a;    
} DataB;


//ora con pragma(1)

#pragma pack(1)
typedef struct{
    char a;
    int b;
    short c;
} Data1;


typedef struct{
    int b;
    short c;
    char a;    
} Data2;


//ora con pragma(0)

#pragma pack(0)
typedef struct{
    char a;
    int b;
    short c;
} DataX;


typedef struct{
    int b;
    short c;
    char a;    
} DataY;


//ora con pragma(2)

#pragma pack(2)
typedef struct{
    char a;
    int b;
    short c;
} DataU;


typedef struct{
    int b;
    short c;
    char a;    
} DataV;



int main(){


    printf("dataA size: %zu \n",sizeof(DataA));
    printf("dataB size: %zu \n",sizeof(DataB));
    //notiamo che dataA e dataB hanno due dimensioni diverse

    //usiamo ora pragma pack su Data1 e Data 2 definite rispettivamente come DataA e DataB
    printf("data1 size con pragma pack(1): %zu \n",sizeof(Data1));
    printf("data2 size con pragma pack(1): %zu \n",sizeof(Data2));


    //proviamo ora con pragmaPack(0), che equivale a non averlo messo
    printf("dataX size con pragma pack(0): %zu \n",sizeof(DataX));
    printf("dataY size con pragma pack(0): %zu \n",sizeof(DataY));
    

    //proviamo ora con pragmaPack(2)
    printf("dataU size con pragma pack(2): %zu \n",sizeof(DataU));
    printf("dataV size con pragma pack(2): %zu \n",sizeof(DataV));
    
    
    
    
    return 0;
}