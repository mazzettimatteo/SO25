import os

def main():
    test_dir = "test_directory"
    
    # Crea la directory se non esiste
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        
    # Dizionario con nomi dei file e loro contenuto iniziale
    files_data = {
        "main.c": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello World\\n\");\n    return 0;\n}\n",
        "script.py": "def main():\n    print(\"Hello Python\")\n\nif __name__ == '__main__':\n    main()\n",
        "script_shebang.sh": "#!/bin/bash\n\necho \"Hello Bash\"\nls -l\n",
        "script_no_shebang.sh": "echo \"No shebang here\"\npwd\n",
        "ignore_me.txt": "Questo file non deve essere modificato dal tuo script.\n"
    }
    
    # Creazione fisica dei file
    for filename, content in files_data.items():
        filepath = os.path.join(test_dir, filename)
        with open(filepath, mode="w") as f:
            f.write(content)
            
    print("Cartella di test creata con successo: " + test_dir)

if __name__ == "__main__":
    main()