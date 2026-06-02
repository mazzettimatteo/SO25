import sys
import os

"""Scrivere un programma Python o uno script bash che presi come parametri i pathname di un file f e
di una directory d stampi l'elenco dei file che hanno la stessa ampiezza (numero di byte) di f ma non
sono link fisici di f presenti nel sottoalbero del file system generato dalla directory d."""

def main():
    if(len(sys.argv)!=3):
        print("Use: python samesize.py <file> <dir/>")
        exit(1)
    
    result=[]

    target=os.path.realpath(sys.argv[1])
    targetStat=os.stat(target)

    for root, dirs, files in os.walk(sys.argv[2]):
        for f in files:
            f=os.path.join(root, f)
            fStat=os.stat(f)
            if(fStat.st_ino == targetStat.st_ino):
                continue
            elif(fStat.st_size==targetStat.st_size):
                result.append(f)

    for r in result:
        print(r)


if __name__ == "__main__":
    main()