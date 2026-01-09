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
META_FILE=trashForSAFERM/.supportFile
optCont=0


mkdir -p $TRASH_DIR
mkdir -p $RIPRISTINATI
touch $META_FILE

countOption(){
	if [[ "$1" == "-P" || "$1" == "-R" || "$1" == "-L" ]]; then
		((optCont++))
	fi
	if [[ "$2" == "-P" || "$2" == "-R" || "$2" == "-L" ]]; then
		((optCont++))
	fi 

	if [[ $optCont -ge 2 ]]; then
		echo "error: multiple options"
		exit 1
	fi
}


restoreFile(){
	local file="$1"
	local fileNoDots=$(basename "$file")
	
	#echo "$fileNoDots"
	if [[ -z "$fileNoDots" ]]; then
		echo "error: inserire nome di un file"
		return 1
	fi
	
	if [[ -f "$TRASH_DIR/$fileNoDots" ]]; then

		local originalPath=$(grep "$file|" "$META_FILE" | cut -d'|' -f2)
		originalPath=$(realpath "$originalPath")
		#echo "$originalPath"
		#grep "pattern" "where" 
		# -d'|' dice che il delimitatore del cut è la "|" e -f2 gli dice di prendere la seconda parte del taglio

		mv "$TRASH_DIR/$fileNoDots" "$originalPath"
		echo "File $file ripristinato"
	else
		echo "error il file non è in $TRASH_DIR"
	fi
}

removeFile(){
	local file="$1"
	file=($basefile "$file")
	local fullPath=$(pwd)/"$file"
	if [[ -z "$fullPath" ]]; then
		echo "error: inserire file esistente"
		return 1
	else
		mv $fullPath $TRASH_DIR
		echo "$file|$fullPath" >> "$META_FILE"  
	fi
}

#----GESTIONE PARAM--------

countOption "$1" "$2" #if there are multiple options eg saferm -L -P quits

case $1 in
	"-L") 
		ls $TRASH_DIR #list trash content
	;;
	"-P") 
		rm $TRASH_DIR* #purge tash bin
	;;
	"-R")  #restore file
		restoreFile "$2"
	;;
	*)
		removeFile "$1"
	;;
esac






