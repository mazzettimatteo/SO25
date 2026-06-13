#Scrivi calc.sh che calcola somma, differenza e prodotto di $1 e $2 usando
#expr. Aggiungi anche il confronto A > B.

sum=$(expr $1 + $2)
diff=$(expr $1 - $2)
mult=$(expr $1 \* $2)
comp=$(expr $1 \<= $2)

echo $sum
echo $diff
echo $mult
echo $comp 

