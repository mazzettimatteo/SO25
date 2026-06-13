import pathlib
p=pathlib.PurePath("/newfolder/text.txt")
print(p.parts)
print(p.parts[-1])
print(p.parent)
print(p.suffix)
p=pathlib.Path("./newfolder")
dire=0
files=0
for x in p.iterdir():
    if x.is_file():
         files+=1
    elif x.is_dir():
         dire+=1
print("num files: ",files,"\nnum directory: ",dire)
