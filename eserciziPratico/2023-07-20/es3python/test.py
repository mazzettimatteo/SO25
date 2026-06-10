import os
import shutil
import subprocess

def main():
    test_dir = "test_ascii_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # Creazione della directory principale
    os.makedirs(test_dir)

    # 1. Elementi puramente ASCII (NON devono essere segnalati dal tuo programma)
    dir_ascii = os.path.join(test_dir, "cartella_normale")
    os.makedirs(dir_ascii)
    open(os.path.join(test_dir, "file_standard.txt"), "w").close()
    open(os.path.join(dir_ascii, "documento.pdf"), "w").close()

    # 2. Elementi con caratteri non-ASCII (DEVONO essere segnalati)
    dir_non_ascii = os.path.join(test_dir, "cartella_espanol".replace("n", "ñ"))
    os.makedirs(dir_non_ascii)

    open(os.path.join(test_dir, "città.txt"), "w").close()
    open(os.path.join(dir_ascii, "file_uber.txt".replace("u", "ü")), "w").close()
    open(os.path.join(test_dir, "nome_con_c.png".replace("c", "ç")), "w").close()

    # Questo file in sé ha un nome ASCII, ma si trova in una directory non-ASCII.
    open(os.path.join(dir_non_ascii, "file_interno_ok.txt"), "w").close()

    print(f"Ambiente di test creato con successo in: {test_dir}\n")

    print("--- STRUTTURA GENERATA ---")
    subprocess.run(["ls", "-R", test_dir])

    print("\n--- RISULTATO ATTESO DAL TUO PROGRAMMA ---")
    print("Il tuo script lanciato sulla directory di test dovrebbe individuare i seguenti elementi:")
    print(f" - {os.path.join(test_dir, 'cartella_espanol'.replace('n', 'ñ'))}")
    print(f" - {os.path.join(test_dir, 'città.txt')}")
    print(f" - {os.path.join(dir_ascii, 'file_uber.txt'.replace('u', 'ü'))}")
    print(f" - {os.path.join(test_dir, 'nome_con_c.png'.replace('c', 'ç'))}")
    print("\nNota: se il tuo programma stampa i percorsi completi, verifica se vuoi includere anche 'file_interno_ok.txt' dato che il suo path include una cartella non-ASCII, oppure se vuoi testare solo il nome base ('basename') di ogni nodo dell'albero.")

if __name__ == "__main__":
    main()