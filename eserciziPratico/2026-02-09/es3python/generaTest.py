import os
import time

#CERCA LA PAROLA "SEGRETO"

def setup_test_environment():
    # Creazione delle directory principale e secondaria
    base_dir = 'test_dir'
    sub_dir = os.path.join(base_dir, 'sottocartella')
    os.makedirs(sub_dir, exist_ok=True)

    # File 1: Vecchio, contiene il pattern
    file1 = os.path.join(base_dir, 'file_vecchio.txt')
    with open(file1, 'w') as f:
        f.write("Questo file contiene la parola SEGRETO.\n")
    # Alteriamo il timestamp a 10 giorni fa
    old_time = time.time() - (10 * 86400)
    os.utime(file1, (old_time, old_time))

    # File 2: Età intermedia, contiene il pattern, si trova nella sottocartella
    file2 = os.path.join(sub_dir, 'file_intermedio.log')
    with open(file2, 'w') as f:
        f.write("Log file con SEGRETO all'interno.\n")
    # Alteriamo il timestamp a 5 giorni fa
    mid_time = time.time() - (5 * 86400)
    os.utime(file2, (mid_time, mid_time))

    # File 3: Molto recente, contiene il pattern
    file3 = os.path.join(base_dir, 'file_recente.txt')
    with open(file3, 'w') as f:
        f.write("Un altro testo con SEGRETO.\n")
    # Alteriamo il timestamp a 1 ora fa
    new_time = time.time() - 3600
    os.utime(file3, (new_time, new_time))

    # File 4: Non contiene il pattern
    file4 = os.path.join(sub_dir, 'file_vuoto.txt')
    with open(file4, 'w') as f:
        f.write("Questo file non contiene la parola cercata.\n")

    # File 5: File fittizio "binario" per testare la gestione delle eccezioni
    # Inseriamo il pattern ma lo circondiamo di byte non decodificabili in UTF-8
    file5 = os.path.join(base_dir, 'eseguibile_finto.bin')
    with open(file5, 'wb') as f:
        f.write(b'\xff\xfe\x00\x11SEGRETO\x99\x88')

    print("Ambiente di test creato con successo.")
    print(f"Esegui il tuo script passando la directory '{base_dir}' e cercando il pattern 'SEGRETO'.")
    print("\nOrdine atteso in output:")
    print(f"1. {file1}")
    print(f"2. {file2}")
    print(f"3. {file3}")
    print(f"(Nota: il file binario potrebbe o meno apparire a seconda di come hai gestito 'errors' nell'apertura)")

if __name__ == "__main__":
    setup_test_environment()