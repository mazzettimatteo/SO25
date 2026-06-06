import sys
import subprocess
import os

"""Scrivere un programma o uno script lscmd che consenta ad un utente di poter avere l'elenco di tutti i
pid dei suoi processi in esecuzione raggruppati per pathname del programma eseguito..
Es:
$ lscmd
/usr/bin/bash 2021 2044
/usr/bin/xterm 2010
"""

def main():
    if(len(sys.argv)!=1):
        print("Use: python lscmd.py")
        exit(1)
    
    result={} #map cmd/path/ -> pid_list[]


    ps=subprocess.run(["ps", "-x"],text=True,capture_output=True)
    for line in ps.stdout.splitlines():
        if (not line):
            continue
        pid=line.split()[0]
        cmd=os.path.join("/proc",pid,"exe")
        try:
            cmdPath=os.readlink(cmd)
            if(cmdPath not in result.keys()):
                result[cmdPath]=[]
        
            result[cmdPath].append(pid)
        except(Exception):
            continue

    
    for k in result.keys():
        print(k+":", end=" ")
        for r in result[k]:
            print(r,end=" ")
        print("")

if __name__=="__main__":
    main()