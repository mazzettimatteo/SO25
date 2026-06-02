import os
import shutil

def main():
    base_dir = "test_drec_dir"
    abs_base_dir = os.path.abspath(base_dir)

    # Pulizia preventiva per avere un ambiente sempre fresco a ogni avvio
    if os.path.exists(abs_base_dir):
        shutil.rmtree(abs_base_dir)
    os.makedirs(abs_base_dir)

    # 1. IL BERSAGLIO: Un file normalissimo, ma il cui path assoluto 
    # verra' inserito all'interno di un altro file.
    file_bersaglio = os.path.join(abs_base_dir, "file_bersaglio.txt")
    with open(file_bersaglio, "w") as f:
        f.write("Sono un file normale. Nessuno cerca il mio contenuto.")

    # 2. FILE DIR RICORSIVO VALIDO: Contiene il path del file bersaglio
    file_valido = os.path.join(abs_base_dir, "file_valido.txt")
    with open(file_valido, "w") as f:
        f.write("Ecco un path a caso trovato in questa directory:\n")
        f.write(file_bersaglio + "\n")

    # 3. FILE DIR RICORSIVO AUTOREFERENZIALE: Contiene il proprio path.
    # Secondo la traccia, anche questo e' valido perche' e' comunque 
    # "il pathname di un file della directory corrente".
    file_auto = os.path.join(abs_base_dir, "file_autoreferenziale.txt")
    with open(file_auto, "w") as f:
        f.write(file_auto)

    # 4. ESCA INSIDIOSA: Contiene un path assoluto ben formattato, 
    # ma di un file che NON esiste fisicamente nella directory.
    file_esca_path = os.path.join(abs_base_dir, "esca_path_finto.txt")
    with open(file_esca_path, "w") as f:
        f.write(os.path.join(abs_base_dir, "fantasma.txt"))

    # 5. ESCA NORMALE: Testo generico.
    file_esca_normale = os.path.join(abs_base_dir, "esca_normale.txt")
    with open(file_esca_normale, "w") as f:
        f.write("Niente da vedere qui, circolare.")

    print("Ambiente di test generato con successo!")
    print("Percorso assoluto della directory: " + abs_base_dir)
    print("\nI file che il tuo programma in C deve stampare a video sono:")
    print("- file_valido.txt")
    print("- file_autoreferenziale.txt")

if __name__ == "__main__":
    main()