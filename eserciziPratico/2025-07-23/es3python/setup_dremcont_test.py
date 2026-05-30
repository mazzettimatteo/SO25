import os
import shutil

# Configurazione
TARGET_FILE = "file_riferimento.txt"
TEST_DIR = "test_dir_dremcont"
TARGET_CONTENT = "Questo e' il contenuto esatto da cercare e distruggere.\n"
DIFFERENT_CONTENT = "Questo contenuto e' innocuo e deve sopravvivere.\n"

def setup_test_env():
    # Pulizia ambiente precedente
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)

    # Creazione file target (f)
    with open(TARGET_FILE, "w") as f:
        f.write(TARGET_CONTENT)

    # Creazione struttura directory (d)
    os.makedirs(os.path.join(TEST_DIR, "subdir1"))
    os.makedirs(os.path.join(TEST_DIR, "subdir2", "subdir3"))

    # Creazione file da eliminare (stesso contenuto)
    files_to_delete = [
        os.path.join(TEST_DIR, "file_uguale_1.txt"),
        os.path.join(TEST_DIR, "subdir1", "file_uguale_2.txt"),
        os.path.join(TEST_DIR, "subdir2", "subdir3", "file_uguale_3.txt")
    ]
    for filepath in files_to_delete:
        with open(filepath, "w") as f:
            f.write(TARGET_CONTENT)

    # Creazione file da mantenere (contenuto diverso)
    files_to_keep = [
        os.path.join(TEST_DIR, "file_diverso_1.txt"),
        os.path.join(TEST_DIR, "subdir1", "file_diverso_2.txt"),
        os.path.join(TEST_DIR, "subdir2", "file_diverso_3.txt")
    ]
    for filepath in files_to_keep:
        with open(filepath, "w") as f:
            f.write(DIFFERENT_CONTENT)

    print("Ambiente di test generato con successo.\n")
    print("-" * 50)
    print("ISTRUZIONI PER IL TEST:")
    print(f"File parametro (f): {TARGET_FILE}")
    print(f"Directory parametro (d): {TEST_DIR}\n")
    print("Comando da eseguire:")
    print(f"python3 dremcont.py {TARGET_FILE} {TEST_DIR}")
    print("-" * 50)
    print("RISULTATO ATTESO DOPO L'ESECUZIONE:\n")
    print("I seguenti file devono ESSERE CANCELLATI:")
    for fp in files_to_delete:
        print(f" [X] {fp}")
    print("\nI seguenti file devono RIMANERE INTACTI:")
    for fp in files_to_keep:
        print(f" [V] {fp}")

if __name__ == "__main__":
    setup_test_env()