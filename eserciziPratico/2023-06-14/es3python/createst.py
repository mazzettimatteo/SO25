import os
import shutil
import subprocess

def main():
    test_dir = "test_rmsym_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # Creazione directory
    os.makedirs(test_dir)
    subdir = os.path.join(test_dir, "subdir")
    os.makedirs(subdir)

    # Creazione di un file reale di riferimento
    real_file = os.path.join(test_dir, "file_reale.txt")
    with open(real_file, "w") as f:
        f.write("Dati del file reale\n")

    # 1. Creazione link ASSOLUTO (Deve essere MANTENUTO)
    abs_target = os.path.abspath(real_file)
    os.symlink(abs_target, os.path.join(test_dir, "link_assoluto"))

    # 2. Creazione link RELATIVI (Devono essere CANCELLATI)
    # Link relativo nello stesso livello
    os.symlink("file_reale.txt", os.path.join(test_dir, "link_relativo_locale"))
    # Link relativo che sale di una cartella
    os.symlink("../file_reale.txt", os.path.join(subdir, "link_relativo_su"))

    print("Ambiente di test creato con successo in: " + test_dir + "\n")
    print("--- STRUTTURA INIZIALE (output di ls -lR) ---")
    subprocess.run(["ls", "-lR", test_dir])

    print("\n--- RISULTATO ATTESO DAL TUO PROGRAMMA ---")
    print("Il tuo script dovra' cancellare:")
    print(" - " + os.path.join(test_dir, "link_relativo_locale"))
    print(" - " + os.path.join(subdir, "link_relativo_su"))
    print("\nDovra' invece MANTENERE:")
    print(" - " + os.path.join(test_dir, "link_assoluto"))

if __name__ == "__main__":
    main()