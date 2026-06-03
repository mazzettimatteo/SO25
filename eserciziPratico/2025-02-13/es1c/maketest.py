import os
import shutil

def main():
    base_dir = "test_ckfile_env"
    
    # Percorsi assoluti per evitare ambiguità
    abs_base_dir = os.path.abspath(base_dir)
    target_file = os.path.join(abs_base_dir, "file_target.txt")
    target_dir = os.path.join(abs_base_dir, "dir_d")
    sub_dir = os.path.join(target_dir, "sottocartella")
    
    # Pulizia preventiva
    if os.path.exists(abs_base_dir):
        shutil.rmtree(abs_base_dir)
    os.makedirs(sub_dir)
    
    # 1. Creazione del file TARGET f
    with open(target_file, "w") as f:
        f.write("Questo è il file target (f) da cercare.\n")
        
    # 2. Creazione di un file ESCA
    file_esca = os.path.join(target_dir, "file_esca_qualsiasi.txt")
    with open(file_esca, "w") as f:
        f.write("Sono un file diverso con un altro inode.\n")

    # --- LIVELLO 1: Cartella principale (dir_d) ---
    
    # SYMLINK VALIDO
    symlink_valido_1 = os.path.join(target_dir, "symlink_valido_1")
    os.symlink(target_file, symlink_valido_1)
    
    # HARDLINK VALIDO
    hardlink_valido_1 = os.path.join(target_dir, "hardlink_valido_1")
    os.link(target_file, hardlink_valido_1)
    
    # SYMLINK ESCA (punta al file esca)
    symlink_esca = os.path.join(target_dir, "symlink_esca")
    os.symlink(file_esca, symlink_esca)

    # --- LIVELLO 2: Sottocartella (dir_d/sottocartella) ---
    
    # SYMLINK VALIDO SOTTORETE
    symlink_valido_2 = os.path.join(sub_dir, "symlink_valido_2")
    os.symlink(target_file, symlink_valido_2)
    
    # HARDLINK VALIDO SOTTORETE
    hardlink_valido_2 = os.path.join(sub_dir, "hardlink_valido_2")
    os.link(target_file, hardlink_valido_2)
    
    # HARDLINK ESCA SOTTORETE (stesso inode del file esca, non del target)
    hardlink_esca_sub = os.path.join(sub_dir, "hardlink_esca_sub")
    os.link(file_esca, hardlink_esca_sub)

    # Output dei percorsi per facilitare i test manuali
    print("Ambiente di test generato con successo!\n")
    print("Target f: " + target_file)
    print("Target d: " + target_dir)
    print("\n--- RISULTATI ATTESI ---")
    print("Se chiami il programma con l'opzione -s (Symlink), deve stampare:")
    print(" - " + symlink_valido_1)
    print(" - " + symlink_valido_2)
    print("\nSe chiami il programma con l'opzione -l (Hardlink), deve stampare:")
    print(" - " + hardlink_valido_1)
    print(" - " + hardlink_valido_2)

if __name__ == "__main__":
    main()