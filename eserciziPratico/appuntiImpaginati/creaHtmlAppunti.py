import os

directory_appunti = "./.." 
file_output_html = "appunti_totali.html"

html_inizio = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Raccolta sorgenti per esame</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <a href="#c-section" class="nav-link">Sorgenti C</a>
        <a href="#python-section" class="nav-link">Script Python</a>
    </nav>
    <div class="main-content">
        <h1>Indice dei file sorgente</h1>
"""

# Script JavaScript per il syntax highlighting avanzato (Bug risolto: Token Isolation)
js_highlighter = r"""
<script>
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("pre code").forEach((block) => {
        let code = block.innerHTML;
        let lang = block.className;
        
        let tokens = {};
        let tokenIndex = 0;
        
        // Funzione per nascondere i token salvando l'HTML separatamente
        function saveToken(match, type) {
            let id = `__TOKEN_${tokenIndex++}__`;
            tokens[id] = `<span class="token ${type}">${match}</span>`;
            return id;
        }

        // 1. Commenti e Stringhe (Hanno la priorità massima)
        code = code.replace(/\/\*[\s\S]*?\*\//g, m => saveToken(m, 'comment'));
        code = code.replace(/\/\/.*$/gm, m => saveToken(m, 'comment'));
        code = code.replace(/#.*$/gm, m => saveToken(m, 'comment'));
        code = code.replace(/(["'])(?:(?!\1)[^\\]|\\.)*\1/g, m => saveToken(m, 'string'));
        
        // 2. Preprocessore (Solo per C)
        if (lang === 'language-c') {
            code = code.replace(/^[ \t]*#\s*(include|define|pragma|ifndef|endif|ifdef).*$/gm, m => {
                if (m.includes("__TOKEN_")) return m;
                return saveToken(m, 'preprocessor');
            });
        }

        // 3. Keyword di controllo flusso
        const controlKw = "\\b(if|else|while|for|return|switch|case|break|continue|default|in|try|except|with|as|pass|elif)\\b";
        code = code.replace(new RegExp(controlKw, "g"), m => saveToken(m, 'control'));

        // 4. Keyword di tipo base
        const typeKw = "\\b(int|void|char|float|double|struct|union|typedef|static|long|short|unsigned|def|class|import|from)\\b";
        code = code.replace(new RegExp(typeKw, "g"), m => saveToken(m, 'type'));

        // 5. Tipi custom e keyword speciali
        const customTypeKw = "\\b(dirent|stat|size_t|ssize_t|DIR|FILE|True|False|None)\\b";
        code = code.replace(new RegExp(customTypeKw, "g"), m => saveToken(m, 'customtype'));

        // 6. Costanti e Macro (Tutto in maiuscolo)
        code = code.replace(/\b([A-Z_][A-Z0-9_]*)\b/g, m => {
            if (m.startsWith("__TOKEN_")) return m;
            return saveToken(m, 'constant');
        });

        // 7. Funzioni (Parole seguite da parentesi tonda aperta)
        code = code.replace(/\b([a-zA-Z_]\w*)\s*(?=\()/g, (match, p1) => {
            if (p1.startsWith("__TOKEN_")) return match;
            return saveToken(p1, 'function') + match.substring(p1.length);
        });

        // 8. Proprietà di struct/oggetti (Parole precedute da -> o .)
        code = code.replace(/(-&gt;|\.)([a-zA-Z_]\w*)\b/g, (match, op, prop) => {
            if (prop.startsWith("__TOKEN_")) return match;
            return op + saveToken(prop, 'property');
        });

        // 9. Numeri
        code = code.replace(/\b(\d+)\b/g, m => saveToken(m, 'number'));

        // 10. Ripristino di tutti i token (Re-innesco dell'HTML in modo sicuro)
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

with open(file_output_html, "w", encoding="utf-8") as f_out:
    f_out.write(html_inizio)
    
    c_files = []
    py_files = []
    
    # Scansione dell'albero e suddivisione per formato
    for root, dirs, files in os.walk(directory_appunti):
        for file in files:
            if file == file_output_html or file == "creaHtmlAppunti.py" or file == "style.css":
                continue
            
            percorso_completo = os.path.join(root, file)
            if file.endswith(('.c', '.h')):
                c_files.append((file, percorso_completo))
            elif file.endswith('.py'):
                py_files.append((file, percorso_completo))
                
    # Ordinamento alfabetico facoltativo all'interno della stessa categoria
    c_files.sort(key=lambda x: x[0])
    py_files.sort(key=lambda x: x[0])
    
    # Scrittura della sezione C
    f_out.write('        <section id="c-section">\n')
    f_out.write('            <div class="section-title">Linguaggio C / Header</div>\n')
    for file, percorso in c_files:
        f_out.write(f"            <h2>File: {file}</h2>\n")
        f_out.write('            <pre><code class="language-c">\n')
        with open(percorso, "r", encoding="utf-8", errors="ignore") as f_in:
            contenuto = f_in.read()
            contenuto_protetto = contenuto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            f_out.write(contenuto_protetto)
        f_out.write("\n            </code></pre>\n")
    f_out.write('        </section>\n\n')
    
    # Scrittura della sezione Python
    f_out.write('        <section id="python-section">\n')
    f_out.write('            <div class="section-title">Linguaggio Python</div>\n')
    for file, percorso in py_files:
        f_out.write(f"            <h2>File: {file}</h2>\n")
        f_out.write('            <pre><code class="language-python">\n')
        with open(percorso, "r", encoding="utf-8", errors="ignore") as f_in:
            contenuto = f_in.read()
            contenuto_protetto = contenuto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            f_out.write(contenuto_protetto)
        f_out.write("\n            </code></pre>\n")
    f_out.write('        </section>\n')
                
    f_out.write(html_fine)
