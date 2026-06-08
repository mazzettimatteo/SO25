import os
import shutil

def main():
    test_dir = "test_tcmp_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    dir1 = os.path.join(test_dir, "dir1")
    dir2 = os.path.join(test_dir, "dir2")

    # --- Creazione struttura per dir1 ---
    os.makedirs(os.path.join(dir1, "cartella_comune"))
    os.makedirs(os.path.join(dir1, "cartella_solo_dir1"))
    
    # File in comune
    with open(os.path.join(dir1, "file_comune.txt"), "w") as f: f.write("comune")
    with open(os.path.join(dir1, "cartella_comune", "file_interno_comune.txt"), "w") as f: f.write("comune")
    
    # File solo in dir1
    with open(os.path.join(dir1, "file_solo_1.txt"), "w") as f: f.write("solo 1")
    with open(os.path.join(dir1, "cartella_comune", "file_interno_solo_1.txt"), "w") as f: f.write("solo 1")


    # --- Creazione struttura per dir2 ---
    os.makedirs(os.path.join(dir2, "cartella_comune"))
    os.makedirs(os.path.join(dir2, "cartella_solo_dir2"))
    
    # File in comune
    with open(os.path.join(dir2, "file_comune.txt"), "w") as f: f.write("comune")
    with open(os.path.join(dir2, "cartella_comune", "file_interno_comune.txt"), "w") as f: f.write("comune")
    
    # File solo in dir2
    with open(os.path.join(dir2, "file_solo_2.txt"), "w") as f: f.write("solo 2")
    with open(os.path.join(dir2, "cartella_comune", "file_interno_solo_2.txt"), "w") as f: f.write("solo 2")

    print(f"Ambiente di test creato con successo in: {test_dir}\n")
    
    print("--- COMANDI PER TESTARE E RISULTATI ATTESI ---")
    
    print("\n1. Comando senza parametri (Elementi in COMUNE):")
    print(f"   python tcmp.py {dir1} {dir2}")
    print("   RISULTATO ATTESO:")
    print("   cartella_comune")
    print("   file_comune.txt")
    print("   cartella_comune/file_interno_comune.txt")
    
    print("\n2. Comando con parametro -1 (Elementi SOLO IN DIR1):")
    print(f"   python tcmp.py -1 {dir1} {dir2}")
    print("   RISULTATO ATTESO:")
    print("   cartella_solo_dir1")
    print("   file_solo_1.txt")
    print("   cartella_comune/file_interno_solo_1.txt")
    
    print("\n3. Comando con parametro -2 (Elementi SOLO IN DIR2):")
    print(f"   python tcmp.py -2 {dir1} {dir2}")
    print("   RISULTATO ATTESO:")
    print("   cartella_solo_dir2")
    print("   file_solo_2.txt")
    print("   cartella_comune/file_interno_solo_2.txt")

if __name__ == "__main__":
    main()