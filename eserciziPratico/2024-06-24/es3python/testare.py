import os
import stat
import shutil

def main():
    test_dir = "test_permdir_env"

    # Pulizia preventiva
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    os.makedirs(test_dir)

    # Funzione di appoggio per creare file e settare i permessi
    def create_file(name, mode):
        path = os.path.join(test_dir, name)
        with open(path, "w") as f:
            f.write(f"Contenuto del file {name}\n")
        os.chmod(path, mode)

    # File "due" -> -rw-r--r-- (644)
    create_file("due", stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # File "quattro" -> -rw-r----- (640)
    create_file("quattro", stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)

    # File "tre" -> -rwx------ (700)
    create_file("tre", stat.S_IRWXU)

    # File "uno" -> -rwx------ (700)
    create_file("uno", stat.S_IRWXU)

    # Directory esca (il programma deve ignorarla)
    os.makedirs(os.path.join(test_dir, "cartella_da_ignorare"))

    print("Ambiente di test creato con successo: " + test_dir)
    print("\nStruttura e permessi attuali:")
    os.system("ls -l " + test_dir)
    
    print("\nComando da lanciare:")
    print("python permdir.py " + test_dir)
    
    print("\n--- RISULTATO ATTESO ---")
    print("Devono essere create 3 cartelle nella directory corrente:")
    print("1. Cartella '-rw-r--r--' con dentro il link 'due'")
    print("2. Cartella '-rw-r-----' con dentro il link 'quattro'")
    print("3. Cartella '-rwx------' con dentro i link 'tre' e 'uno'")

if __name__ == "__main__":
    main()