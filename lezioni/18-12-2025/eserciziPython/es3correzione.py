import sys
import subprocess
import os

#guarda file segnato con * su foto iphone

root=sys.argv[1]

print(root)

ls=subprocess.run(['ls', '-lR', 'root'], capture_output=True, text=True)

print(ls.stdout)

currDir=""
for line in ls.stdout.splitlines():
    if not line:
        continue
    if line.startswith('total'):
        continue
    if line.endswith(':'):
        currDir=line[:-1]
        continue
    col=line.split()
    if col[0].startswith("l"):
        name=col[8]
        target=col[10]
        path =os.path.join(currDir, name)

        if os.path.isabs(target):
            
