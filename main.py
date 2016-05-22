#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot # Libreria de la API del bot.
from telebot import types # Tipos para la API del bot.
import urllib2
from Fachade import *
from Entity import *
import time
import datetime
from Mensajes import Mensajes


TOKEN = '' # Nuestro tokken del bot (el que @BotFather nos dio).

ADMINISTRADOR=6924972


bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
factory = FactoryConcursos()
factory.getConcursosActivos()
mensaje= Mensajes()
#mensajes = Mensajes()



knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard


commands = {  # command description used in the "help" command
			  'iniciojuego': 'Get used to the bot',
			  'votar': 'Gives you information about the available commands',
			  'sendLongText': 'A test using the \'send_chat_action\' command',
			  'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
}

def get_user_step(uid):
	if uid in userStep:
		return userStep[uid]
	else:
		knownUsers.append(uid)
		userStep[uid] = 0
		return 0

def getNombreUsuario(mensaje):
	usuario=mensaje.from_user.username
	if usuario==None:
		usuario = mensaje.from_user.first_name
	return str(usuario)

@bot.message_handler(commands=['iniciarjuego'])
def command_iniciojuego(m):
	#print m
	cid = m.chat.id

	if m.from_user.id==ADMINISTRADOR:
		if cid not in knownUsers:
			knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
			userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
		if factory.nuevoConcurso(cid)=="noJuego":
			msg ="No hay juegos Disponibles"
		elif factory.nuevoConcurso(cid)=="juegoYaIniciado":
			#msg = mensaje.getJuegoYaIniciado(getNombreUsuario(m))
			msg = "Juego Iniciado"
		else:
			msg = mensaje.getJuegoYaIniciado(getNombreUsuario(m))

		bot.send_message(cid,msg)

	else:
		msg =mensaje.getNoTienesPermisoIniciarEncuesta(getNombreUsuario(m))
		bot.send_message(cid,msg)

@bot.message_handler(commands=['verfoto'])
def command_ver_foto(m):
	cid = m.chat.id

	if factory.isConcursoActivo(cid):

		for imagen in factory.getConcursoByIdGrupo(cid).getJuego().getImagen():
			bot.send_message(cid, imagen)
			#time.sleep(0.5)
		bot.send_message(cid,factory.getConcursoByIdGrupo(cid).getJuego().getPregunta())
	else:
		msg = mensaje.getNoJuegoIniciado(getNombreUsuario(m))
		bot.send_message(cid,msg)

@bot.message_handler(commands=['votar'])
def command_votar(m):

	cid = m.chat.id
	if cid not in knownUsers:
		knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
		userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
	if factory.isConcursoActivo(cid):

		markup = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)

		for i in factory.getConcursoByIdGrupo(cid).getJuego().getListaOpciones():
			markup.add(str(i))
		bot.send_message(cid, "Elige una opcion:", reply_markup=markup)
		userStep[cid] = 2
	else:
		msg = mensaje.getNoJuegoIniciado(getNombreUsuario(m))
		bot.send_message(cid,msg)

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def msg_select_opcion(m):
	cid = m.chat.id
	text = m.text
	try:
		voto = Voto()
		usuario = Usuario()
		usuario.setIdUsuario(m.from_user.id)
		usuario.setNombre(getNombreUsuario(m))
		date = datetime.datetime.now()
		date.strftime('%Y-%m-%d %H:%M:%S')
		us = UsuarioFachade()
		us.insertaUsuario(usuario)
		voto.setVoto(cid, text,date, usuario)
		concurso = factory.getConcursoByIdGrupo(cid)
		con = ConcursoFachade()
		if con.votarEnConcurso(concurso,voto):
			msg = mensaje.getGraciasPorVotar(getNombreUsuario(m))
		else:
			msg = mensaje.getYaHasVotado(getNombreUsuario(m))
	except:
		bot.send_message("Error en la votacion",reply_markup=hideBoard)
		userStep[cid] = 0


	bot.send_message(cid, msg,reply_markup=hideBoard)
	userStep[cid] = 0

@bot.message_handler(commands=['votaciones'])
def command_ver_votaciones(m):
	cid = m.chat.id

	if factory.isConcursoActivo(cid):

		votaciones = factory.getVotaciones(cid)
		if votaciones==0:
			msg = mensaje.getNoHaVotadoNadie(getNombreUsuario(m))
		else:
			msg = votaciones

		bot.send_message(cid,msg)
	else:
		msg = mensaje.getNoJuegoIniciado(getNombreUsuario(m))
		bot.send_message(cid,msg)

@bot.message_handler(commands=['solucion'])
def command_ver_solucion(m):
	cid = m.chat.id
	if factory.isConcursoActivo(cid):
		if m.from_user.id==ADMINISTRADOR:
			for imagen in factory.getConcursoByIdGrupo(cid).getJuego().getImagenSolucion():
				bot.send_message(cid,imagen)
				time.sleep(0.5)
			ganadores = factory.getGanadores(cid)
			if len(ganadores)==0:
				msg="No hay ganadores\n"
				msg=msg+"La solucion correcta era: %s\n" %(factory.getConcursoByIdGrupo(cid).getJuego().getSolucion())
				print msg
			else:
				msg="La solucion correcta era: %s\n" %(factory.getConcursoByIdGrupo(cid).getJuego().getSolucion())
				msg=msg+"Los ganadores son:\n"
				for u in ganadores:
					espacios=23 - len(ganadores[u].getUsuario().getNombre()) + len(str(ganadores[u].getUsuario().getPuntuacion()))
					msg = msg + ganadores[u].getUsuario().getNombre()+' '*espacios+str(ganadores[u].getUsuario().getPuntuacion())+'\n'
			clasificacion = ClasificacionFachade()

			clasificacion.actualizaClasificacion(cid,ganadores)

			factory.eliminaConcurso(factory.getConcursoByIdGrupo(cid))
			#añadir concurso a tabla de ultimo concuros(aun no creada)
			#eliminar concurso del diccionaro factory de concursos
			bot.send_message(cid,msg)

		else:
			msg = mensaje.getNoTieesPermisoSolucion(getNombreUsuario(m))
			bot.send_message(cid,msg)



	else:
		msg = mensaje.getNoJuegoIniciado(getNombreUsuario(m))
		bot.send_message(cid,msg)


@bot.message_handler(commands=['clasificacion'])
def command_ver_clasificacion(m):
	cid = m.chat.id
	clasificacion = ClasificacionFachade()
	c = clasificacion.getClasificacion(cid)
	bot.send_message(cid,c)


@bot.message_handler(commands=['informacion'])
def command_ver_informacion(m):
	cid = m.chat.id
	info = "En este concurso podras mostrar tus habilidades para adivinar que hay debajo de lo oculto.\n\
	Si eres rapido y aciertas conseguiras el maximo de puntos.\nConforme avance el tiempo la recompensa por acertar sera menor"
	bot.send_message(cid,info,reply_markup=hideBoard)




def listener(messages): # Con esto, estamos definiendo una funcion llamada 'listener', que recibe como parametro un dato llamado 'messages'.
	for m in messages: # Por cada dato 'm' en el dato 'messages'
		cid = m.chat.id # Almacenaremos el ID de la conversacion.
		#bot.send_message(cid, 'msg',reply_markup=hideBoard)
		#print "[" + str(cid) + "]: " + m.text + m.chat.username # Y haremos que imprima algo parecido a esto -> [52033876]: /start

def main():
	while True:
		try:

			bot.set_update_listener(listener) # Así, le decimos al bot que utilice como funcion escuchadora nuestra funcion 'listener' declarada arriba.
			bot.polling(none_stop=True)
		except:
			pass
main()
