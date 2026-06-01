import sys
import os


"""Scrivere un programma python o uno script bash che aggiunga
alcune righe di testo all'inizio di tutti i file C, bash, python presenti nella directory specificata
(riconoscibili dal suffisso .c .sh o .py)
Il testo deve comparire come commento coerentemente con la sintassi del linguaggio:
• per i file sorgente C: /* .... */
• per gli script bash: linee con prefisso # (dopo se esiste la prima riga #!)
• per i file sorgente python: ''' .... '''
"""


#idea: copio il conenuto del file, creo un file identico in cui faccio append 
# del comment e poi reinserisco il contenuto
def main():

    if(len(sys.argv)!=3):
        print("Use: python addComment.py <multi_line_string> <dir/>")
        exit(1)

    content=sys.argv[1]
    
    for root,dirs,files in os.walk(sys.argv[2]):
            dirs.clear()
            for f in files:
                f=os.path.join(root, f)

                if(f.endswith(".c")):
                    comment="/* \n" + content +"\n */\n"
                    with open(f,mode="r") as file:
                       text=file.read()
                    with open(f,mode="w") as file:
                        file.write(comment)
                        file.write(text)


                elif(f.endswith(".py")):
                    comment=" ''' \n" + content +"\n '''\n "
                    with open(f,mode="r") as file:
                       text=file.read()
                    with open(f,mode="w") as file:
                        file.write(comment)
                        file.write(text)
                    
                elif(f.endswith(".sh")):
                    #bash script, commenti con # dopo riga 1 che contiene metodo di compilazione
                    comment="#" + content.replace("\n","\n#") + "\n"
                    with open(f,mode="r") as file:
                       text=file.read()
                    
                    firstLine=""
                    if text.startswith("#!"):
                        for ch in text:
                            if(ch!="\n"):
                                firstLine+=ch
                            else: 
                                break
                    with open(f,mode="w") as file:
                        if(len(firstLine)!=0):
                            file.write(firstLine + "\n")
                        file.write(comment)
                        file.write(text)



if __name__=="__main__":
    main()