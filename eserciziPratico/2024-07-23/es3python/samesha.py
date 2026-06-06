import sys
import os
import hashlib

"""Scrivere uno script che prende in input da linea di comando il nome di due directory ed elimina (da
entrambe le directory) tutti i file che hanno la stessa hash sha1. Più precisamente se c'è un file nella
prima directory e uno nella seconda che hanno la stessa hash sha1 tutti i file che hanno la stessa hash
sha1 presenti nelle due directory vanno cancellati.
(Se esistono file con la stessa hash sha1 ma solo in una delle due directory, non sono da cancellare.)"""


def main():
    if(len(sys.argv)!=3):
        print("Use: python samesha.py <dir1/> <dir2/>")
        exit(1)

    dir1=os.path.realpath(sys.argv[1])
    dir2=os.path.realpath(sys.argv[2])

    result1={} #dict: filePath -> sha

    for root, dirs, files in os.walk(dir1):
        dirs.clear() #dice nella directory, non nell'albero che ha come radice la directory
        for f in files:            
            filePath=os.path.join(root,f)
            filePath=os.path.abspath(filePath)

            with open(filePath, 'rb') as file: #Uso "with open as file" invece che file=open così poi si chiude da solo il file 
                fileContent=file.read()
                fileHash=(hashlib.sha1(fileContent)).hexdigest()
                if(fileHash not in result1.keys()):
                    result1[fileHash]=[]
                result1[fileHash].append(filePath)

    toRemove=set()

    for root, dirs, files in os.walk(dir2):
        dirs.clear()
        for f in files:
            filePath=os.path.join(root,f)
            filePath=os.path.abspath(filePath)

            with open(filePath, 'rb') as file: 
                fileContent=file.read()
                fileHash=(hashlib.sha1(fileContent)).hexdigest()
                if(fileHash in result1.keys()):
                    toRemove.update(result1[fileHash]) #update è l'operazione di add su tutti gli elem di una list
                    toRemove.add(filePath)
    
    for f in toRemove:
        print("Removing " + f)
        os.remove(f)



if __name__ == "__main__":
    main()

# Al posto di usare libreria hashlib posso importare il modulo subprocess
# e invocare subprocess.run([sha1sum, filePath], capture_output=True, text=True)
# sha1sum di Linux restituisce una stringa strutturata in questo modo: <hash_esadecimale>  <percorso_del_file>\n
# quindi per avere solo l'hash uso il metodo .stdout per ottenere il val di ritorno di subprocess.run
# e poi splittarla in corrispondenza degli spazi con .split() in una lista e prendere l'elemento [0] 