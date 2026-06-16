import os
import shutil

def main():
    test_dir = "test_elf_env"

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(test_dir)

    # Creazione di un falso file ELF (dimensione: 4 byte di header + 10 byte casuali = 14 byte)
    with open(os.path.join(test_dir, "fake_exec1.bin"), "wb") as f:
        f.write(b'\x7fELF' + b'\x00' * 10)

    # Creazione di un secondo falso file ELF (dimensione: 4 byte di header + 20 byte casuali = 24 byte)
    with open(os.path.join(test_dir, "fake_exec2.bin"), "wb") as f:
        f.write(b'\x7fELF' + b'\x01' * 20)

    # Creazione di un file NON ELF (la dimensione non deve essere calcolata dal tuo programma)
    with open(os.path.join(test_dir, "not_an_elf.txt"), "w") as f:
        f.write("Questo e' un semplice file di testo, non inizia con il magic number.")

    print(f"Ambiente di test creato in: {test_dir}")
    print("File ELF creati: fake_exec1.bin (14 byte) e fake_exec2.bin (24 byte).")
    print("Totale atteso dal programma elfsize: 38 byte.")

if __name__ == "__main__":
    main()