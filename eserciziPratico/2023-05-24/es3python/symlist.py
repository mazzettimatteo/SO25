import sys
import os

"""Scrivere un programma python o uno script bash che cerchi all'interno di un sottoalbero se ci sono
link simbolici che indicano lo stesso file. (hint controllare se coincide il numero dell'i-node del file
indicato)."""

def main():
    if(len(sys.argv)!=2):
        print("Use: python symlist.py <dir/>")
        exit(1)
    

    dict={} #inode->listOfLinks[]
    '''
        12 -> link1, link3
        42 -> link2

        link3 => FileConInode12

    '''



    for root,dirs,files in os.walk(sys.argv[1]):
        for f in files:
            fPath=os.path.join(root,f)
            if(os.path.islink(fPath)):
                #target=os.readlink(fPath)
                targetStat=os.stat(fPath) #perché os.stat segue già i link
                targetInode=targetStat.st_ino
                if(targetInode not in dict.keys()):
                    dict[targetInode]=[]
                dict[targetInode].append(fPath)
    
    for inode in dict.keys():
        print(f"{inode}: ")
        for link in dict[inode]:
            print(link)

                






if __name__=="__main__":
    main()