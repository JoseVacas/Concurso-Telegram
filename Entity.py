#!/usr/bin/env python

import Fachade
import datetime

class Usuario:
	def __init__(self):
		self.idUsuario=0
		self.nombre=""
		self.puntuacion=0

	def getIdUsuario(self):
		return self.idUsuario

	def getNombre(self):
		return self.nombre

	def getPuntuacion(self):
		return self.puntuacion

	def setIdUsuario(self,idUsuario):
		self.idUsuario = idUsuario

	def setNombre(self,nombre):
		self.nombre = nombre

	def setPuntuacion(self,puntuacion):
		self.puntuacion = puntuacion

class Grupo:
	def __init__(self):
		self.idGrupo=0
		self.nombre=""

	def setGrupo(self,idGrupo,nombre):
		self.idGrupo = idGrupo
		self.nombre = nombre

	def getIdGrupo(self):
		return self.idGrupo

	def getNombre(self):
		return self.nombre

	def setIdGrupo(self,idGrupo):
		self.idGrupo = idGrupo

	def setNombre(self,nombre):
		self.nombre = nombre

	def __str__(self):
		return str(self.nombre)+' '+str(self.idGrupo)


class Juego:
	def __init__(self):
		self.idJuego=0
		self.pregunta=""
		self.listaOpciones=""
		self.solucion=""
		self.imagen=""
		self.imagenSolucion=""


	def setJuego(self,idJuego,pregunta,opciones,solucion,imagen,imagenSolucion):
		self.idJuego=idJuego
		self.pregunta=pregunta
		self.listaOpciones=opciones.split(',')
		self.solucion=solucion
		self.imagen=imagen.split(',')
		self.imagenSolucion=imagenSolucion.split(',')

	def getIdJuego(self):
		return self.idJuego

	def getListaOpciones(self):
		return self.listaOpciones

	def getImagen(self):
		return self.imagen

	def getImagenSolucion(self):
		return self.imagenSolucion

	def getSolucion(self):
		return self.solucion

	def getPregunta(self):
		return self.pregunta


	def __str__(self):
		return 'ID:'+str(self.idJuego)+' ;Pregunta:'+self.pregunta+' ;ListaOpciones:'+str(self.listaOpciones)+' ;Solucion:'+str(self.solucion)+' ;Imagen:'+str(self.imagen)+' ;ImagenSolucion'+str(self.imagenSolucion)

class Concurso:
	def __init__(self,):
		self.idConcurso=0
		self.idGrupo=0
		self.inicioConcurso=None
		self.juego=None
		self.activo=1
		self.votos={}

	def setConcurso(self,idConcurso,idGrupo,inicioConcurso,juego,activo):
		self.idConcurso=idConcurso
		self.idGrupo=idGrupo
		self.inicioConcurso=inicioConcurso
		self.juego=juego
		self.activo=activo

	def getIdConcurso(self):
		return self.idConcurso

	def getIdGrupo(self):
		return self.idGrupo

	def getInicioConcurso(self):
		return self.inicioConcurso

	def getJuego(self):
		return self.juego

	def isActivo(self):
		return self.activo == 1

	def getVotaciones(self):
		return self.votos

	def setIdConcurso(self,idConcurso):
		self.idConcurso = idConcurso

	def setiDGrupo(self,idGrupo):
		self.idGrupo = idGrupo

	def setInicioConcurso(self,inicioConcurso):
		self.inicioConcurso = inicioConcurso

	def setJuego(self,juego):
		self.juego = juego

	def setActivo(self,activo):
		self.activo=activo

	def compruebaVoto(self,voto):
		return self.votos.has_key(voto.getUsuario().getIdUsuario())

	def addVoto(self,voto):
		if not self.compruebaVoto(voto):
			ids=voto.getUsuario().getIdUsuario()
			self.votos[ids]=voto
			return True
		else:
			return False

	def __str__(self):
		return str(self.idConcurso)+' '+str(self.idGrupo)+' '+str(self.juego)+' '+str(self.inicioConcurso)


class Voto:
	def __init__(self):
		self.idConcurso=0
		self.respuesta=""
		self.tiempoRespuesta=0
		self.usuario=None

	def setVoto(self,idConcurso,respuesta,tiempoRespuesta,usuario):
		self.idConcurso=idConcurso
		self.respuesta=respuesta
		self.tiempoRespuesta=tiempoRespuesta
		self.usuario=usuario

	def getIdConcurso(self):
		return self.idConcurso

	def getRespuesta(self):
		return self.respuesta

	def getTiempoRespuesta(self):
		return self.tiempoRespuesta

	def getUsuario(self):
		return self.usuario

	def setIdConcurso(self,concurso):
		self.idConcurso = idConcurso

	def setRespuesta(self,respuesta):
		self.respuesta = respuesta

	def setTiempoRespuesta(self,tiempoRespuesta):
		self.tiempoRespuesta = tiempoRespuesta

	def setUsuario(self,usuario):
		self.usuario = usuario

	def __str__(self):
		return str(self.usuario.getIdUsuario())+' Nombre:'+str(self.usuario.getNombre())+' Respuesta:'+self.respuesta


class ConcursoC:
	def __init__(self):
		self.horaConcurso=None
		self.idGrupo=None
		self.nombreGrupo=""

	def setConcursoC(self,idGrupo,nombreGrupo,horaConcurso):
		self.horaConcurso = horaConcurso
		self.idGrupo=idGrupo
		self.nombreGrupo=nombreGrupo


	def getFechaConcurso(self):
		return self.horaConcurso

	def getDayOfWeek(self):
		return self.horaConcurso.timetuple()[6]

	def getHora(self):
		return self.horaConcurso.timetuple()[3]
	def getMinuto(self):
		return self.horaConcurso.timetuple()[4]

	def getIdGrupo(self):
		return self.idGrupo

	def getNombreGrupo(self):
		return self.nombreGrupo


class FactoryConcursos:
	def __init__(self):
		self.listaConcursos={}

	def getConcursosActivos(self):
		concursos = Fachade.ConcursoFachade().getConcursosActivos()
		for con in concursos:
			self.listaConcursos[con.getIdGrupo()]= con

	def nuevoConcurso(self,idGrupo):
		if self.isConcursoActivo(idGrupo):
			return "juegoYaIniciado"
		else:
			concurso = Fachade.ConcursoFachade().nuevoConcurso(idGrupo)
			if not concurso:
				return "noJuego"
			else:
				self.listaConcursos[concurso.getIdGrupo()]=concurso
				return True

	def isConcursoActivo(self,idGrupo):
		return self.listaConcursos.has_key(idGrupo)

	def getListaConcursos(self):
		return self.listaConcursos

	def getConcursoByIdGrupo(self,idGrupo):
		return self.listaConcursos[idGrupo]

	def getVotaciones(self,idGrupo):
		votaciones = self.listaConcursos[idGrupo].getVotaciones()
		if len(votaciones)==0:
			return 0
		else:
			self.listaConcursos[idGrupo].getJuego().getPregunta()
			salida=self.listaConcursos[idGrupo].getJuego().getPregunta()+"\n\n"
			for i in votaciones:
				espacios=23 - len(votaciones[i].getUsuario().getNombre()) + len(votaciones[i].getRespuesta())
				salida= salida+votaciones[i].getUsuario().getNombre()+' '*espacios+votaciones[i].getRespuesta()+'\n'

			return salida

	def __calcularPuntos(self,listaGanadores,horaInicioConcurso):
		date = datetime.datetime.now()
		date.strftime('%Y-%m-%d %H:%M:%S')
		maximoSegundos = date - horaInicioConcurso

		for v in listaGanadores:
			delta =  maximoSegundos - (listaGanadores[v].getTiempoRespuesta() - horaInicioConcurso)
			puntosUsuario =  (delta.seconds * 120) / maximoSegundos.seconds
			if puntosUsuario < 30:
				puntosUsuario = 30
			listaGanadores[v].getUsuario().setPuntuacion(puntosUsuario)

		return listaGanadores


	def getGanadores(self,idGrupo):
		listaGanadores={}
		solucion = self.listaConcursos[idGrupo].getJuego().getSolucion()
		votos =self.listaConcursos[idGrupo].getVotaciones()
		for v in votos:
			if votos[v].getRespuesta() == solucion:
				listaGanadores[votos[v].getUsuario().getIdUsuario()] = votos[v]

		horaInicioConcurso = self.listaConcursos[idGrupo].getInicioConcurso()

		listaGanadores = self.__calcularPuntos(listaGanadores,horaInicioConcurso)
		return listaGanadores

	def eliminaConcurso(self,concurso):
		conFach=Fachade.ConcursoFachade()
		conFach.setConcursoJugado(concurso)
		del self.listaConcursos[concurso.getIdGrupo()]
