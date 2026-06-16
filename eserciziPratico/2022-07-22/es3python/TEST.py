import os
import shutil

def main():
    test_dir = "test_exec_env"

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(test_dir)

    # 1. Finto eseguibile ELF
    # Il tuo script deve ignorarlo grazie al controllo isElf()
    elf_path = os.path.join(test_dir, "fake_elf.bin")
    with open(elf_path, "wb") as f:
        f.write(b'\x7fELF' + b'\x00\x01\x02\x03')

    # 2. Script Bash valido con shebang
    # Il tuo script deve identificarlo ed eseguirlo stampando il messaggio a schermo
    script_path = os.path.join(test_dir, "test_script.sh")
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("echo \"---> SUCCESSO: test_script.sh e' stato eseguito!\"\n")

    # 3. File di testo generico
    # Il tuo script non deve eseguirlo perché non inizia con "#!"
    txt_path = os.path.join(test_dir, "documento.txt")
    with open(txt_path, "w") as f:
        f.write("Questo e' un semplice file di testo.\n")
        f.write("Non contiene shebang e non e' un eseguibile.\n")

    print(f"Ambiente di test creato con successo in: {test_dir}")
    print("Contenuto generato:")
    print(" - fake_elf.bin   (Da saltare: e' un ELF)")
    print(" - test_script.sh (Da eseguire: ha lo shebang)")
    print(" - documento.txt  (Da saltare: non ha lo shebang)")

if __name__ == "__main__":
    main()