#------------WRITE---------
f=open("newfile","w")
f.write("ciao\n")
f.write("come va?\n")
f.write("lelelelel\n")
f.close()
#------------READ-----------
f=open("newfile","r")
for line in f.readlines():
    print(line)
f.close()