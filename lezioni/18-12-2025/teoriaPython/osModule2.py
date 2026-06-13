import os
try:
    print("OS Module name: "+os.name)
    #Returns the list of active processes
    processList = os.system("ps aux") #dentro processList ci va il val di ritorno di os.system
    print(processList) #se va tutto a buon fine stampo 0
except OSError:
    print("error")