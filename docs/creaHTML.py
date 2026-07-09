import os

directory_appunti = "./eserciziPratico" 
file_output_index = "index.html"

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
        <h2>Soluzioni di Matteo Mazzetti - matteo.mazzetti13@studio.unibo.it</h2>
    </header>
    <div class="main-content">
        <p class="ai-disclaimer">I file di nome test.py, maketest.py, creaTest.py e simili sono file generati da un AI utilizzati per testare il codice. </p>
        <h1>{titolo_h1}</h1>
"""

# Script JavaScript originale per il syntax highlighting
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

html_fine = js_highlighter + """    </div>
</body>
</html>
"""

html_fine_index = """    </div>
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

# 2. Scrittura del file Indice (index.html)
with open(file_output_index, "w", encoding="utf-8") as f_index:
    f_index.write(get_html_inizio("Indice Esami", "Seleziona la data dell'esame"))
    f_index.write('        <ul class="exam-list">\n')
    
    for data in date_esame_ordinate:
        nome_file_html = f"esame_{data.replace(' ', '_')}.html"
        f_index.write(f'            <li><a href="{nome_file_html}" class="exam-link">Esame del: {data}</a></li>\n')
        
    f_index.write('        </ul>\n')
    f_index.write(html_fine_index)

# 3. Scrittura di un file HTML separato per ogni esame
for data in date_esame_ordinate:
    nome_file_html = f"esame_{data.replace(' ', '_')}.html"
    
    with open(nome_file_html, "w", encoding="utf-8") as f_out:
        f_out.write(get_html_inizio(f"Esame {data}", f"File dell'esame: {data}"))
        f_out.write(f'        <a href="{file_output_index}" class="back-link">Torna all\'indice degli esami</a>\n\n')
        
        file_ordinati = sorted(esami_dict[data], key=lambda x: x[0])
        
        # Creazione del menu interno per saltare ai vari file
        f_out.write('        <div class="toc">\n')
        f_out.write('            <h3>Indice degli esercizi</h3>\n')
        f_out.write('            <ul>\n')
        for file, percorso, lang_class in file_ordinati:
            safe_id = file.replace(".", "-").replace(" ", "-")
            f_out.write(f'                <li><a href="#{safe_id}">{file}</a></li>\n')
        f_out.write('            </ul>\n')
        f_out.write('        </div>\n\n')
        
        # Scrittura dei file
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