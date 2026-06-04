import os
import shutil

def main():
    base_dir = "test_samecont_env"
    abs_base_dir = os.path.abspath(base_dir)

    target_file = os.path.join(abs_base_dir, "file_target.txt")
    search_dir = os.path.join(abs_base_dir, "dir_d")
    sub_dir = os.path.join(search_dir, "subdir")

    # Pulizia preventiva
    if os.path.exists(abs_base_dir):
        shutil.rmtree(abs_base_dir)

    os.makedirs(sub_dir)

    # 1. Creazione file target (dimensione: 100 byte)
    with open(target_file, "wb") as f:
        f.write(b"A" * 100)

    # 2. CASO VALIDO 1: Stessa dimensione (100 byte), inode diverso
    file_valid_1 = os.path.join(search_dir, "file_valid_1.txt")
    with open(file_valid_1, "wb") as f:
        f.write(b"B" * 100)

    # 3. CASO INVALIDO 1: Dimensione diversa (50 byte)
    file_invalid_size = os.path.join(search_dir, "file_invalid_size.txt")
    with open(file_invalid_size, "wb") as f:
        f.write(b"C" * 50)

    # 4. CASO INVALIDO 2: Hardlink al target (stessa dimensione, ma stesso inode)
    hardlink_1 = os.path.join(search_dir, "hardlink_1")
    os.link(target_file, hardlink_1)

    # 5. CASO VALIDO 2 (nella sottocartella): Stessa dimensione, inode diverso
    file_valid_2 = os.path.join(sub_dir, "file_valid_2.txt")
    with open(file_valid_2, "wb") as f:
        f.write(b"D" * 100)

    # 6. CASO INVALIDO 3 (nella sottocartella): Hardlink al target
    hardlink_2 = os.path.join(sub_dir, "hardlink_2")
    os.link(target_file, hardlink_2)

    print("Ambiente di test generato con successo: " + abs_base_dir)
    print("Target f: " + target_file)
    print("Directory d: " + search_dir)
    print("Comando da lanciare per il test:")
    print("./samecont " + target_file + " " + search_dir)
    print("Output atteso (solo questi due file):")
    print(file_valid_1)
    print(file_valid_2)

if __name__ == "__main__":
    main()