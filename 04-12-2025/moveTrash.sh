#!/bin/bash

#Sposta tutto ciò che finisce con ~ in trashFolder\

DIR_TRASH="./trashFolder/"

for file in `ls *~` #oppure potevo scrivere $(ls *~)
do
	echo $file
	mv $file $DIR_TRASH
done
