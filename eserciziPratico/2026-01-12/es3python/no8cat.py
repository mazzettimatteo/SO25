import sys

#Scrivere un programma python o uno script bash che copi un file di testo UTF-8. Nella copia i caratteri
#non ASCII devono essere sostituiti con "?".
#Es: no8cat filein fileout
#se filein contiene: "cioè I Y💖"
#fileout dovrà essere: "cio? I?Y"

def main():
    if(len(sys.argv) != 2):
        print("Uso: python no8cat.py \"sting with weird chars(non UTF-8) è💖ç§\" ")
        sys.exit(1)
    str=sys.argv[1]
    
    for char in str:
        if char.isascii():
            print(char, end='')
        else:
            print('?', end='')
    print("\n")

        




if __name__ == "__main__" :
    main()