import sys
import os

"""Scrivere un programma python o uno script bash che data una directory passata come parametro
produca una lista dei link simbolici presenti nel sottoalbero che fanno riferimento allo stesso file.
Esempio, in questo caso:
$ ls -lR /tmp/test
/tmp/test:
total 4
drwxr-xr-x 2 renzo renzo 4096 Sep 10 15:45 d
-rw-r--r-- 1 renzo renzo 0 Sep 10 15:41 file1
-rw-r--r-- 1 renzo renzo 0 Sep 10 15:41 file2
lrwxrwxrwx 1 renzo renzo 5 Sep 10 15:42 sl1 -> file1
lrwxrwxrwx 1 renzo renzo 5 Sep 10 15:42 sl1bis -> file1
lrwxrwxrwx 1 renzo renzo 5 Sep 10 15:49 sl2 -> file2
/tmp/test/d:
total 0
lrwxrwxrwx 1 renzo renzo 15 Sep 10 15:45 gsld -> /tmp/test/file1
lrwxrwxrwx 1 renzo renzo 8 Sep 10 15:43 sld -> ../file1
il programma lanciato con parametro /tmp/test deve trovare che sl1, sl1bis, d/sld e d/gllsd indicano lo
stesso file. (similmente dovrebbe rilevare altri insiemi di link simbolici che indicano lo stesso file"""

def main():
    if(len(sys.argv)!=2):
        print("Use: python listlink.py <dir/>")
        exit(1)
    

    inodeToLink={} #inode->linkList[]
    inodeToFile={} 

    for root,dirs,files in os.walk(sys.argv[1]):
        for f in files:
            fPath=os.path.join(root,f)
            fStat=os.stat(fPath)
            if(os.path.islink(fPath)):
                linkSrc=os.readlink(fPath)
                srcInode=fStat.st_ino
                if(srcInode not in inodeToLink.keys()):
                    inodeToLink[srcInode]=[]
                    inodeToFile[srcInode]=linkSrc
                inodeToLink[srcInode].append(fPath)

    for ino in inodeToFile.keys():
        print(inodeToFile[ino]+": ")
        for lk in inodeToLink[ino]:
            print("- "+lk)

if __name__=="__main__":
    main()