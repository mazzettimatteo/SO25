#!/bin/bash

administrator(){
	echo "amministratore"
}
student(){
	echo "studente"
}
teacher(){
	echo "professore"
}

stop=0

while [[ $stop -eq 0 ]]
do
	cat << EOM
	1: admin
	2: student
	3: teacher
	0: quit
EOM

echo "whats your choice?"
read reply

if [[ "$reply" == "1" ]]; then
	administrator
elif [[ "$reply" == "2" ]]; then
	student
elif [[ "$reply" == "3" ]]; then
	teacher
elif [[ "$reply" == "0" ]]; then
	stop=1
else
	echo "error"
fi
done















