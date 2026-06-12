import os
import subprocess
import time
import sys

def main():
    binary_name = "./pidcmd"
    source_name = "pidcmd.c"

    # 1. Compilazione del programma C
    print(f"Compilazione di {source_name}...")
    compilation = subprocess.run(["gcc", source_name, "-o", binary_name], capture_output=True, text=True)
    if compilation.returncode != 0:
        print("Errore di compilazione!")
        print(compilation.stderr)
        sys.exit(1)

    # Usiamo python3 per creare un comando sicuro che accetta stringhe arbitrarie in fondo
    test_cmd = ["python3", "-c", "import time; time.sleep(3600)", "stringa_test_univoca_2026"]

    print(f"Avvio del processo target in background: {' '.join(test_cmd)}")
    
    # 2. Lanciamo il processo in background
    bg_process = subprocess.Popen(test_cmd)
    expected_pid = bg_process.pid

    # Attendiamo un istante per permettere al kernel di creare il file in /proc
    time.sleep(0.5)

    try:
        print(f"Esecuzione di {binary_name}...")
        # 3. Eseguiamo il programma C passando gli stessi identici argomenti
        result = subprocess.run([binary_name] + test_cmd, capture_output=True, text=True)
        
        output = result.stdout.strip()
        detected_pids = output.split()

        print("\n--- RESOCONTO VERIFICA ---")
        print(f"PID reale generato da Python: {expected_pid}")
        print(f"PID rilevati dal tuo pidcmd:   {output if output else '[Nessun output]'}")
        print("--------------------------")

        if str(expected_pid) in detected_pids:
            print("ESITO TEST: SUCCESS (Il tuo programma funziona perfettamente!)")
        else:
            print("ESITO TEST: FAILURE (Il PID atteso non è stato rilevato)")

    finally:
        # 4. Pulizia del sistema
        bg_process.terminate()
        bg_process.wait()
        print("\nProcesso di background terminato e rimosso.")

if __name__ == "__main__":
    main()