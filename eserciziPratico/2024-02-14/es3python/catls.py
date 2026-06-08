import sys
import os
import subprocess

"""Scrivere un programma python o uno script bash che crei un catalogo dei file presenti nella directory
passata come parametro (o la directory corrente se manca il parametro).
Il catalogo deve essere ordinato in categorie in base alla stringa ritornata dal comando 'file'.
Es:
$ catls
ASCII text:
testo1
favourites.txt
directory:
mydir
lib
Unicode text, UTF-8 text:
unitesto"""

def main():
    argc=len(sys.argv)
    workingDir=""
    if(argc>2):
        print("Use: python ./catls [dir/]       (default dir is '.')")
        exit(1)
    elif(argc==1):
        workingDir="."
    else:
        workingDir=sys.argv[1]

    result={} #dict typeOfFile -> listOfFiles[]

    for root, dirs, files in os.walk(workingDir):
        dirs.clear() #deve lavorare solo nella dir corrente, non anche nelle sotto dir
        for f in files:
            f=os.path.join(root,f)
            cmd=subprocess.run(["file", f],capture_output=True, text=True)
            currFile=cmd.stdout.split(": ")[0]
            descriptions=cmd.stdout.split(": ")[1].split(", ")
            for k in descriptions:
                if(k not in result.keys()):
                    result[k]=[]
                result[k].append(currFile)
    
    for k in result.keys():
        print(k)
        for r in result[k]:
            print(r)

        print("-------")

"""Il codice funziona ma non lista le directory(risolvi iterando con os.scandir o os.listdir al posto di o.walk),
inoltre separa i testi Unicode da UTF-8, al posto di fare .split(", ") era meglio usare .strip(...)"""



if __name__=="__main__":
    main()