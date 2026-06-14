import os
import shutil

def main():
    test_dir = "test_difdir_env"

    # Pulizia preventiva dell'ambiente
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(test_dir)
    dir_a = os.path.join(test_dir, "a")
    dir_b = os.path.join(test_dir, "b")
    
    os.makedirs(dir_a)
    os.makedirs(dir_b)

    # Popoliamo la directory 'a'
    files_a = ["alpha", "beta", "gamma", "delta"]
    for f in files_a:
        path = os.path.join(dir_a, f)
        with open(path, "w") as file:
            file.write(f"Questa e' la versione di {f} della directory A\n")

    # Popoliamo la directory 'b'
    files_b = ["beta", "delta", "epsilon", "zeta"]
    for f in files_b:
        path = os.path.join(dir_b, f)
        with open(path, "w") as file:
            file.write(f"Questa e' la versione di {f} della directory B\n")

    print(f"Ambiente di test creato con successo in: {test_dir}")
    print(f"Directory generate: {dir_a} e {dir_b}")
    print("I file in comune sono 'beta' e 'delta'.")

if __name__ == "__main__":
    main()