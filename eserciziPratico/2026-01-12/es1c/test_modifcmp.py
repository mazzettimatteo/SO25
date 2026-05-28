import os
import time
import subprocess
import shutil

# Configurazione
WORKSPACE = "test_workspace"
C_SOURCE = "modifcmp.c"
EXEC_NAME = "modifcmp"
EXEC_PATH = os.path.join(".", EXEC_NAME)

def setup_env():
    """Crea una directory isolata con file vecchi e nuovi rispetto a un file di riferimento."""
    if os.path.exists(WORKSPACE):
        shutil.rmtree(WORKSPACE)
    os.makedirs(os.path.join(WORKSPACE, "subdir"))

    now = time.time()
    old_time = now - 86400  # -1 giorno
    new_time = now + 86400  # +1 giorno

    # Mappa dei file da creare e relativo timestamp
    files = {
        "ref.txt": now,
        "old.txt": old_time,
        "new.txt": new_time,
        os.path.join("subdir", "old_sub.txt"): old_time,
        os.path.join("subdir", "new_sub.txt"): new_time
    }

    for fname, mtime in files.items():
        path = os.path.join(WORKSPACE, fname)
        with open(path, "w") as f:
            f.write("dati di test")
        os.utime(path, (mtime, mtime))

def check_output(output_lines, expected_substrings):
    """Verifica che l'output contenga esattamente le stringhe attese."""
    if not output_lines and not expected_substrings:
        return True
    
    match_count = 0
    for expected in expected_substrings:
        if any(expected in line for line in output_lines):
            match_count += 1
            
    return match_count == len(expected_substrings) and len(output_lines) == len(expected_substrings)

def run_test(name, cmd, expected_substrings, cwd=None):
    print(f"--- {name} ---")
    print(f"Comando: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    
    if result.returncode != 0:
        print(f"Errore di esecuzione (Exit {result.returncode}):\n{result.stderr}")
        return
        
    output_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
    
    if check_output(output_lines, expected_substrings):
        print("Risultato: PASSATO\n")
    else:
        print("Risultato: FALLITO")
        print(f"Atteso (substringhe): {expected_substrings}")
        print(f"Ottenuto: {output_lines}\n")

def main():
    if not os.path.exists(C_SOURCE):
        print(f"Errore: Il file sorgente '{C_SOURCE}' non si trova nella directory corrente.")
        return

    print("1. Compilazione del file C...")
    compile_result = subprocess.run(["gcc", C_SOURCE, "-o", EXEC_NAME], capture_output=True, text=True)
    if compile_result.returncode != 0:
        print(f"Errore di compilazione:\n{compile_result.stderr}")
        return

    print("2. Creazione dell'ambiente di test temporale...")
    setup_env()

    print("3. Esecuzione dei test...\n")

    # CASO 1: Un solo argomento
    # Spostiamo il processo nel workspace affinché la directory corrente "." coincida con i file di test
    run_test(
        "Caso 1 (1 argomento - Cerca nel sottoalbero corrente)",
        [f"../{EXEC_NAME}", "ref.txt"],
        ["new.txt", "new_sub.txt"], 
        cwd=WORKSPACE
    )

    # CASO 2: Due argomenti (File e File)
    run_test(
        "Caso 2A (2 argomenti - Il secondo file è più recente)",
        [EXEC_PATH, os.path.join(WORKSPACE, "ref.txt"), os.path.join(WORKSPACE, "new.txt")],
        ["new.txt"]
    )
    
    run_test(
        "Caso 2B (2 argomenti - Il secondo file è più vecchio, nessun output atteso)",
        [EXEC_PATH, os.path.join(WORKSPACE, "ref.txt"), os.path.join(WORKSPACE, "old.txt")],
        []
    )

    # CASO 3: Due argomenti (File e Directory)
    run_test(
        "Caso 3 (2 argomenti - Cerca nel sottoalbero della directory target)",
        [EXEC_PATH, os.path.join(WORKSPACE, "ref.txt"), os.path.join(WORKSPACE, "subdir")],
        ["new_sub.txt"]
    )

if __name__ == "__main__":
    main()