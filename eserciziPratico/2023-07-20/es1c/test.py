import os
import shutil
import subprocess

def main():
    test_env = "test_cprl_env"
    src_dir = os.path.join(test_env, "src_dir")
    dst_dir = os.path.join(test_env, "dst_dir")

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_env):
        shutil.rmtree(test_env)

    # Creazione della struttura delle directory
    os.makedirs(src_dir)
    os.makedirs(dst_dir) # Creiamo la dir di destinazione principale
    
    sub_dir = os.path.join(src_dir, "sottocartella")
    os.makedirs(sub_dir)

    # Creazione dei file di test
    with open(os.path.join(src_dir, "file_radice.txt"), "w") as f:
        f.write("Testo radice\n")
        
    with open(os.path.join(sub_dir, "file_interno.txt"), "w") as f:
        f.write("Testo interno\n")

    print("Ambiente di test creato con successo in: " + test_env)
    print("Compilazione del file C...")
    
    # Compilazione tramite subprocess
    compilation = subprocess.run(["gcc", "cprl.c", "-o", "cprl"], capture_output=True, text=True)
    if compilation.returncode != 0:
        print("Errore di compilazione:\n" + compilation.stderr)
        exit(1)

    print("Esecuzione del programma C...\n")
    # Esecuzione del programma compilato
    subprocess.run(["./cprl", src_dir, dst_dir])

    print("--- RISULTATO ATTESO ---")
    print("Dovresti vedere la cartella src_dir e dst_dir con la stessa struttura.")
    print("I file corrispondenti DEVONO avere lo stesso numero iniziale (inode).")
    print("------------------------\n")
    
    # Esecuzione di ls -liR per mostrare gli inode e la struttura
    subprocess.run(["ls", "-liR", test_env])

if __name__ == "__main__":
    main()