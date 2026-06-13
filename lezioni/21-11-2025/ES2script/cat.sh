#!/bin/bash


#Scrivi cat.sh che usa un here-document per inviare:
#- un messaggio contenente le variabili $1 e $2.
#- mostra 'cat effettuato a <dest>' alla fine.

cat << EOF

l'arg1 è $1
l'arg2 è $2
EOF
#EOF=stringa scelta da me per segnare EndOfFile
#$i con i=1..n è la variabile che contiene l'argomento i


