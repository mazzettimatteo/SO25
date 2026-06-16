import sys
import os

"""Scrivere un programma pyhton o uno script bash che calcoli l'ampiezza totale in byte dei file
eseguibili ELF presenti in tutte le directory passate come parametri o nella directory corrente se non
viene specificato alcun parametro.
e.g.
$ elfsize /bin /usr/bin
1682573547"""

def main():

    argc=len(sys.argv)

    totSize=0
    

    if(argc==1):
        sys.argv.append(".")
        nDirs=2
    else:
        nDirs=argc

    for i in range(1,nDirs):#nel loop nDirs non è compreso
        for root,dirs,files in os.walk(sys.argv[i]):
            dirs.clear() #dice nelle dir, non nell'albero delle dir
            for f in files:
                fPath=os.path.join(root,f)
                with open(fPath, "rb") as file:
                    content=file.read(4) #mi interesssano i primi 4byte
                    #print(f"{content}\n-----------------------------------\n")
                    if(content==(b'\x7fELF')):
                        fStat=os.stat(fPath)
                        totSize+=fStat.st_size

    #print("\n\n\n\n........................")
    print(totSize)


if __name__=="__main__":
    main()