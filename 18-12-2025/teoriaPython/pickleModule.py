
import pickle
#Pickle module: it allows to serialize and deserialize Python objects
#prendi un oggetto: lo salvi con pickle.dump(data, file, version) e viene creato un file binario
#per rileggere quel file, ossia ritrasformarlo in testo vero, uso pickle.load(file)

#???????????????????????????????????????????????


file = open('myfile', 'wb')
data = ["Test","Hello","Let's try"]
pickle.dump(data, file)
file.close()
file = open('myfile', 'rb')
data = pickle.load(file)
file.close()
for item in data:
print("Current item", item)