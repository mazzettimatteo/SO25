#!/usr/bin/env python3

import sys
import os


"""Scrivere un programma Python o uno script bash che, dati il pathname di un file f e di una directory d
stampi a seconda del proprio nome:
• l'elenco dei link simbolici che puntano a f presenti nella directory d se chiamato come cksimlink
cksymlink /tmp/file /tmp/dir
• l'elenco dei link fisici di f presenti nella directory d se chiamato come cklink
cklink /tmp/file /tmp/dir"""


"""
Per fare si che lo script risponda a due comandi seguire questo procedimento:
    - creare core_script.py con prima riga:
        #!/usr/bin/env python3
    - rendere eseguibile tale script con:
        chmod +x core_script.py
    - creare due link simbolici con nomi diversi collegati allo script:
        ln -s core_script.py cksymlink
        ln -s core_script.py cklink
    - nel programma python distinguere i casi in base al valore di argv[0]
"""


def main():
    if(len(sys.argv)!=3):
        print("Use: \n ./cksymlink <file> <dir/>    prints name of all softlink in dir that point to file \n /cklink <file> <dir/>    prints name of all hard link in dir that point to file\n")
        exit(1)
    target=os.path.abspath(sys.argv[1])
    result=[]
    if(sys.argv[0]=="./cksymlink"):
        for root, dirs, files in os.walk(sys.argv[2]):
            dirs.clear()
            for f in files:
                f=os.path.join(root, f)
                if(os.path.islink(f) and os.path.samefile(f,target)):
                    result.append(f)
        print("symlink list:")

    elif(sys.argv[0]=="./cklink"):
        targetStat=os.stat(target)
        for root, dirs, files in os.walk(sys.argv[2]):
            dirs.clear()
            for f in files:
                f=os.path.join(root, f)
                fStat=os.stat(f)
                if(os.path.islink(f)):
                    continue
                if(targetStat.st_ino==fStat.st_ino):
                    result.append(f)
        print("hlink list:")


    for r in result:
        print(r)



if __name__=="__main__":
    main()