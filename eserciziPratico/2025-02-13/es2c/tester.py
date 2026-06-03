import os
import shutil

def main():
    base_dir = "test_esteso_env"
    
    # Percorsi base
    abs_base_dir = os.path.abspath(base_dir)
    target_file = os.path.join(abs_base_dir, "file_target.txt")
    target_dir = os.path.join(abs_base_dir, "dir_d")
    sub_dir = os.path.join(target_dir, "sottocartella")
    
    if os.path.exists(abs_base_dir):
        shutil.rmtree(abs_base_dir)
    os.makedirs(sub_dir)

    # Contenuto di riferimento (es. 20 byte totali, consideriamo 10 byte come prefisso per i test -p)
    prefisso = b"0123456789"
    resto = b"ABCDEFGHIJ"
    contenuto_target = prefisso + resto

    # 1. Creazione FILE TARGET
    with open(target_file, "wb") as f:
        f.write(contenuto_target)

    # 2. File con CONTENUTO IDENTICO (Stessa dimensione, stessi byte)
    file_identico = os.path.join(target_dir, "file_identico.txt")
    with open(file_identico, "wb") as f:
        f.write(contenuto_target)

    # 3. File con STESSO PREFISSO (Primi 10 byte uguali, resto diverso, dimensione diversa o uguale)
    file_prefisso = os.path.join(sub_dir, "file_prefisso.txt")
    with open(file_prefisso, "wb") as f:
        f.write(prefisso + b"XXXXXXXXXX_EXTRA_BYTES")

    # 4. File ESCA (Tutto diverso)
    file_esca = os.path.join(target_dir, "file_esca.txt")
    with open(file_esca, "wb") as f:
        f.write(b"Z" * 30)

    # 5. SYMLINK e HARDLINK (Per verificare di non aver rotto le funzioni precedenti)
    os.symlink(target_file, os.path.join(target_dir, "symlink_valido"))
    os.link(target_file, os.path.join(sub_dir, "hardlink_valido"))

    print(f"Ambiente di test generato: {abs_base_dir}")
    print(f"Target: {target_file}")
    print(f"Directory: {target_dir}")
    print("\n--- Test Consigliati ---")
    print(f"./ckfile {target_file} {target_dir}          # Deve trovare 'file_identico.txt'")
    print(f"./ckfile -p 10 {target_file} {target_dir}    # Deve trovare 'file_identico.txt' e 'file_prefisso.txt'")

if __name__ == "__main__":
    main()