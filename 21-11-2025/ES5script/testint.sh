#!/bin/bash

#Scrivi testint.sh che legge due interi e usa il test per:
# confrontare a e b (-gt, -eq, -lt)
# verificare se a è negativo
# usare una negazione: !

if [[ $1 -gt $2 ]]; then
	echo "A>B"
else 
	echo "A<=B"
fi

if test $1 -eq $2; then
	echo "A equals B"
elif [[ $1 -lt $2 ]]; then
	echo "A<B"
fi

if [[ ! $1 -eq $2 ]]; then
	echo "A!=B"
else
	echo "a==B"
fi
