import sys
import os

"""Scrivere un programma python o uno script bash che data una directory produca un elenco dei file e
delle directory che non potrebbero essere copiati in file system che supportino solo caratteri ascii nei
nomi."""

def main():
    if(len(sys.argv)!=2):
        print("Use: python notascii.py <dir/>")
        exit(1)
    
    result=[]

    ''' SCANDIR NON È PER IMPLEMENTAZIONE RICORSIVA, BISOGNEREBBE SCRIVERE UNA FUNZIONE recScandir
        for entry in os.scandir(sys.argv[1]):
            entryPath=entry.path
            if(not entryPath.isascii()):
                result.append(entryPath)

        
    '''
    for root,dirs,files in os.walk(sys.argv[1]):

        for d in dirs:
            dPath=os.path.join(root,d)
            if(not dPath.isascii()):
                result.append(dPath)

        for f in files:
            fPath=os.path.join(root,f)
            if(not fPath.isascii()):
                result.append(fPath)
    
    for r in result:
            print(r)
            
        
'''Se volessi che controlla solo in nome del file e non il suo path bisognerebbe sostituire dPath e fPath semplicemente con d ed f'''
 
if __name__=="__main__":
    main()