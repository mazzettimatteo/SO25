import os
import shutil

def main():
    base_dir = "test_mvclone_env"
    
    # Pulizia preventiva dell'ambiente
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        
    os.makedirs(base_dir)

    # 1. Creazione di file regolari
    file1 = os.path.join(base_dir, "documento.txt")
    with open(file1, "w") as f:
        f.write("Questo è il file originale numero 1.\n")

    file2 = os.path.join(base_dir, "immagine.png")
    with open(file2, "w") as f:
        f.write("Finto contenuto binario di una immagine.\n")

    # 2. Creazione di una directory (il programma C NON deve toccarla)
    os.makedirs(os.path.join(base_dir, "cartella_da_ignorare"))

    print(f"Ambiente di test generato con successo: {base_dir}")
    print("\nContenuto iniziale:")
    for item in os.listdir(base_dir):
        print(f" - {item}")

    print("\nComando da lanciare:")
    print(f"./mvclone {base_dir}")
    
    print("\n--- RISULTATO ATTESO DOPO L'ESECUZIONE ---")
    print("1. Deve esistere la cartella '...'.")
    print("2. I file 'documento.txt' e 'immagine.png' originali devono essere DIVENTATI LINK SIMBOLICI.")
    print("3. I link devono puntare a '.../documento.txt' (link RELATIVO).")
    print("4. 'cartella_da_ignorare' deve essere rimasta intatta e non deve essere un link.")

if __name__ == "__main__":
    main()