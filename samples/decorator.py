#Usando Decorators
#Especialmente utiles en entorno web!
def login_required(f):
	def check_auth(request,*args,**kwargs):
		session = Session()
		try:
			if session['nick']:
				return f(request,*args,**kwargs)
		except:
			request.redirect('/')
	return check_auth

@login_required
def func1():
    print "inside func1()"