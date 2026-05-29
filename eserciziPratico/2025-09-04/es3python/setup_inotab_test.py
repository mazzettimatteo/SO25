import os
import shutil

def main():
    base_dir = "test_inotab"

    # Rimuove la directory di test se esiste già per garantire un ambiente pulito
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    # Livello 0 (Directory base)
    os.makedirs(base_dir)
    open(os.path.join(base_dir, "file_L0_a.txt"), 'w').close()
    open(os.path.join(base_dir, "file_L0_b.txt"), 'w').close()

    # Livello 1 (Sottodirectory della base)
    dir_l1_a = os.path.join(base_dir, "dir_L1_a")
    dir_l1_b = os.path.join(base_dir, "dir_L1_b")
    os.makedirs(dir_l1_a)
    os.makedirs(dir_l1_b)
    open(os.path.join(dir_l1_a, "file_L1_a.txt"), 'w').close()
    open(os.path.join(dir_l1_b, "file_L1_b.txt"), 'w').close()

    # Livello 2 (Sottodirectory del livello 1)
    dir_l2 = os.path.join(dir_l1_a, "dir_L2")
    os.makedirs(dir_l2)
    open(os.path.join(dir_l2, "file_L2.txt"), 'w').close()

    # Livello 3 (Per testare che inotab 2 si fermi prima di leggere questo livello)
    dir_l3 = os.path.join(dir_l2, "dir_L3")
    os.makedirs(dir_l3)
    open(os.path.join(dir_l3, "file_L3.txt"), 'w').close()

    print(f"Struttura generata con successo nella directory '{base_dir}'.\n")
    print("Elenco completo degli i-node ordinati in ordine crescente:")
    print("----------------------------------------------------------")

    # Raccoglie tutti i percorsi (file e directory) e i relativi i-node
    nodi = []
    
    # Aggiunge la directory radice di test
    nodi.append((os.stat(base_dir).st_ino, base_dir))

    for root, dirs, files in os.walk(base_dir):
        for nome in dirs + files:
            percorso_completo = os.path.join(root, nome)
            inode = os.stat(percorso_completo).st_ino
            nodi.append((inode, percorso_completo))

    # Ordina la lista basandosi sul primo elemento della tupla (l'i-node)
    nodi.sort(key=lambda x: x[0])

    # Stampa i risultati nel formato richiesto
    for inode, percorso in nodi:
        print(f"{inode} {percorso}")

if __name__ == "__main__":
    main()