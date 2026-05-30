import os
import sys
import filecmp

"""Scrivere un programma Python o uno script bash dremcont.
dremcont ha due parametri: un file f e una directory d. Tutti i file nella directory d e nelle sue
sottodirectory che hanno contenuto uguale a f devono essere cancellate."""

def main():
    if(len(sys.argv)!=3):
        print("Use: python dremcont.py <file> <dir/>")
    target=os.path.abspath(sys.argv[1])
    directory=os.path.abspath(sys.argv[2])
    removedFiles=[]
    remainingFiles=[]

    for root, dirs, files in os.walk(directory):
        for f in files:
            fPath=os.path.join(root, f)
            if(filecmp.cmp(target, fPath, shallow=False)): 
                #Shallow=false permette di confrontare tutto il contenuto, altrimenti filecmp contronta solo le os.stat 
                removedFiles.append(fPath)
                os.remove(fPath)
            else:
                remainingFiles.append(fPath)

    print("Remove files that are identical to: ", sys.argv[1])
    for file in removedFiles:
        print(file)
    print("Remainig files: ")
    for file in remainingFiles:
        print(file)




if __name__ == "__main__":
    main()