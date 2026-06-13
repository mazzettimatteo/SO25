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
int ** creaMatrice(int n, int m){
	int ** M=malloc(n*sizeof(int *));
	for(int i=0;i<n;i++){
		M[i]=calloc(m,sizeof(int));
	}

	return M;
}

void printMatrix(int ** M, int n, int m){
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			printf("%d",M[i][j]);
		}
		printf("\n");
	}
}

void freeMem(int ** M,int n,int m){
	for(int i=0;i<n;i++){
		free(M[i]);
	}
	free(M);
}

void es4(){
	int righe=4, colonne=6;
	int ** A=creaMatrice(righe,colonne);
	printMatrix(A,righe,colonne);
	printf("%p \n",&A);
	freeMem(A,righe,colonne);
	printf("%p \n",&A);
	
}


/*5. Definisci una struttura Node con campo value e puntatore next.
Implementa le funzioni:
o insert_head per inserire un nodo in testa,
oprint_list per stampare tutti gli elementi,
ofree_list per deallocare la lista*/

struct Node{
	int val;
	struct Node * next;
};
typedef struct Node * pnode;

//struttura alternativa
typedef struct{
	int value;
	lista * next;
}lista;


pnode headInsert(pnode p, int value){
	pnode temp=malloc(sizeof(struct Node));
	temp->val=value;
	temp->next=p;
	return temp;
}

void printList(pnode p){
	while(p!=NULL){
		printf("%d ",p->val);
		p=p->next;
	}
}

void freeList(pnode p){

	while(p!=NULL){
		pnode temp=p;
		p=p->next;
		free(temp);
	}
}

void es5(){
	pnode h=NULL;
	for(int i=0;i<5;i++){
		h=headInsert(h,i);
	}
	printList(h);
	freeList(h);
		
	
}


int main(){
	//es1();
	//es2();	
	//es3();
	//es4();
	es5();
	
	

	return 0;
}