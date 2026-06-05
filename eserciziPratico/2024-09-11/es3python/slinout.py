import sys
import os

"""Scrivere un programma Python o uno script bash slinout che elenchi tutti i link simbolici presenti nel
sottoalbero del file system che ha come radice la directory passata come parametro (o la current
working directory se slinout viene chiamato senza parametri).
I link simbolici devono essere suddivisi in interni, che cioè puntano ad altro file o directory nel
sottoalbero considerato, o esterni, che cioè indicano un file o directory al di fuori del sotoalbero.
(attenzione: il target dei link simbolici può essere assoluto o relativo)"""

def main():
    if(len(sys.argv)>2):
        print("Use: \npython slinout.py for the current dir, or\npython slinout.py <dir/> for the specified dir ")
        exit(1)
    
    if(len(sys.argv)==1):
        targetDir="."
    else: 
        targetDir=sys.argv[1]

    targetDirFiles=[]

    for root, dirs, files in os.walk(targetDir):

        rootPath=os.path.abspath(root)
        if(rootPath not in targetDirFiles): #serve perché esistono anche i link a dir e non solo ai file
            targetDirFiles.append(rootPath)

        for f in files:
            fPath=os.path.join(root,f)
            fPath=os.path.abspath(fPath)
            
            if not os.path.islink(fPath):
               targetDirFiles.append(fPath)


    internalLinks=[]
    externalLinks=[]
    for root, dirs, files in os.walk(targetDir):
        for f in files:
            fPath=os.path.join(root,f)
            fPath=os.path.abspath(fPath)

            if os.path.islink(fPath):
                linkSrc=os.readlink(fPath) #ottengo l'indirizzo a cui punta il link
                linkSrc=os.path.join(root, linkSrc) #lo rendo assoluto 
                linkSrc=os.path.abspath(linkSrc)

                if(linkSrc in targetDirFiles): #guardo se è dentro la targetDir
                    internalLinks.append(fPath)
                else:
                    externalLinks.append(fPath)

    print("Internal links:")
    for l in internalLinks:
        print(l)
    print("----------")
    print("External links:")
    for l in externalLinks:
        print(l)


if __name__=="__main__":
    main()

"""Nota bene: non era necessario pre-esplorare l'albero di targetDir. Basta: 
- salvarsi path assoluto di targetDir
- usare os.readlink sui file che sono link ottenendo realPath
- controllare se realPath contiene il path assoluto di targetDir  """

