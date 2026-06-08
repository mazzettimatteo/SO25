import os
import stat
import shutil

def main():
    test_dir = "test_search_name_env"

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    os.makedirs(test_dir)
    os.makedirs(os.path.join(test_dir, "dir1"))
    os.makedirs(os.path.join(test_dir, "dir2"))
    os.makedirs(os.path.join(test_dir, "dir2", "dir3"))

    # 1. Caso: Script eseguibile nella directory radice
    script_path = os.path.join(test_dir, "testprog")
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\necho 'hello'")
    os.chmod(script_path, stat.S_IRWXU)

    # 2. Caso: Eseguibile ELF in dir1
    elf_path = os.path.join(test_dir, "dir1", "testprog")
    with open(elf_path, "wb") as f:
        f.write(b"\x7fELF_finto_codice_binario")
    os.chmod(elf_path, stat.S_IRWXU)

    # 3. Caso: Eseguibile ELF molto annidato in dir2/dir3
    elf2_path = os.path.join(test_dir, "dir2", "dir3", "testprog")
    with open(elf2_path, "wb") as f:
        f.write(b"\x7fELF_altro_codice_binario")
    os.chmod(elf2_path, stat.S_IRWXU)

    # 4. ESCA: File con il nome giusto, ma NON eseguibile (da ignorare)
    not_exec_path = os.path.join(test_dir, "dir2", "testprog")
    with open(not_exec_path, "w") as f:
        f.write("#!/bin/bash\necho 'non ho i permessi'")
    os.chmod(not_exec_path, stat.S_IRUSR | stat.S_IWUSR)

    # 5. ESCA: File eseguibile e script, ma con nome SBAGLIATO (da ignorare)
    wrong_name_path = os.path.join(test_dir, "dir1", "altro_script")
    with open(wrong_name_path, "w") as f:
        f.write("#!/bin/bash\necho 'nome sbagliato'")
    os.chmod(wrong_name_path, stat.S_IRWXU)

    print("Ambiente di test generato con successo: " + test_dir)
    print("\nComando da lanciare per testare:")
    print(" ./search_name testprog " + test_dir)
    
    print("\n--- RISULTATO ATTESO DOPO L'ESECUZIONE ---")
    print(f"{script_path}: script")
    print(f"{elf_path}: ELF executable")
    print(f"{elf2_path}: ELF executable")
    print("\nI file in 'dir2/testprog' (non eseguibile) e 'dir1/altro_script' (nome errato) non devono apparire nell'output.")

if __name__ == "__main__":
    main()