import os
import shutil

def main():
    test_dir = "test_catls_env"

    # Pulizia preventiva dell'ambiente di test
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # Creazione della directory principale del test
    os.makedirs(test_dir)

    # 1. Creazione di file di testo ASCII
    with open(os.path.join(test_dir, "testo1"), "w", encoding="ascii") as f:
        f.write("Questo e un semplice file di testo ASCII.\n")

    with open(os.path.join(test_dir, "favourites.txt"), "w", encoding="ascii") as f:
        f.write("Lista dei preferiti.\n")

    # 2. Creazione di sotto-directory
    os.makedirs(os.path.join(test_dir, "mydir"))
    os.makedirs(os.path.join(test_dir, "lib"))

    # 3. Creazione di un file in formato Unicode UTF-8 (con caratteri speciali)
    with open(os.path.join(test_dir, "unitesto"), "w", encoding="utf-8") as f:
        f.write("Testo con caratteri speciali UTF-8: à è ì ò ù €\n")

    print("Ambiente di test creato con successo: " + test_dir)
    print("\nComandi da lanciare per testare lo script:")
    print("1) python catls.py " + test_dir + "  (passando la directory)")
    print("2) cd " + test_dir + " && python ../catls.py  (senza parametri, usa la dir corrente)")
    
    print("\n--- RISULTATO ATTESO (l'ordine delle categorie può variare) ---")
    print("ASCII text:")
    print("testo1")
    print("favourites.txt")
    print("directory:")
    print("mydir")
    print("lib")
    print("Unicode text, UTF-8 text:")
    print("unitesto")

if __name__ == "__main__":
    main()