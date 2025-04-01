





r = open("reactionsInfo.txt", "r")
e = r.read()
f = open("reactionsInfo.txt", "w")
print(e)

e = e.strip('[')
e = e.replace("[", "")
print(e)



f.write(e)
f.close()
r.close()