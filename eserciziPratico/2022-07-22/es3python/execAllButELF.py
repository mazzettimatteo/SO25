import sys
import os
import subprocess

"""l programma python o lo script bash deve eseguire uno dopo l'altro tutti gli script presenti nella
directory passata come parametro (o la current directory se manca il parametro) ma non gli eseguibili
binari di tipo ELF."""

def isElf(filePath):
    with open(filePath,"rb") as file:
        content=file.read(4)
        if(content==(b'\x7fELF')):
            return 1
        else:
            return 0


def main():
    argc=len(sys.argv)
    if(argc==1):
        dir="."
    elif(argc==2):
        dir=sys.argv[1]
    else:
        print("Use: python execAllButElf.py [dir/]")
        exit(1)
    
    for root,dirs,files in os.walk(dir):
        dirs.clear() #dice nella dir, non nel sottoalbero
        for f in files:
            fPath=os.path.join(root,f)
            if(not isElf(fPath)):
                with open(fPath,"r") as file:
                    if(file.read(2)=="#!"):
                        subprocess.run(["bash",fPath])


'''Nota: in realtà il controllo isElf non serve se poi controllo se il file inizia con lo shebang #!, 
però andrebbe fatto in maniera binaria, così da non rischiare di aprire i file ELF inn un formato sbagliato
prima di fare il controllo: si possono sostituire da linea 32 a 35 come segue:

with open(fPath, "rb") as file:
    if(file.read(2)== b'#!' ):
        subprocess.run(["bash",fPath])


'''



if __name__=="__main__":
    main()