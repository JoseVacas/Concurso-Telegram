
from Fachade import ConcursoFachade, UsuarioFachade
from Entity import *

def pruebaVotos():
	con = ConcursoFachade()
	concursos = con.getConcursosActivos()

	for c in concursos:
		v = Voto()
		us = Usuario()
		us.setIdUsuario(6924972)
		v.setVoto(c.getIdConcurso(),"respuesta",'2016-04-18 19:12:54',us)
		if not con.votarEnConcurso(c,v):
			print "ya ha votado"
		print con

def pruebaFactoryConcursos():
	factory = FactoryConcursos()
	factory.getConcursosActivos()
	factory.nuevoConcurso(-14968400)
	for i in factory.getListaConcursos():
		print factory.getListaConcursos()[i]

def concursosActivos():
	concursos = ConcursoFachade().getConcursosActivos()
	print concursos

def pruebaUsuario():
	usuario = Usuario()
	usuario.setNombre('ramon')
	usuario.setIdUsuario(6924972)
	us = UsuarioFachade()
	us.insertaUsuario(usuario)

pruebaUsuario()

#pruebaFactoryConcursos()
#concursosActivos()
