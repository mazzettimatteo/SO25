
#include<stdio.h>
#include<unistd.h>

int main(){	//capiamo ora come muore il processo, come finisce
	//la systemcall di suicidio dei processi è _exit, exit ritorna un int
	_exit(42);

	return 0;
}
