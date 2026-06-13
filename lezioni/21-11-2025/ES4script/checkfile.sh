#!/bin/bash

#Scrivi checkfile.sh che:
# usa cmp file /dev/null
# redirige l'output in /dev/null
# stampa se il file è vuoto
# visualizza l'exit status

#confronto con /dev/null, mando stdout(1) in null,
#poi redirigo(>&) stderr(2) nello steso posto di stdout(1)
cmp $1 /dev/null > /dev/null 2 >&  1
#salvo lo status
exitStatus=$?

#guardo se il file è vuoto
if [ $exitStatus -eq 0 ]; then
	echo "il file è vuoto"
else 
	echo "il fle non è vuoto"
fi

echo "exitStatus: $exitStatus"

