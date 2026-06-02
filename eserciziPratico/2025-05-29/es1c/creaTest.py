import os

def main():
    base_dir = "test_prec_dir"
    
    # Otteniamo il percorso assoluto della cartella di test
    abs_base_dir = os.path.abspath(base_dir)

    # Creazione directory principale
    if not os.path.exists(abs_base_dir):
        os.makedirs(abs_base_dir)

    # 1. File path ricorsivo VALIDO (nella cartella base)
    file1 = os.path.join(abs_base_dir, "file_ricorsivo_1.txt")
    with open(file1, "w") as f:
        f.write(file1)

    # 2. File ESCA normale
    file2 = os.path.join(abs_base_dir, "file_esca.txt")
    with open(file2, "w") as f:
        f.write("Il contenuto di questo file non c'entra nulla con il suo nome.")

    # Creazione di una sottocartella per verificare la scansione (ricorsiva o iterativa)
    sub_dir = os.path.join(abs_base_dir, "sub_dir")
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

    # 3. File path ricorsivo VALIDO (nella sottocartella)
    file3 = os.path.join(sub_dir, "file_ricorsivo_2.txt")
    with open(file3, "w") as f:
        f.write(file3)

    # 4. File ESCA insidioso (pathname corretto ma con un \n di troppo alla fine)
    file4 = os.path.join(sub_dir, "file_esca_insidioso.txt")
    with open(file4, "w") as f:
        f.write(file4 + "\n")

    # 5. File vuoto per testare crash da lettura
    file5 = os.path.join(sub_dir, "file_vuoto.txt")
    with open(file5, "w") as f:
        pass

    print("Ambiente di test generato con successo!")
    print("Percorso assoluto della directory di test: " + abs_base_dir)
    print("\nI file che il tuo programma in C deve identificare sono:")
    print("- " + file1)
    print("- " + file3)

if __name__ == "__main__":
    main()