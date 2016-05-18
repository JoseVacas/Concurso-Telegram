# -*- coding: utf-8 -*-

import random
class Mensajes:
	def __init__(self):
		pass

	def getYaHasVotado(self,usuario):
		listaMensajes = self.__getListaMensajes('yaHasVotado=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getJuegoYaIniciado(self,usuario):
		listaMensajes = self.__getListaMensajes('hayJuegoYaIniciado=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getJuegoIniciado(self):
		listaMensajes = self.__getListaMensajes('juegoIniciado=')
		print listaMensajes
		return self.__getMensajeRandomFromLista(listaMensajes)

	def getGraciasPorVotar(self,usuario):
		listaMensajes = self.__getListaMensajes('graciasPorVotar=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getNoJuegoIniciado(self,usuario):
		listaMensajes = self.__getListaMensajes('noJuegoIniciado=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getNoHaVotadoNadie(self,usuario):
		listaMensajes = self.__getListaMensajes('noHaVotadoNadie=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getNoTieesPermisoSolucion(self,usuario):
		listaMensajes = self.__getListaMensajes('noTienesPermisoSolucion=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getNoTienesPermisoGenerico(self,usuario):
		listaMensajes = self.__getListaMensajes('noTienesPermisoGenerico=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)

	def getNoTienesPermisoIniciarEncuesta(self,usuario):
		listaMensajes = self.__getListaMensajes('noTienesPermisoInicioEncuesta=')
		return self.__getMensajeRandomFromLista(listaMensajes).replace('USUARIO',usuario)


	def __getMensajeRandomFromLista(self,lista):
		return random.choice(lista)

	def __getListaMensajes(self,cabecera):
		lista=[]
		archi = open('mensajes.txt', 'r')
		contenido = archi.readlines()
		for line in contenido:
			if line.find(cabecera)>=0:
				lista = line.replace(cabecera,'').replace('\n','').split(';')
		archi.close()
		return lista
