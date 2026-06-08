import os
import stat
import shutil

def main():
    test_dir = "test_run_name_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    # Creazione delle directory dell'albero
    dir1 = os.path.join(test_dir, "dir1")
    dir3 = os.path.join(test_dir, "dir2", "dir3")
    os.makedirs(dir1)
    os.makedirs(dir3)

    # Funzione per creare uno script eseguibile di test
    def create_executable_script(folder_path):
        file_path = os.path.join(folder_path, "testprog")
        with open(file_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"[testprog] Eseguito in directory: $(pwd)\"\n")
            f.write("echo \"[testprog] Argomenti ricevuti: $@\"\n")
        # Imposta i permessi di lettura ed esecuzione
        os.chmod(file_path, stat.S_IRWXU)

    # Crea i tre file testprog nelle rispettive cartelle
    create_executable_script(test_dir)
    create_executable_script(dir1)
    create_executable_script(dir3)

    print("Ambiente di test creato con successo: " + test_dir)
    print("\nComando da lanciare per testare (supponendo di aver specificato la cartella di partenza):")
    print(f" ./run_name testprog {test_dir} arg1 arg2 arg3")
    
    print("\n--- RISULTATO ATTESO ---")
    print(f"Il programma deve stampare 3 blocchi di output simili a questo:")
    print(f"[testprog] Eseguito in directory: <percorso_assoluto_della_sottocartella>")
    print(f"[testprog] Argomenti ricevuti: arg1 arg2 arg3")

if __name__ == "__main__":
    main()