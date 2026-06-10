import os
import shutil
import subprocess
import time

def main():
    test_env = "test_cprlt_env"
    src_dir = os.path.join(test_env, "src_dir")
    dst_dir = os.path.join(test_env, "dst_dir")

    # Pulizia preventiva
    if os.path.exists(test_env):
        shutil.rmtree(test_env)

    os.makedirs(src_dir)

    # Calcolo dei timestamp rispetto al tempo di esecuzione
    current_time = int(time.time())
    threshold_time = current_time - 1000 # Il tempo soglia che passeremo come parametro
    old_time = current_time - 2000       # Tempo nel passato (da linkare)
    new_time = current_time              # Tempo nel presente (da copiare)

    # 1. Creazione file VECCHIO
    old_file = os.path.join(src_dir, "file_vecchio.txt")
    with open(old_file, "w") as f:
        f.write("Questo file e' antecedente alla soglia.\n")
    os.utime(old_file, (old_time, old_time))

    # 2. Creazione file NUOVO
    new_file = os.path.join(src_dir, "file_nuovo.txt")
    with open(new_file, "w") as f:
        f.write("Questo file e' successivo alla soglia.\n")
    os.utime(new_file, (new_time, new_time))

    print(f"Ambiente creato. Soglia temporale (Epoch): {threshold_time}")
    print("Compilazione del file C...")
    
    compilation = subprocess.run(["gcc", "cprlt.c", "-o", "cprlt"], capture_output=True, text=True)
    if compilation.returncode != 0:
        print("Errore di compilazione:\n" + compilation.stderr)
        exit(1)

    print("Esecuzione del programma C...\n")
    # Lanciamo il programma passando il tempo come stringa
    subprocess.run(["./cprlt", src_dir, dst_dir, str(threshold_time)])

    print("--- RISULTATO ATTESO ---")
    print("file_vecchio.txt -> STESSO INODE in src e dst (Hard Link)")
    print("file_nuovo.txt   -> INODE DIVERSO (Copia Fisica tramite sendfile)")
    print("------------------------\n")
    
    subprocess.run(["ls", "-liR", test_env])

if __name__ == "__main__":
    main()