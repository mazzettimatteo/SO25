import os
import re

directory_appunti = "../eserciziPratico" 
file_output_index = "index.html"

C_SYSCALLS = [
    "fork", "execve", "execvp", "execlp", "execv", "execl", "wait", "waitpid", 
    "pipe", "dup", "dup2", "open", "read", "write", "close", "stat", "lstat", 
    "fstat", "opendir", "readdir", "closedir", "kill", "signal", "sigaction", 
    "mkfifo", "link", "unlink", "symlink", "readlink", "chmod", "chown"
]

PY_METHODS = [
    "os.fork", "os.exec", "os.pipe", "os.dup", "os.dup2", "os.open", "os.read", 
    "os.write", "os.close", "os.stat", "os.lstat", "os.listdir", "os.walk", 
    "os.kill", "os.symlink", "os.link", "os.unlink", "os.remove", "os.mkdir", 
    "os.rmdir", "signal.signal", "subprocess.run", "subprocess.Popen", 
    "argparse.ArgumentParser", "sys.argv"
]

def get_html_inizio(titolo_pagina, titolo_h1):
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{titolo_pagina}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header-info">
        <h2>Sistemi Operativi - Soluzioni prove pratiche - Matteo Mazzetti matteo.mazzetti13@studio.unibo.it</h2>
    </header>
    <div class="main-content">
        <p class="ai-disclaimer">I file di nome test.py, maketest.py, creaTest.py e simili sono file generati da un AI utilizzati per testare il codice.</p>
        <h1>{titolo_h1}</h1>
"""

js_highlighter = r"""
<script>
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("pre code").forEach((block) => {
        let code = block.innerHTML;
        let lang = block.className;
        
        let tokens = {};
        let tokenIndex = 0;
        
        function saveToken(match, type) {
            let id = `__TOKEN_${tokenIndex++}__`;
            tokens[id] = `<span class="token ${type}">${match}</span>`;
            return id;
        }

        code = code.replace(/\/\*[\s\S]*?\*\//g, m => saveToken(m, 'comment'));
        code = code.replace(/\/\/.*$/gm, m => saveToken(m, 'comment'));
        code = code.replace(/#.*$/gm, m => saveToken(m, 'comment'));
        code = code.replace(/(["'])(?:(?!\1)[^\\]|\\.)*\1/g, m => saveToken(m, 'string'));
        
        if (lang === 'language-c') {
            code = code.replace(/^[ \t]*#\s*(include|define|pragma|ifndef|endif|ifdef).*$/gm, m => {
                if (m.includes("__TOKEN_")) return m;
                return saveToken(m, 'preprocessor');
            });
        }

        const controlKw = "\\b(if|else|while|for|return|switch|case|break|continue|default|in|try|except|with|as|pass|elif)\\b";
        code = code.replace(new RegExp(controlKw, "g"), m => saveToken(m, 'control'));

        const typeKw = "\\b(int|void|char|float|double|struct|union|typedef|static|long|short|unsigned|def|class|import|from)\\b";
        code = code.replace(new RegExp(typeKw, "g"), m => saveToken(m, 'type'));

        const customTypeKw = "\\b(dirent|stat|size_t|ssize_t|DIR|FILE|True|False|None)\\b";
        code = code.replace(new RegExp(customTypeKw, "g"), m => saveToken(m, 'customtype'));

        code = code.replace(/\b([A-Z_][A-Z0-9_]*)\b/g, m => {
            if (m.startsWith("__TOKEN_")) return m;
            return saveToken(m, 'constant');
        });

        code = code.replace(/\b([a-zA-Z_]\w*)\s*(?=\()/g, (match, p1) => {
            if (p1.startsWith("__TOKEN_")) return match;
            return saveToken(p1, 'function') + match.substring(p1.length);
        });

        code = code.replace(/(-&gt;|\.)([a-zA-Z_]\w*)\b/g, (match, op, prop) => {
            if (prop.startsWith("__TOKEN_")) return match;
            return op + saveToken(prop, 'property');
        });

        code = code.replace(/\b(\d+)\b/g, m => saveToken(m, 'number'));

        let hasTokens = true;
        let safety = 1000;
        while (hasTokens && safety > 0) {
            hasTokens = false;
            for (let id in tokens) {
                if (code.includes(id)) {
                    code = code.replace(id, tokens[id]);
                    hasTokens = true;
                }
            }
            safety--;
        }

        block.innerHTML = code;
    });
});
</script>
"""

js_filter = """
<script>
document.addEventListener("DOMContentLoaded", () => {
    const filterSelect = document.getElementById("tag-filter");
    if (filterSelect) {
        filterSelect.addEventListener("change", (e) => {
            const selectedTag = e.target.value;
            const items = document.querySelectorAll(".exam-list-item");
            
            items.forEach(item => {
                if (selectedTag === "all") {
                    item.classList.remove("hidden-item");
                } else {
                    const tagsAttr = item.getAttribute("data-tags");
                    if (tagsAttr) {
                        const tags = tagsAttr.split(",");
                        if (tags.includes(selectedTag)) {
                            item.classList.remove("hidden-item");
                        } else {
                            item.classList.add("hidden-item");
                        }
                    } else {
                        item.classList.add("hidden-item");
                    }
                }
            });
        });
    }
});
</script>
"""

html_fine = js_highlighter + """    </div>
</body>
</html>
"""

html_fine_index = js_filter + """    </div>
</body>
</html>
"""

esami_dict = {}

# 1. Scansione dell'albero e raggruppamento per data
for root, dirs, files in os.walk(directory_appunti):
    for file in files:
        if file in [file_output_index, "creaHtmlAppunti.py", "style.css"] or file.startswith("esame_"):
            continue
        
        if file.endswith(('.c', '.h', '.py')):
            percorso_completo = os.path.join(root, file)
            percorso_relativo = os.path.relpath(root, directory_appunti)
            parti_percorso = percorso_relativo.split(os.sep)
            
            if len(parti_percorso) > 0 and parti_percorso[0] not in ('.', '..'):
                data_esame = parti_percorso[0]
            else:
                data_esame = "File senza data"
            
            if data_esame not in esami_dict:
                esami_dict[data_esame] = []
                
            lang_class = "language-c" if file.endswith(('.c', '.h')) else "language-python"
            esami_dict[data_esame].append((file, percorso_completo, lang_class))

date_esame_ordinate = sorted(esami_dict.keys())

# 2. Pre-elaborazione: Estrazione dei tag per popolare il filtro
tags_per_esame = {}
tutti_tag_c = set()
tutti_tag_py = set()

for data in date_esame_ordinate:
    tags_c = set()
    tags_py = set()
    
    for file, percorso, lang_class in esami_dict[data]:
        with open(percorso, "r", encoding="utf-8", errors="ignore") as f_in:
            contenuto = f_in.read()
            if lang_class == "language-c":
                for sc in C_SYSCALLS:
                    if re.search(r'\b' + sc + r'\s*\(', contenuto):
                        tags_c.add(sc)
                        tutti_tag_c.add(sc)
            elif lang_class == "language-python":
                for pm in PY_METHODS:
                    base_pm = pm.replace('.', r'\.')
                    if re.search(r'\b' + base_pm, contenuto):
                        tags_py.add(pm)
                        tutti_tag_py.add(pm)
                        
    tags_per_esame[data] = {
        "c": sorted(list(tags_c)),
        "py": sorted(list(tags_py))
    }

# 3. Scrittura del file Indice (index.html)
with open(file_output_index, "w", encoding="utf-8") as f_index:
    f_index.write(get_html_inizio("Indice Esami", "Seleziona la data dell'esame"))
    
    # Sezione Filtro
    f_index.write('        <div class="filter-section">\n')
    f_index.write('            <label for="tag-filter" class="filter-label">Filtra per procedura:</label>\n')
    f_index.write('            <select id="tag-filter" class="filter-select">\n')
    f_index.write('                <option value="all">Mostra tutti gli esami</option>\n')
    if tutti_tag_c:
        f_index.write('                <optgroup label="C Syscalls">\n')
        for tag in sorted(tutti_tag_c):
            f_index.write(f'                    <option value="{tag}">{tag}</option>\n')
        f_index.write('                </optgroup>\n')
    if tutti_tag_py:
        f_index.write('                <optgroup label="Metodi Python">\n')
        for tag in sorted(tutti_tag_py):
            f_index.write(f'                    <option value="{tag}">{tag}</option>\n')
        f_index.write('                </optgroup>\n')
    f_index.write('            </select>\n')
    f_index.write('        </div>\n\n')

    f_index.write('        <ul class="exam-list">\n')
    
    for data in date_esame_ordinate:
        nome_file_html = f"esame_{data.replace(' ', '_')}.html"
        file_names = [f[0] for f in sorted(esami_dict[data], key=lambda x: x[0])]
        files_str = ", ".join(file_names)
        
        # Recupero i tag precedentemente salvati
        current_tags_c = tags_per_esame[data]["c"]
        current_tags_py = tags_per_esame[data]["py"]
        all_item_tags = current_tags_c + current_tags_py
        tags_str = ",".join(all_item_tags)
        
        f_index.write(f'            <li class="exam-list-item" data-tags="{tags_str}">\n')
        f_index.write(f'                <a href="{nome_file_html}" class="exam-link">Esame del: {data}</a>\n')
        f_index.write(f'                <div class="index-files">File: {files_str}</div>\n')
        
        if all_item_tags:
            f_index.write('                <div class="index-tags">\n')
            for t in current_tags_c:
                f_index.write(f'                    <span class="tag">{t}</span>\n')
            for t in current_tags_py:
                f_index.write(f'                    <span class="tag python-tag">{t}</span>\n')
            f_index.write('                </div>\n')
            
        f_index.write(f'            </li>\n')
        
    f_index.write('        </ul>\n')
    f_index.write(html_fine_index)

# 4. Scrittura di un file HTML separato per ogni esame
for data in date_esame_ordinate:
    nome_file_html = f"esame_{data.replace(' ', '_')}.html"
    
    with open(nome_file_html, "w", encoding="utf-8") as f_out:
        f_out.write(get_html_inizio(f"Esame {data}", f"File dell'esame: {data}"))
        f_out.write(f'        <a href="{file_output_index}" class="back-link">Torna all\'indice degli esami</a>\n\n')
        
        current_tags_c = tags_per_esame[data]["c"]
        current_tags_py = tags_per_esame[data]["py"]
        
        if current_tags_c or current_tags_py:
            f_out.write('        <div class="tags-container">\n')
            f_out.write('            <h3>Syscall e Metodi utilizzati in questo esame:</h3>\n')
            for t in current_tags_c:
                f_out.write(f'            <span class="tag">{t}</span>\n')
            for t in current_tags_py:
                f_out.write(f'            <span class="tag python-tag">{t}</span>\n')
            f_out.write('        </div>\n\n')
        
        file_ordinati = sorted(esami_dict[data], key=lambda x: x[0])
        
        f_out.write('        <div class="toc">\n')
        f_out.write('            <h3>Indice degli esercizi</h3>\n')
        f_out.write('            <ul>\n')
        for file, percorso, lang_class in file_ordinati:
            safe_id = file.replace(".", "-").replace(" ", "-")
            f_out.write(f'                <li><a href="#{safe_id}">{file}</a></li>\n')
        f_out.write('            </ul>\n')
        f_out.write('        </div>\n\n')
        
        for file, percorso, lang_class in file_ordinati:
            safe_id = file.replace(".", "-").replace(" ", "-")
            f_out.write(f'        <section class="file-section" id="{safe_id}">\n')
            f_out.write(f"            <h2>File: {file}</h2>\n")
            f_out.write(f'            <pre><code class="{lang_class}">\n')
            
            with open(percorso, "r", encoding="utf-8", errors="ignore") as f_in:
                contenuto = f_in.read()
                contenuto_protetto = contenuto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                f_out.write(contenuto_protetto)
                
            f_out.write("\n            </code></pre>\n")
            f_out.write('        </section>\n\n')
            
        f_out.write(html_fine)