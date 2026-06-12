import os
import shutil
import subprocess

def main():
    test_dir = "test_symlist_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # Creazione delle directory
    os.makedirs(test_dir)
    subdir = os.path.join(test_dir, "subdir")
    os.makedirs(subdir)

    # 1. Creazione dei file reali (i target)
    file_a = os.path.join(test_dir, "file_A.txt")
    file_b = os.path.join(test_dir, "file_B.txt")
    
    with open(file_a, "w") as f:
        f.write("Target A\n")
    with open(file_b, "w") as f:
        f.write("Target B\n")

    # 2. Creazione dei link simbolici che puntano a file_A (Stesso Inode)
    os.symlink("file_A.txt", os.path.join(test_dir, "link_A1"))
    os.symlink("file_A.txt", os.path.join(test_dir, "link_A2"))
    os.symlink("../file_A.txt", os.path.join(subdir, "link_A3_ricorsivo"))

    # 3. Creazione dei link simbolici che puntano a file_B (Altro Inode)
    os.symlink("file_B.txt", os.path.join(test_dir, "link_B1"))

    print(f"Ambiente di test creato in: {test_dir}\n")
    print("--- INODE REALI DEI FILE TARGET ---")
    # Mostriamo gli inode reali per controllo visivo
    print(f"File A Inode: {os.stat(file_a).st_ino}")
    print(f"File B Inode: {os.stat(file_b).st_ino}\n")
    
    print("--- STRUTTURA GENERATA (ls -lR) ---")
    subprocess.run(["ls", "-lR", test_dir])

if __name__ == "__main__":
    main()