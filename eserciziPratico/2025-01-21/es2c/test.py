import os
import shutil

def main():
    base_dir = "test_findsyslink_env"
    abs_base_dir = os.path.abspath(base_dir)

    target_file = os.path.join(abs_base_dir, "file_target.txt")
    file_esca = os.path.join(abs_base_dir, "file_esca.txt")
    search_dir = os.path.join(abs_base_dir, "dir_d")
    sub_dir = os.path.join(search_dir, "sottocartella")

    # 1. Pulizia preventiva dell'ambiente
    if os.path.exists(abs_base_dir):
        shutil.rmtree(abs_base_dir)

    os.makedirs(sub_dir)

    # 2. Creazione del file target e di un file esca
    with open(target_file, "w") as f:
        f.write("Questo e' il file f.\n")
    
    with open(file_esca, "w") as f:
        f.write("Questo e' un altro file.\n")

    # 3. LIVELLO 1: Cartella principale
    # CASO VALIDO 1: Symlink corretto
    symlink_1 = os.path.join(search_dir, "symlink_valido_1")
    os.symlink(target_file, symlink_1)

    # CASO INVALIDO 1: Symlink che punta a un file diverso
    symlink_falso = os.path.join(search_dir, "symlink_falso")
    os.symlink(file_esca, symlink_falso)

    # CASO INVALIDO 2: Hardlink (stesso inode del target, ma NON e' un symlink)
    hardlink = os.path.join(search_dir, "hardlink_esca")
    os.link(target_file, hardlink)

    # 4. LIVELLO 2: Sottocartella
    # CASO VALIDO 2: Symlink corretto nella sottocartella
    symlink_2 = os.path.join(sub_dir, "symlink_valido_2")
    os.symlink(target_file, symlink_2)

    # CASO VALIDO 3: Un altro symlink corretto nella sottocartella
    symlink_3 = os.path.join(sub_dir, "symlink_valido_3")
    os.symlink(target_file, symlink_3)

    print("Ambiente di test generato con successo: " + abs_base_dir)
    print("Target f: " + target_file)
    print("Directory d: " + search_dir)
    print("\nComando da lanciare:")
    print("./findsyslink " + target_file + " " + search_dir)
    print("\n--- RISULTATO ATTESO ---")
    print("I percorsi stampati devono essere ESATTAMENTE 3:")
    print("- " + symlink_1)
    print("- " + symlink_2)
    print("- " + symlink_3)
    print("\nSe hai implementato correttamente il ritorno 'int', il main dovrebbe stampare che il TOTALE e' 3.")

if __name__ == "__main__":
    main()