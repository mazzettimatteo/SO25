#!/bin/bash

# stampa utenti che consumano piu’ spazio su HD
case "$1" in #switch($1)
	"") lines=50 #nulla inserito
;;
	*[!0-9]*) echo "Usage: `basename $0` usersnum"; #inserito num fatto da cifre 1-9
exit 1
;;
	*) lines=$1 #caso default
;;

esac

#finito il case(lo switch) faccio du(comando che guarda lo spazio occupato delle dir in home/), poi le sorto, poi head -$lines stampa le prime $lines righe
du -s /tmp/* | sort -gr | head -$lines


