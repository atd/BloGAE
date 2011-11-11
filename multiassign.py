#Multiasignacion en python

nombre1, apellido1 = "VICTOR","SANCHEZ"

print nombre1
print apellido1

#Incluso en funciones
def splitName(name):
	name = name.split(" ")
	return name[0],name[1]

nombre2,apellido2 = splitName("CARLOS LEON")

print nombre2
print apellido2	