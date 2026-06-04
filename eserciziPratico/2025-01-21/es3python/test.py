import os
import shutil

def main():
    base_dir = "test_depth_env"
    abs_base_dir = os.path.abspath(base_dir)

    # Pulizia preventiva
    if os.path.exists(abs_base_dir):
        shutil.rmtree(abs_base_dir)

    # Definizione delle directory
    dir_lvl_1_a = os.path.join(abs_base_dir, "dir_1_a")
    dir_lvl_1_b = os.path.join(abs_base_dir, "dir_1_b")
    dir_lvl_2 = os.path.join(dir_lvl_1_a, "dir_2_profonda")

    os.makedirs(dir_lvl_1_a)
    os.makedirs(dir_lvl_1_b)
    os.makedirs(dir_lvl_2)

    # LIVELLO 0 (Radice del sottoalbero)
    # L'ordinamento alfabetico atteso e': a_file_0, z_file_0
    open(os.path.join(abs_base_dir, "z_file_0.txt"), "w").close()
    open(os.path.join(abs_base_dir, "a_file_0.txt"), "w").close()

    # LIVELLO 1 (Sottocartelle dirette)
    # L'ordinamento alfabetico atteso e': b_file_1, x_file_1, y_file_1
    open(os.path.join(dir_lvl_1_a, "x_file_1.txt"), "w").close()
    open(os.path.join(dir_lvl_1_a, "b_file_1.txt"), "w").close()
    open(os.path.join(dir_lvl_1_b, "y_file_1.txt"), "w").close()

    # LIVELLO 2 (Cartella piu' profonda)
    # L'ordinamento alfabetico atteso e': c_file_2, w_file_2
    open(os.path.join(dir_lvl_2, "w_file_2.txt"), "w").close()
    open(os.path.join(dir_lvl_2, "c_file_2.txt"), "w").close()

    print("Ambiente di test generato con successo: " + abs_base_dir)
    print("\nL'output del tuo programma deve essere rigorosamente in questo ordine:")
    print("\n--- PROFONDITA' 2 (Piu' profonda) ---")
    print(os.path.join(dir_lvl_2, "c_file_2.txt"))
    print(os.path.join(dir_lvl_2, "w_file_2.txt"))
    print("\n--- PROFONDITA' 1 ---")
    # Nota: Anche se sono in cartelle diverse (dir_1_a e dir_1_b), 
    # se la stampa richiede l'ordine alfabetico sul nome del file puro, 
    # oppure sul path intero a parita' di livello, questo dipendera' 
    # dalla tua implementazione di sort(). Assumiamo ordinamento sul path completo:
    print(os.path.join(dir_lvl_1_a, "b_file_1.txt"))
    print(os.path.join(dir_lvl_1_a, "x_file_1.txt"))
    print(os.path.join(dir_lvl_1_b, "y_file_1.txt"))
    print("\n--- PROFONDITA' 0 (Radice) ---")
    print(os.path.join(abs_base_dir, "a_file_0.txt"))
    print(os.path.join(abs_base_dir, "z_file_0.txt"))

if __name__ == "__main__":
    main()