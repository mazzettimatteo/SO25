import os
import shutil

def main():
    base_dir = "test_undomvclone_env"
    clone_dir = os.path.join(base_dir, "...")
    
    # Pulizia preventiva
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        
    # Ricreiamo la struttura post-mvclone
    os.makedirs(clone_dir)

    # 1. CASO VALIDO: File reale in '...' e symlink relativo nella base
    real_file1 = os.path.join(clone_dir, "documento.txt")
    with open(real_file1, "w") as f:
        f.write("Contenuto reale del documento 1.\n")
    
    symlink1 = os.path.join(base_dir, "documento.txt")
    os.symlink(os.path.join("...", "documento.txt"), symlink1)

    # 2. CASO VALIDO 2: Un altro file
    real_file2 = os.path.join(clone_dir, "immagine.png")
    with open(real_file2, "w") as f:
        f.write("Contenuto reale immagine.\n")
        
    symlink2 = os.path.join(base_dir, "immagine.png")
    os.symlink(os.path.join("...", "immagine.png"), symlink2)

    # 3. ESCA 1: Un file regolare appena creato nella dir principale (NON deve essere toccato)
    esca_file = os.path.join(base_dir, "file_nuovo.txt")
    with open(esca_file, "w") as f:
        f.write("Questo file non c'entra con mvclone.\n")

    # 4. ESCA 2: Un symlink che punta da un'altra parte (NON deve essere toccato)
    esca_symlink = os.path.join(base_dir, "link_falso")
    os.symlink("file_nuovo.txt", esca_symlink)

    print(f"Ambiente di test generato con successo: {base_dir}")
    print("\nStruttura attuale:")
    print(" test_undomvclone_env/")
    print(" ├── .../                 (contiene i file reali)")
    print(" │   ├── documento.txt")
    print(" │   └── immagine.png")
    print(" ├── documento.txt        (symlink -> .../documento.txt)")
    print(" ├── immagine.png         (symlink -> .../immagine.png)")
    print(" ├── file_nuovo.txt       (esca - file regolare)")
    print(" └── link_falso           (esca - symlink -> file_nuovo.txt)")

    print("\nComando da lanciare per testare:")
    print(f"./undomvclone {base_dir}")
    
    print("\n--- RISULTATO ATTESO ---")
    print("1. I symlink 'documento.txt' e 'immagine.png' devono essere sostituiti dai file reali.")
    print("2. La cartella '...' dovrebbe rimanere vuota (i file sono stati spostati).")
    print("3. 'file_nuovo.txt' e 'link_falso' devono rimanere intatti.")

if __name__ == "__main__":
    main()