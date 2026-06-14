import os
import sys
import shutil

"""Scrivere uno script bash o python difidr che date due directory ne crei una terza e una quarta
Le nuove directory devono contenere solamente i file aventi lo stesso nome presenti nella prima e nella seconda
albero. Ogni file della terza directory deve contenere una copia del file nella versione della prima directory,
mentre nella quarta directory la versione della seconda.
es.
* se la direcotry a contiene i file alpha, beta, gamma, delta e la directory b i file beta, delta, epsilon, zeta
il comando "difdir a b newa newb" crea le directory newa e newb ed entrambe le directory devono
contenere solo beta e delta (i nomi in comune). newa/beta deve essere una copia di a/beta mentre
newb/beta una copia di b/beta. In modo simile per a/delta b/delta newa/delta e newb/delta."""


def main():
    if(len(sys.argv)!=5):
        print("Use: python difdr.py <dir_a/> <dir_b/> <new_a_dir/> <new_b_dir/>")
        exit(1)

    aContent={} #nomeFile->pathA

    shared={} #nome-> [pathA, pathB]

    for root,dirs,files in os.walk(sys.argv[1]):
        for f in files:
            aContent[f]=os.path.join(root,f)

    for root,dirs,files in os.walk(sys.argv[2]):
        for f in files:
            if(f in aContent.keys()):
                shared[f]=[(aContent[f]), os.path.join(root,f)]

    
    newA=sys.argv[3]
    newB=sys.argv[4]


    os.mkdir(newA)
    os.mkdir(newB)

    for f in shared.keys():
        
        shutil.copyfile(shared[f][0],os.path.join(newA,f))
        shutil.copyfile(shared[f][1],os.path.join(newB,f))
        print(f"File {f} copied")




if __name__=="__main__":
    main()