#Clases en python

class Profesor:
	""" docs for estudiante
	"""
	def __init__(self,nombre,twitter):
		self.nombre = nombre
		self.twitter= twitter
	
	def printTwitter(self):
		print self.nombre+" @"+self.twitter
		

p1 = Profesor("Victor","VictorSanchez")
p1.printTwitter()
p2 = Profesor("Carlos","scyros")
p2.printTwitter()

