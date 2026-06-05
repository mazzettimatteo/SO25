import os
import shutil

def main():
    # Definiamo i nomi delle cartelle
    base_test_dir = "test_slinout_env"          # Il sottoalbero da passare al programma
    outside_dir = "test_slinout_outside"        # La cartella ESTERNA al sottoalbero

    abs_base_test_dir = os.path.abspath(base_test_dir)
    abs_outside_dir = os.path.abspath(outside_dir)

    # Pulizia preventiva
    if os.path.exists(abs_base_test_dir): shutil.rmtree(abs_base_test_dir)
    if os.path.exists(abs_outside_dir): shutil.rmtree(abs_outside_dir)

    # Creazione delle directory
    os.makedirs(abs_base_test_dir)
    os.makedirs(os.path.join(abs_base_test_dir, "subdir"))
    os.makedirs(abs_outside_dir)

    # Creazione dei file target fisici
    internal_file = os.path.join(abs_base_test_dir, "internal_target.txt")
    with open(internal_file, "w") as f: f.write("Interno")

    external_file = os.path.join(abs_outside_dir, "external_target.txt")
    with open(external_file, "w") as f: f.write("Esterno")

    # --- Creazione dei Link Simbolici nella radice del sottoalbero ---
    
    # 1. INTERNO (Assoluto)
    os.symlink(internal_file, os.path.join(abs_base_test_dir, "sym_int_abs"))
    
    # 2. INTERNO (Relativo - punta al file nella stessa cartella)
    os.symlink("internal_target.txt", os.path.join(abs_base_test_dir, "sym_int_rel"))
    
    # 3. ESTERNO (Assoluto)
    os.symlink(external_file, os.path.join(abs_base_test_dir, "sym_ext_abs"))
    
    # 4. ESTERNO (Relativo - sale di un livello e scende nella cartella esterna)
    os.symlink(f"../{outside_dir}/external_target.txt", os.path.join(abs_base_test_dir, "sym_ext_rel"))

    # --- Creazione dei Link Simbolici nella sottocartella ---
    subdir = os.path.join(abs_base_test_dir, "subdir")
    
    # 5. INTERNO (Relativo - sale di un livello per puntare al file interno)
    os.symlink("../internal_target.txt", os.path.join(subdir, "sym_int_rel_sub"))
    
    # 6. ESTERNO (Relativo - sale di due livelli per puntare al file esterno)
    os.symlink(f"../../{outside_dir}/external_target.txt", os.path.join(subdir, "sym_ext_rel_sub"))

    print(f"Ambiente di test generato con successo!")
    print(f"Directory radice da analizzare: {abs_base_test_dir}")
    print("\n--- RISULTATO ATTESO DAL TUO PROGRAMMA ---")
    print("LINK INTERNI (puntano dentro il sottoalbero):")
    print(" - sym_int_abs")
    print(" - sym_int_rel")
    print(" - subdir/sym_int_rel_sub")
    print("\nLINK ESTERNI (puntano fuori dal sottoalbero):")
    print(" - sym_ext_abs")
    print(" - sym_ext_rel")
    print(" - subdir/sym_ext_rel_sub")

if __name__ == "__main__":
    main()