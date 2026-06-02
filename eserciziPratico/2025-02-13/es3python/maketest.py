import os
import shutil

def main():
    base_dir = "test_size_env"
    target_file = "file_target_f.txt"
    target_dir = os.path.join(base_dir, "directory_d")
    
    # Pulizia preventiva dell'ambiente
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(target_dir)
    
    # Generiamo un file target di esattamente 50 byte
    content_50_bytes = "A" * 50
    with open(target_file, "w") as f:
        f.write(content_50_bytes)
        
    # 1. CASO VALIDO: Stessa dimensione (50 byte), ma file diverso
    file_valido_1 = os.path.join(target_dir, "file_valido_1.txt")
    with open(file_valido_1, "w") as f:
        f.write("B" * 50)
        
    # 2. CASO INVALIDO: Hardlink del file target (stessa dimensione ma stesso inode)
    hardlink_1 = os.path.join(target_dir, "hardlink_esca.txt")
    os.link(target_file, hardlink_1)
    
    # 3. CASO INVALIDO: File normale ma dimensione diversa (10 byte)
    file_diverso = os.path.join(target_dir, "file_piccolo.txt")
    with open(file_diverso, "w") as f:
        f.write("C" * 10)
        
    # Creazione di una sottocartella per testare l'attraversamento del sottoalbero
    sub_dir = os.path.join(target_dir, "sottocartella")
    os.makedirs(sub_dir)
    
    # 4. CASO VALIDO SOTTORETE: Stessa dimensione (50 byte), file diverso
    file_valido_2 = os.path.join(sub_dir, "file_valido_2.txt")
    with open(file_valido_2, "w") as f:
        f.write("D" * 50)
        
    # 5. CASO INVALIDO SOTTORETE: Hardlink del file target
    hardlink_2 = os.path.join(sub_dir, "hardlink_esca_sub.txt")
    os.link(target_file, hardlink_2)

    print("Ambiente di test generato con successo!")
    print("File target 'f': " + os.path.abspath(target_file))
    print("Directory 'd': " + os.path.abspath(target_dir))
    print("\nI file che il tuo script deve identificare e stampare sono:")
    print("- " + file_valido_1)
    print("- " + file_valido_2)

if __name__ == "__main__":
    main()