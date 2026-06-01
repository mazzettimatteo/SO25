import os
import shutil

def main():
    base_dir = "ambiente_test"
    target_file = os.path.join(base_dir, "file_target.txt")
    target_dir = os.path.join(base_dir, "directory_d")
    
    # 1. Pulizia preventiva (se la cartella esiste già, la ricreiamo pulita)
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    
    os.makedirs(target_dir)

    # 2. Creazione del file target (f)
    with open(target_file, "w") as f:
        f.write("Questo è il file target originale.\nIl suo inode è unico.\n")
        
    # 3. Creazione di un file "esca" normale
    file_esca = os.path.join(target_dir, "file_normale.txt")
    with open(file_esca, "w") as f:
        f.write("Sono un file normale, non un link.\n")

    # 4. Creazione dell'HARD LINK reale (cklink deve trovarlo)
    hardlink_reale = os.path.join(target_dir, "hardlink_valido")
    os.link(target_file, hardlink_reale)
    
    # 5. Creazione di un HARD LINK "esca" (stesso contenuto, ma file diverso)
    # Copiamo il file brutalmente per avere stesso testo ma inode diverso
    hardlink_falso = os.path.join(target_dir, "hardlink_falso")
    shutil.copy2(target_file, hardlink_falso)

    # 6. Creazione del SYMLINK reale (cksymlink deve trovarlo)
    symlink_reale = os.path.join(target_dir, "symlink_valido")
    # Usiamo il path assoluto per evitare problemi di risoluzione
    os.symlink(os.path.abspath(target_file), symlink_reale)

    # 7. Creazione di un SYMLINK "esca" (punta al file normale, non al target)
    symlink_falso = os.path.join(target_dir, "symlink_falso")
    os.symlink(os.path.abspath(file_esca), symlink_falso)

    print(f"Ambiente di test generato con successo nella cartella: {base_dir}/")
    print(f"-> File target 'f': {os.path.abspath(target_file)}")
    print(f"-> Directory 'd': {os.path.abspath(target_dir)}")
    print("\nFile generati dentro 'd':")
    for item in os.listdir(target_dir):
        print(f"  - {item}")

if __name__ == "__main__":
    main()