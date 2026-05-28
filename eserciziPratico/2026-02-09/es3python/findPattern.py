import os
import sys
#import subprocess
#import argparse
#import pathlib
#import pickle
#import invoke


#Scrivere uno script bash o un programma python che preso come parametro un pattern (stringa
#ASCII) fornisca in output l'elenco dei file del sottoalbero che ha come radice la directory corrente che
#nel loro contenuto includano il pattern.. La lista di output deve essere ordinata dal file con tempo di
#ultima modifica più antico al file con ultima modifica più recente.

def main():
    if(len(sys.argv)==3):
        searchDir=sys.argv[2]
    elif(len(sys.argv)==2):
        searchDir="."
    else:    
        print("USE: python findPattern.py <pattern> <directory>")
        print("Default directory is the current one(\'.\') ")
        sys.exit(1)
    
    pattern=sys.argv[1]
    result=[]

    for root, dirs, files in os.walk(searchDir):
        for f in files:
            fullPath=os.path.join(root,f) #genero il path completo di ogni file

            try:
                with open(fullPath, "r") as file: #apro quel file tramite path completo
                    content=file.read()
                    if(pattern in content): #se contiene il pattern lo salvo in una lista, con anche l'orario di modifica
                        lastModifiedSince=os.path.getmtime(fullPath)
                        result.append((fullPath,lastModifiedSince))
            except Exception:
                continue
    
    result.sort(key=lambda x: x[1]) #sort per lastModified

    for path,time in result:
        print(path)



if __name__ == "__main__":
    main()