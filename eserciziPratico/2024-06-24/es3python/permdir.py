import sys
import os
import subprocess

"""Scrivere un programma python o uno script bash chiamato permdir. permdir prende come
parametro il pathname di una directory e crea nella directory corrente(io uso ./permdir) una directory per stringa di
permessi contenente link simbolici ai file con tali permessi.
es: se /tmp/dir è la directory passata come parametro e:
ls -l /tmp/dir
-rw-r--r-- 1 renzo renzo 0 Jun 20 13:23 due
-rw-r----- 1 renzo renzo 0 Jun 20 13:23 quattro
-rwx------ 1 renzo renzo 0 Jun 20 13:23 tre
-rwx------ 1 renzo renzo 0 Jun 20 13:23 uno
il comando permdir deve creare tre directory:
-rw-r--r-- che contiene il link due che punta a /tmp/dir/due
-rw-r----- che contiene il link quattro che punta a /tmp/dir/quattro
-rwx------ che contiene due link uno e tre che puntano agli omonimi file in /tmp/dir
(gestire solo il caso di file, no directory o file speciali)"""

def main():
    if(len(sys.argv)!=2):
        print("Use: python permdir.py <dir/>")
        exit(1)
    
    permessi={} # nomeVero->permesso

    argDir=os.path.abspath(sys.argv[1])
    ls=subprocess.run(["ls","-l",argDir], capture_output=True, text=True)
    for line in ls.stdout.splitlines():
        if (not line) or line.startswith("total") or (not line.startswith("-")): 
            continue
        perm=line.split()[0]
        trueName=line.split()[8] #perché il nome è il nono campo
        permessi[trueName]=perm

    if not os.path.exists(".permdir/"):
        os.mkdir(".permdir/")
    
    for p in permessi.values(): #creo una dir per ogni combinazione di permessi che ci sono
        if(not os.path.exists(".permdir/"+p)):
            os.mkdir(".permdir/"+p)
    
    for trueName in permessi.keys(): #perogni nome vero creo link da fileVero a link in cartella con nome permesso
        os.symlink(os.path.join(argDir,trueName),
                    os.path.join(".permdir/",permessi[trueName],trueName))
    



if __name__=="__main__":
    main()