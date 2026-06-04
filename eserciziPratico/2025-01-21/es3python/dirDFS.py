import os
import sys

"""Lo script o il programma Python deve fornire una lista dei file
all'interno di un sottoalbero del file system ordinati secondo la “profondità” a partire da quelli più
profondi, per ultimi quelli della directory radice. I nodi allo stesso livello devono essere ordinati in
ordine crescente del nome del file."""

def main():
    if(len(sys.argv)!=2):
        print("Use: python dirDFS.py <dir/>")
        exit(1)
    
    levels={}

    for root, dirs, files in os.walk(sys.argv[1]):
        normalizedRoot=os.path.normpath(root)
        depth=normalizedRoot.count(os.sep)

        if(depth not in levels):
            levels[depth]=[]

        for f in files:
            levels[depth].append((f,os.path.join(root,f)))
        
    depths=sorted(levels.keys(), reverse=True)

    for d in depths:
        temp=levels[d]
        temp.sort(key=lambda x: x[0])
        for t in temp:
            print(t[1])


if __name__=="__main__":
    main()