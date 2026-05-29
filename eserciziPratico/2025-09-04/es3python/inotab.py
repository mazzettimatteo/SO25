import sys
import os

#Questo programma scandisce il file system a partire dalla directory corrente e genera in output un
#elenco (una riga per ogni file o directory) contenente il numero di i-node e il pathname del file:
#6508 a
#6609 x/b
#6710 c
#6801 x
#L’elenco prodotto deve essere ordinato per valori crescenti del numero di i-node
#Il programma inotab può avere come parametro un numero intero che limita la profondità della scansione.
#Inotab → scandisce l’intero sottoalbero
#inotab 0 → scandisce solo la directory corrente
#inotab 1 → scandisce la directory corrente e le sottodirectory della dir corrente
#inotab 2 → scandisce anche le sottodirectory delle sottodirectory, ma non va oltre, 

def main():
    result=[]
    if len(sys.argv)==1:
        #scandisce intero sottoalbero
        for root,dirs,files in os.walk("."):
            for f in files:
                fullPath=os.path.join(root, f)
                result.append((os.stat(fullPath).st_ino, fullPath ))
            for d in dirs:
                fullPath=os.path.join(root, d)
                result.append((os.stat(fullPath).st_ino, fullPath ))
            fullPath=os.path.join(root, ".")
            result.append((os.stat(fullPath).st_ino,  fullPath ))

    elif (len(sys.argv)==2 and sys.argv[1]=="0"):
        #inotab 0 → scandisce solo la directory corrente
        for root,dirs,files in os.walk("."):
            dirs.clear()
            for f in files:
                fullPath=os.path.join(root, f)
                result.append((os.stat(fullPath).st_ino, fullPath ))
            fullPath=os.path.join(root, ".")
            result.append((os.stat(fullPath).st_ino,  fullPath ))

    elif (len(sys.argv)==2 and sys.argv[1]=="1"):
        #inotab 1 → scandisce la directory corrente e le sottodirectory della dir corrente
        
        for root,dirs,files in os.walk("."):

            currDepth=root.count(os.sep)

            if(currDepth==0): #pari a zero all'inizio perché si stanno usando indirizzi relativi
                result.append((os.stat(root).st_ino, root))

            for f in files:
                fullPath=os.path.join(root, f)
                result.append((os.stat(fullPath).st_ino, fullPath ))
            
            for d in dirs:
                fullPath=os.path.join(root, d)
                result.append((os.stat(fullPath).st_ino, fullPath ))

            if currDepth>=1:
                dirs.clear()


    elif (len(sys.argv)==2 and sys.argv[1]=="2"):
        #inotab 2 → scandisce anche le sottodirectory delle sottodirectory, ma non va oltre
        
        for root,dirs,files in os.walk("."):

            currDepth=root.count(os.sep)

            if(currDepth==0): 
                result.append((os.stat(root).st_ino, root))

            for f in files:
                fullPath=os.path.join(root, f)
                result.append((os.stat(fullPath).st_ino, fullPath ))
            
            for d in dirs:
                fullPath=os.path.join(root, d)
                result.append((os.stat(fullPath).st_ino, fullPath ))

            if currDepth>=2:
                dirs.clear()

    else:
        print("Use: python inotab.py [0,1,2]")
        sys.exit(1)
    
    result.sort(key=lambda x: x[0]) #sort per inode num

    for inode, path in result:
        print(inode, path)


if __name__=="__main__":
    main()