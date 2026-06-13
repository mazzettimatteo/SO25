import os
import sys

"""Sia data una directory che contiene file di testo.
Scopo dell'esercizio e' di scrivere un programma Python o uno script bash chiamato ccpl che conti i
caratteri delle corrispondenti righe di testo di tutti i file della directory, si vuole cioe' sapere il numero
totale di caratteri presenti nelle prime righe di tutti i file, nelle seconde linee, ecc.
$ ccpl mydir
1 234
2 21
3 333
…..
l'ouput significa che se contiamo tutti i caratteri contenuti nella prima riga di tutti i file in mydir
otteniamo 234 (mydir/file1 puo' avere 40 caratteri nella prima riga, mydir/file2 ne puo' avere 20, ecc...
procedendo per tutti i file di mydir la somma fa 234)."""


def main():
    if(len(sys.argv)!=2):
        print("Use: python ccpl.py <dir/>")
        exit(1)

    result={} # nDiRiga->numChars 

    for root,dirs,files in os.walk(sys.argv[1]):
        dirs.clear() #dice solo della directory
        for f in files:
            f=os.path.join(root,f)
            with open(f,"r") as file:
                i=1
                for line in file:
                    if(i not in result.keys()):
                        result[i]=0
                    result[i]+=len(line) 
                    i+=1


    for k in result.keys():
        print(f"Linea {k}: {result[k]}")
    #notare che tutti i risultati possono essere sfalsati di uno se c'è un carattere newline '\n'


if __name__=="__main__":
    main()