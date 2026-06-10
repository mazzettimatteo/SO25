import os
import sys

"""Scrivere un programma python o uno script bash che, passata una directory come parametro, cancelli
nel sottoalbero generato dalla directory passata come parametro tutti i link simbolici relativi (e non
cancelli quelli assoluti)
lrwxrwxrwx 1 renzo renzo 13 Jun 11 17:03 hostname1 -> /etc/hostname
lrwxrwxrwx 1 renzo renzo 15 Jun 11 17:04 hostname2 -> ../etc/hostname
il primo va mantenuto e il secondo cancellato"""

def main():
    if(len(sys.argv)!=2):
        print("Use: python rmrelsymlink.py <dir/>")
        exit(1)
    
    links=[]
    for root,dirs,files in os.walk(sys.argv[1]):
        for f in files:
            fPath=os.path.join(root,f)
            if(os.path.islink(fPath)):
                links.append(fPath)
            

    print("Removed links that are relative:")
    for lk in links:
        linkSrc=os.readlink(lk)
        if(not os.path.isabs(linkSrc)):
            os.remove(lk)
            print(lk)



if __name__=="__main__":
    main()