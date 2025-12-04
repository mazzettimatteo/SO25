#!/bin/bash
#Scrivere uno script che abbia le funzionalità di rm, ma che invece di cancellare
#definitivamente i file li sposti in una directory .trash nella vostra home
#• Usage:
#• saferm –L elenca il contenuto del cestino
#• saferm –P svuota (“purge”) il cestino
#• saferm –R files ripristina il file file
#• saferm files rimuove i file spostandoli nel cestino
#• Nota: le varie opzioni sono esclusive; ovvero, non si può lanciare un comando
#saferm –L –P ; generate un errore e stampate l’usage dello script nel caso
#Gestione di file con lo stesso nome:
#• se un nome di file da inserire nel cestino esiste già, rinominare il file esistente concatenando la sua data
#• suggerimento: utilizzate date –r +%s
#• Esempio:
#• Se nel cestino c’è un file prova.sh, e volete aggiungere un altro file prova.sh,
# rinominate il primo come “prova.sh.1030606290” e poi spostate il secondo nel cestino
#- Estensioni
#• tenete conto della possibilità di ripristinare file precedenti

#-----------INIZIALIZZAZIONE-----------

TRASH_DIR=trashForSAFERM/
RIPRISTINATI=fileRipristinati/

#----GESTIONE PARAM--------
case $1 in
	"-L") ls $TRASH_DIR
	;;
	"-P") rm $TRASH_DIR*
	;;
	"-R")  
		mv $TRASH_DIR$2 $RIPRISINATI
	;;
esac






