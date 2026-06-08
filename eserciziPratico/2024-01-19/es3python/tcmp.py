import sys
import os

"""Scrivere un programma python o uno script bash chiamato tcmp che confronti gli alberi del file
system di due directory.. A seconda del parametro deve elencare i pathname di file e di directory che
• sono comuni ad entrambi i sottoalberi, se manca il parametro
• esistono solo nel primo sottoalbero, se il parametro è -1
• esistono solo nel secondo sottoalbero se il parametro è -2
esempi:
$ . /tcmp dir1 dir2
stampa l'elenco dei path che esistono sia in dir1 sia in dir2
$ . /tmcp -1 dir1 dir2
stampa l'elenco dei path che esistono in dir1 ma non in dir2"""

def main():
    argc=len(sys.argv)
    if(argc<3):
        print("Use: python tcmp.py <dir1> <dir2> [-1|-2]")
        exit(1)

    content1=[] 
    for root,dirs,files in os.walk(sys.argv[1]):
        for d in dirs:
            dPath = os.path.join(root, d)
            content1.append(os.path.relpath(dPath, sys.argv[1]))
    
        for f in files:
            fPath=os.path.join(root,f)
            content1.append(os.path.relpath(fPath,sys.argv[1]))


    content2=[] #coppie inode, path
    for root,dirs,files in os.walk(sys.argv[2]):
        for d in dirs:
            dPath = os.path.join(root, d)
            content2.append(os.path.relpath(dPath, sys.argv[2]))

        for f in files:
            fPath=os.path.join(root,f)
            content2.append(os.path.relpath(fPath, sys.argv[2]))


    if(argc==3):
        for c in content1:
            if c in content2:
                print(c)
    elif(sys.argv[3]=="-1"):
        for c in content1:
            if c not in content2:
                print(c)
    elif(sys.argv[3]=="-2"):
        for c in content2:
            if c not in content1:
                print(c)
    


if __name__=="__main__":
    main()