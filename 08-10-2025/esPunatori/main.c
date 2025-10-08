#include<stdio.h>
#include<stdlib.h>


/*
1. Dichiara una variabile intera, un puntatore che la referenzia e stampa: il
valore della variabile, l’indirizzo della variabile, il valore del puntatore, il valore
puntato.
*/
void es1(){
	int a=8;
	int * ptr=&a;

	printf("variabile %d, indirizzo variabile %p,indirizzo puntatore %p , valore puntato %d \n",a,&a,ptr,*ptr);
}


/*2. Scrivi una funzione swap(int *x, int *y) che scambi i valori di due
variabili. Testa la funzione nel main con due interi.*/

void swap(int *x, int *y){
	int temp=*x;
	*x=*y;
	*y=temp;
}
void es2(){
	int a=3;
	int b=7;
	printf("a:%d b:%d",a,b);
	swap(&a,&b);
	printf("a:%d b:%d",a,b);

}





/*3. Definisci la funzione int* genera_array(int n); che allochi
dinamicamente un array di n interi inizializzati a zero e ne restituisca il
puntatore. Usala nel main e stampa i valori.*/

int * genera_array(int n){
	int * A=NULL;
	A = (int*) malloc(n*sizeof(int)); //malloc???
	for(int i=0;i<n;i++){
		A[i]=0;
	}

	//oppure si poteva usare la calloc che inizializza direttamente quei valori a zero

	return A;
}

void printArray(int * A, int n){
	for(int i=0;i<n;i++){
		printf("%d, ",A[i]);
	}
	printf("\n");
}


void es3(){
	int dim;
	scanf("%d",&dim);
	int * array=genera_array(dim);
	printArray(array, dim);

}



/*4.Scrivi un programma che allochi dinamicamente una matrice di interi n × m, la
riempia con valori (es. random), la stampi in forma tabellare e liberi tutta la
memoria allocata.
*/
//DA FINIRE
int * creaMatrice(int n, int m){
	int * M=malloc(n*sizeof(int *));


	

	for(int i=0;i<n;i++){
		for(int * j=0;j<m;j++){
			M[i][j]=rand()%10;
		}
	}

	return M;
}


int main(){
	//es1();
	//es2();	
	//es3();
	

	return 0;
}