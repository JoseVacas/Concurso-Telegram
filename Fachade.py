# -*- coding: utf-8 -*-
from Mysql import BD
import Entity
import datetime


class JuegoFachade:
	def __init__(self):
		self.bd =BD('localhost', 'externo', 'cipotona', 'trivialBot')

	def getJuegoByID(self,idJuego):
		juego = Entity.Juego()
		jBD=self.bd.getJuegoByID(idJuego)
		juego.setJuego(jBD[0]['idJuego'],jBD[0]['pregunta'], jBD[0]['opciones'],jBD[0]['solucion'], jBD[0]['imagen'], jBD[0]['imagenSolucion'])
		self.bd.closeDB
		return juego

	def getJuegoGrupo(self,idGrupo):

		juego = Entity.Juego()
		jBD = self.bd.getJuegoGrupo(idGrupo)
		try:
			juego.setJuego(jBD[0]['idJuego'],jBD[0]['pregunta'], jBD[0]['opciones'],jBD[0]['solucion'], jBD[0]['imagen'], jBD[0]['imagenSolucion'])
			return juego
		except:
			return "noGame"


class ConcursoFachade:
	def __init__(self):
		self.bd =BD('localhost', 'externo', 'cipotona', 'trivialBot')

	def getConcursosActivos(self):
		listaConcursos=[]

		conDB=self.bd.getConcurosActivos()
		if not conDB=="noEncontrado":

			for con in conDB:
				juego = Entity.Juego()
				concurso = Entity.Concurso()
				juego.setJuego(con['idJuego'], con['pregunta'], con['opciones'], con['solucion'], con['imagen'], con['imagenSolucion'])
				concurso.setConcurso(con['idConcurso'], con['idGrupo'], con['inicioConcurso'], juego, con['activo'])
				listaConcursos.append(concurso)

			for con in listaConcursos:
				votos = self.getVotos(con.getIdConcurso())
				for i in votos:
					con.addVoto(i)

		return listaConcursos

	def nuevoConcurso(self,idGrupo):
		concurso = Entity.Concurso()

		concurso.setiDGrupo(idGrupo)

		juego = JuegoFachade().getJuegoGrupo(idGrupo)
		if juego=="noGame":
			return False
		else:
			concurso.setJuego(juego)

			date = datetime.datetime.now()

			concurso.setInicioConcurso(date)
			date.strftime('%Y-%m-%d %H:%M:%S')

			concurso.setActivo(1)
			self.bd.insertaConcurso(concurso)

			self.bd.getIdConcurso(idGrupo,juego.getIdJuego())
			concurso.setIdConcurso(self.bd.getIdConcurso(idGrupo,juego.getIdJuego())[0])
			self.bd.insertaJuegoJugado(idGrupo,juego.getIdJuego())


			return concurso

	def getVotos(self,idConcurso):
		listaVotos=[]
		votosBd = self.bd.getVotosConcursos(idConcurso)

		for v in votosBd:
			vot = Entity.Voto()
			us = Entity.Usuario()
			us.setIdUsuario(v['idUsuario'])
			us.setNombre(v['nombreUsuario'])
			vot.setVoto(v['idConcurso'], v['respuesta'], v['tiempoRespuesta'], us)
			listaVotos.append(vot)

		return listaVotos

	def votarEnConcurso(self,concurso,voto):
		if self.bd.votarEnConcurso(concurso.getIdConcurso(),voto.getRespuesta(),voto.getUsuario().getIdUsuario(),voto.getTiempoRespuesta()):
			concurso.addVoto(voto)
			return True
		else:
			return False

	def setConcursoJugado(self,concurso):
		idGrupo= concurso.getIdGrupo()
		idJuego = concurso.getJuego().getIdJuego()
		idConcurso = concurso.getIdConcurso()
		self.bd.insertaJuegoJugado(idGrupo, idJuego)
		self.bd.updateConcursoActivo(idConcurso,0)




class UsuarioFachade:
	def __init__(self):
		self.bd =BD('localhost', 'externo', 'cipotona', 'trivialBot')

	def getUsuarioById(self,idUsuario):
		usuario = Entity.Usuario()
		us = self.bd.getUsuarioById(idUsuario)
		print us
		if us=='noEncontrado' or len(us)==0:
			return "noEncontrado"
		else:
			usuario.setIdUsuario(us['idUsuario'])
			usuario.setNombre(us['nombre'])
			return usuario


	def insertaUsuario(self,usuario):
		usuarioDB = self.getUsuarioById(usuario.getIdUsuario())
		if usuarioDB=="noEncontrado":
			self.bd.insertaUsuario(usuario.getIdUsuario(), usuario.getNombre())
		else:
			if usuarioDB.getNombre() != usuario.getNombre():
				self.bd.updateUsuario(usuario.getIdUsuario(), usuario.getNombre())




class ClasificacionFachade:
	def __init__(self):
		self.bd =BD('localhost', 'externo', 'cipotona', 'trivialBot')
		self.lista=[]

	def getClasificacion(self,idGrupo):
		clasificacion = self.bd.getClasificacion(idGrupo)

		msg="Clasificacion Jornada nº "+str(self.getJornada(idGrupo))+'\n\n'
		if len(clasificacion)==0:
			msg="No hay clasificacion aun"
		else:
			cont = 1;
			for c in clasificacion:
				espacios = 19 - len(c[0])+len(str(c[1]))+len(str(cont))
				msg=msg+str(cont)+'º '+c[0]+' '*espacios+str(c[1])+' Pts'+'\n'
				cont = cont +1
		return msg

	def actualizaClasificacion(self,idGrupo,listaGanadores):
		listaUsuarios = self.bd.getUsuariosClasificacionByIdGrupo(idGrupo)
		for v in listaGanadores:
			if listaUsuarios.has_key(listaGanadores[v].getUsuario().getIdUsuario()):
				print "Actualizamos usuario",listaGanadores[v].getUsuario().getNombre()
				puntuacionNueva =  listaUsuarios[listaGanadores[v].getUsuario().getIdUsuario()]['puntuacion'] + listaGanadores[v].getUsuario().getPuntuacion()
				self.bd.actualizaClasificacionUsuario(listaGanadores[v].getUsuario().getIdUsuario(), idGrupo,puntuacionNueva)
			else:
				print "insertamos usuario",listaGanadores[v].getUsuario().getNombre()
				self.bd.insertaUsuarioClasificacion(listaGanadores[v].getUsuario().getIdUsuario(), idGrupo, listaGanadores[v].getUsuario().getPuntuacion())

	def getJornada(self,idGrupo):
		return self.bd.getNumJornada(idGrupo)


class ControladorFachade:
	def __init__(self):
		self.bd =BD('localhost', 'externo', 'cipotona', 'trivialBot')
		self.listaConcursoControlador=[]
		self.getConcursos()
	def getConcursos(self):

		lista = self.bd.getConcursosControlador()

		for con in lista:
			conControlador = Entity.ConcursoC()
			conControlador.setConcursoC(con['idGrupo'],con['nombreGrupo'],con['horaConcurso'])
			self.listaConcursoControlador.append(conControlador)

	def getLitaConcursosControlador(self):
		return self.listaConcursoControlador
