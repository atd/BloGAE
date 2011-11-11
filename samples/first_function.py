#Funciones en python:

def mifuncion(cadena, numero, float):
	print cadena
	print str(numero)
	print str(float)

mifuncion('Hola',3,3.1416)

mifuncion(float=3.1416,cadena="lalala",numero="3")

#Funciones devolviendo algo
def quitaUltimoCaracter(cadena):
	return cadena[0:-1] #equivale a cadena[0:len(cadena)-1]

pythony = "pythony"
print quitaUltimoCaracter(pythony)
	
# Listas o diccionarios de longitud variable
# tambien pueden usarse a la hora de pasar params.	
otrafuncion(*args, **kwargs)

