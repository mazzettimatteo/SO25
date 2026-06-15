import os
import sys
import shutil

"""Scrivere uno script bash o python che faccia il merge di due alberi del file system copiandoli in un terzo.
La gerarchia risultante dovrebbe contenere tutti i file e le directory presenti nel primo o nel secondo albero.
Se due file hanno lo stesso percorso e nomi uguali nei due alberi di partenza i contenuti devono essere
concatenati nel file risultante"""

def main():
    if(len(sys.argv)!=4):
        print("Use: python merge2dirs.py <src_dir1/> <src_dir2/> <dest_dir/>")
        exit(1)
    
    try:
        os.mkdir(sys.argv[3])
    except(FileExistsError):
        print(f"{sys.argv[1]} esisteva già, non l'ho ricreata")

    for root,dirs,files in os.walk(sys.argv[1]):
        for d in dirs:
            relRoot=os.path.relpath(root,sys.argv[1])
            newDir=os.path.join(sys.argv[3],relRoot,d)
            os.makedirs(newDir, exist_ok=True)
        for f in files:
            fPath=os.path.join(root,f)
            relRoot=os.path.relpath(root,sys.argv[1])
            newFile=os.path.join(sys.argv[3],relRoot,f)
            shutil.copyfile(fPath,newFile)


    for root,dirs,files in os.walk(sys.argv[2]):
        for d in dirs:
            relRoot=os.path.relpath(root,sys.argv[2])
            newDir=os.path.join(sys.argv[3],relRoot,d)
            os.makedirs(newDir, exist_ok=True)
        for f in files:
            fPath=os.path.join(root,f)
            relRoot=os.path.relpath(root,sys.argv[2])
            newFile=os.path.join(sys.argv[3],relRoot,f)
            if(os.path.exists(newFile)):
                with open(fPath,"r") as sourceFile:
                    with open(newFile, 'a') as existingFile:
                        existingFile.write(sourceFile.read()+"\n")
            else:
                shutil.copyfile(fPath,newFile)



if __name__=="__main__":
    main()