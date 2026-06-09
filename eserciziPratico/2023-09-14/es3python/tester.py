import os
import shutil
import subprocess

def main():
    test_dir = "test_symlinks_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    # Creazione della directory principale e della sottocartella 'd'
    os.makedirs(test_dir)
    d_dir = os.path.join(test_dir, "d")
    os.makedirs(d_dir)

    # 1. Creazione dei file reali (vuoti)
    file1_path = os.path.join(test_dir, "file1")
    file2_path = os.path.join(test_dir, "file2")
    open(file1_path, 'a').close()
    open(file2_path, 'a').close()

    # 2. Creazione dei link simbolici nella directory principale (percorsi relativi)
    # os.symlink(target, nome_del_link)
    os.symlink("file1", os.path.join(test_dir, "sl1"))
    os.symlink("file1", os.path.join(test_dir, "sl1bis"))
    os.symlink("file2", os.path.join(test_dir, "sl2"))

    # 3. Creazione del link simbolico relativo nella sottocartella 'd'
    os.symlink("../file1", os.path.join(d_dir, "sld"))

    # 4. Creazione del link simbolico con percorso ASSOLUTO nella sottocartella 'd'
    abs_file1 = os.path.abspath(file1_path)
    os.symlink(abs_file1, os.path.join(d_dir, "gsld"))

    print(f"Ambiente di test creato con successo in: {test_dir}\n")
    print("--- STRUTTURA GENERATA (output di ls -lR) ---")
    
    # Esegue ls -lR per mostrare la struttura generata (usando subprocess come da tue linee guida)
    subprocess.run(["ls", "-lR", test_dir])

    print("\n--- RISULTATO ATTESO DAL TUO PROGRAMMA ---")
    print(f"Se lanci il tuo script passando come parametro '{test_dir}',")
    print("dovrebbe raggruppare i link in questo modo (il formato di stampa scegli tu quale usare):")
    print("\nGruppo 1 (puntano a file1):")
    print(" - test_symlinks_env/sl1")
    print(" - test_symlinks_env/sl1bis")
    print(" - test_symlinks_env/d/sld")
    print(" - test_symlinks_env/d/gsld")
    print("\nGruppo 2 (puntano a file2):")
    print(" - test_symlinks_env/sl2")

if __name__ == "__main__":
    main()