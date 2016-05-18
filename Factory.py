import Fachade
import datetime

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
