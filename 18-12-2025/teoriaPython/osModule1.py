import os
print(os.environ)

print(os.system("ls -la"))
print(os.getcwd()) #cwd curr working directory

os.rmdir("newdir")
os.mkdir("newdir")

print(os.system("ls -la"))
os.chdir("newdir")
print(os.getcwd()) 

currPID=os.getpid()
print(currPID)





os.abort()
print("ho fatto un abort, questo non si dovrebbe vedere")
