import os
import shutil

def main():
    dir1 = "test_dir1"
    dir2 = "test_dir2"

    if os.path.exists(dir1): shutil.rmtree(dir1)
    if os.path.exists(dir2): shutil.rmtree(dir2)

    os.makedirs(dir1)
    os.makedirs(dir2)

    # Caso 1: Stesso file in entrambe le directory (DA CANCELLARE)
    with open(os.path.join(dir1, "comune_A.txt"), "w") as f: f.write("Contenuto A")
    with open(os.path.join(dir2, "comune_B.txt"), "w") as f: f.write("Contenuto A")

    # Caso 2: Più copie in dir1 e una in dir2 (DA CANCELLARE TUTTI E TRE)
    with open(os.path.join(dir1, "multiplo_1.txt"), "w") as f: f.write("Contenuto C")
    with open(os.path.join(dir1, "multiplo_2.txt"), "w") as f: f.write("Contenuto C")
    with open(os.path.join(dir2, "multiplo_3.txt"), "w") as f: f.write("Contenuto C")

    # Caso 3: Copie multiple ma solo in dir1 (DA NON CANCELLARE)
    with open(os.path.join(dir1, "solo_dir1_a.txt"), "w") as f: f.write("Contenuto D")
    with open(os.path.join(dir1, "solo_dir1_b.txt"), "w") as f: f.write("Contenuto D")

    # Caso 4: File unici e isolati (DA NON CANCELLARE)
    with open(os.path.join(dir1, "unico_dir1.txt"), "w") as f: f.write("Contenuto E")
    with open(os.path.join(dir2, "unico_dir2.txt"), "w") as f: f.write("Contenuto F")

    # Caso 5: Sottocartelle con file uguali (DA IGNORARE, non devono essere cancellati)
    sub1 = os.path.join(dir1, "sub")
    sub2 = os.path.join(dir2, "sub")
    os.makedirs(sub1)
    os.makedirs(sub2)
    with open(os.path.join(sub1, "sub_comune.txt"), "w") as f: f.write("Contenuto G")
    with open(os.path.join(sub2, "sub_comune.txt"), "w") as f: f.write("Contenuto G")

    print("Ambiente di test creato.")
    print("Comando: python samesha.py test_dir1 test_dir2\n")
    
    print("RISULTATI ATTESI DOPO L'ESECUZIONE:")
    print("File RIMOSSI (hash in comune):")
    print("- comune_A.txt, comune_B.txt")
    print("- multiplo_1.txt, multiplo_2.txt, multiplo_3.txt")
    print("\nFile CONSERVATI:")
    print("- solo_dir1_a.txt, solo_dir1_b.txt (stesso hash, ma mancano in dir2)")
    print("- unico_dir1.txt, unico_dir2.txt (hash unici)")
    print("- i file nella sottocartella 'sub' (directory ignorate)")

if __name__ == "__main__":
    main()