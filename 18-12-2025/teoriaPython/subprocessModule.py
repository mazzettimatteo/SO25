import subprocess
#modo migliore per invocare comandi della shell è usando subprocess, usare os.system non ti permette di salvare, in maniera semplice, stdout ecc..
a=subprocess.run(["ls","-l"])
print(a)
print(a.returncode)
print(a.stdout)