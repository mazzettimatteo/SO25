#!/bin/bash
# tabelline
if [ "$1" -eq "" ]; then
	echo “Usage: $0 max”
	exit
fi
x=1
while [ $x -le $1 ]
do
	y=1
	while [ $y -le $1 ]
 	do
 		echo ‘expr $x \* $y‘ " "
 		y=‘expr $y + 1‘
 	done
 	echo
 	x=‘expr $x + 1‘
done



