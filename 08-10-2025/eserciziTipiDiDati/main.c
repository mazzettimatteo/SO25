#include<stdio.h>
/*
Vogliamo utilizzare tipi portatili
usiamo tipi moderni della libreria stdint.h come uint8_t, uint32_t che sono tipi a larghezza fissa
E' garantito che poi questi tipi vengano tradotti bene nel c quando ad esempio li si stampa? No
Anche i puntatori hanno lunghezza diversa. 
Anche le struct cambiano dimensione da architettura ad architettura.
Ci sono delle macro ad esempio per stampare. Il calcolatore fa una promozione per ogni tipo di dato durante la stampa.
i char occupano 1byte l'uno ma poi la CPU li promuove per ottenere parolo della dimensione corretta per i registri della CPU
C'è il problema analogo per le operazioni size: usiamo quindi size_t per tutte le operazioni di dimensione/memoria.
*/

/*1. Scrivere un programma che stampi:
la dimensione in byte dei tipi base 
(char, int, unsigned int, float, double),
il valore minimo e massimo per interi e floating point (usando <limits.h> e
<float.h>)
*/
#include <limits.h>
#include <float.h>

void es1(){
	printf("char %zu, min %d, max %d \n",sizeof(char),CHAR_MIN,CHAR_MAX);
	//il char è signed in questo caso

	printf("int %zu, min %d, max %d \n",sizeof(int),INT_MIN,INT_MAX);
	printf("unsigned int %zu, min %u, max %u \n",sizeof(unsigned int),0,UINT_MAX);
	printf("float %zu, min %f, max %f \n",sizeof(float),FLT_MIN,FLT_MAX);
	printf("double %zu, min %f, max %f \n",sizeof(double),DBL_MIN,DBL_MAX);
	
}


/*2. Scrivere un programma che dichiari una variabile intmax_t (da <stdint.h>)
e la stampi. Il programma deve essere portabile.*/
#include<inttypes.h>
void es2(){
	
	intmax_t a=888888888888888888;
	printf("intamx %" PRIdMAX "\n",a); //il % verrà completato da qualcosa che capirà il calcolatore
}


/*3. Scrivere un programma che:
dichiari unsigned int u = 0; e int s = -1;,
stampi il valore di u - 1, verifichi se s < u e spieghi il risultato.*/
void es3(){
	unsigned int u=0;
	int s=-1;
	printf("%u \n",u-1);
	printf("%d",(s<u));
}




/*5. Scrivere un programma che:
definisca un enum con flag READ, WRITE, EXEC come maschere di bit,
combini i permessi con |, li modifichi con & ~, stampi il risultato in binario
dopo ogni modifica.*/
typedef enum{
	READ = 1 << 0,	//0001		>> x oppure << x è uno shift di x bit
	WRITE = 1 << 1,	//0010
	EXEC = 1 << 2,	//0100
} Permission;

void printBits(int number){
	for(int i=7;i>=0;i--){
		printf("%d", (number >> i) & 1);	//se è 1 stampa 1 perche 1&1=1 altrimenti da 0
	}
	printf("\n");
}
void es5(){
	//una maschera di bit è un insieme di bit che interpretata definsisce qualche tipo di logica o comportamento.	

	Permission p=READ | WRITE;	//voglio che sia sia read che write 0001 | 0010 => 0011
	printBits(p);
	p = p | EXEC;
	printBits(p);
	p = p & ~(WRITE);	//disabilito la write, la tilde funziona come not
	printBits(p); 
	p = p & ~(WRITE);	//adesso se riprovo a disabilitare la write non succede più nulla
	printBits(p); 
}

/*4. Scrivere un programma che:
dichiari char c = 200; signed char sc = 200; unsigned char uc =
200;,stampi i tre valori, determini a runtime se char è interpretato come
signed o unsigned sulla piattaforma.
*/

void es4(){
	char c=200;
	signed char sc=200;
	unsigned char uc=200;

	printf("c:%d, sc:%d, uc:%d",c,sc,uc);
}


int main(){
	//es1();
	//es2();
	//es3();	
	es4();
	//es5();	//a cosa serve sta roba???  



	 return 0;
}
