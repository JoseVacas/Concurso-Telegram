#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import telebot
from datetime import timedelta
from thread import start_new_thread
from datetime import datetime
from Fachade import ControladorFachade
TOKEN = ''



class TelegramCli:
	def __init__(self):
		self.comando= '/usr/local/bin/telegram-cli -k %s/.src/tg/tg-server.pub -W -R -D -e '%(str(os.environ['HOME']))

	def sendMsgToUser(self,usuarios,mensaje):
		for usuario in usuarios:
			try:
				cmd = "%s 'msg %s %s' > /dev/null" %(self.comando,usuario,mensaje)
				#os.system(cmd)
				print (cmd)
				subprocess.Popen([cmd])
			except:
				print ("Error en la notificacion de Telegram: "+mensaje)


"""
try:
	if sys.argv[1]=="-m":
		subprocess.Popen(["/home/pi/bots/telegram/trivial/telegramCli.sh", sys.argv[2],sys.argv[3]])
	elif sys.argv[1]=="-b":
		bot = telebot.TeleBot(TOKEN)
		bot.send_message(sys.argv[2], sys.argv[3])
		#start_new_thread(self.inicioDescarga,(url,nombre))
except:
	print "Error en los parametros"
"""


class Controlador:
	def __init__(self):
		pass

	def iniciarJuego(self,concurso):
		subprocess.Popen(["/home/pi/bots/telegram/trivial/telegramCli.sh", concurso.getNombreGrupo(),'/iniciarjuego'])

	def verFoto(self,concurso):
		subprocess.Popen(["/home/pi/bots/telegram/trivial/telegramCli.sh", concurso.getNombreGrupo(),'/verfoto'])

	def clasificacion(self,concurso):
		subprocess.Popen(["/home/pi/bots/telegram/trivial/telegramCli.sh", concurso.getNombreGrupo(),'/clasificacion'])

	def votaciones(self,concurso):
		subprocess.Popen(["/home/pi/bots/telegram/trivial/telegramCli.sh", concurso.getNombreGrupo(),'/votaciones'])

	def solucion(self,concurso):
		subprocess.Popen(["/home/pi/bots/telegram/trivial/telegramCli.sh", concurso.getNombreGrupo(),'/solucion'])

	def runPrueba(self,hour,minute,dayOfWeek):
		now =  datetime.now().timetuple()
		controladorFachade = ControladorFachade()
		listaConcursos = controladorFachade.getLitaConcursosControlador()
		ahora = datetime.now().timetuple()

		for concurso in listaConcursos:
			if concurso.getHora()==hour and concurso.getDayOfWeek()==dayOfWeek:
				if minute==0:
					#Inicio concurso
					print "Inicio Concurso"
					#self.iniciarJuego(concurso)
				if minute==15 or minute==30 or minute==45:
					#self.verFoto(concurso)
					print "Ver Foto"
				if minute==59:
					#self.solucion(concurso)
					print "Solucion Concurso"
				if minute== 10 or minute == 20 or minute == 40 or minute== 50:
					print "votaciones"
					#self.votaciones(concurso)
				if minute== 25:
					print "Clasificacion"
					#self.clasificacion(concurso)


			"""Prueba una hora mas, falta reparar el caso en el que al terminar concurso a las 12 ya seria un dias distinto

			if ((concurso.getFechaConcurso() + timedelta(hours=+1)).timetuple()[3] == hour) and concurso.getDayOfWeek()==dayOfWeek:
				if minute==0:
					self.solucion(concurso)
					print "Solucion Concurso: 0 min"
			"""

	def run(self):
		now =  datetime.now().timetuple()
		controladorFachade = ControladorFachade()
		listaConcursos = controladorFachade.getLitaConcursosControlador()
		ahora = datetime.now().timetuple()
		dayOfWeek = ahora[6]
		hour = ahora[3]
		minute = ahora[4]

		for concurso in listaConcursos:
			if concurso.getHora()==hour and concurso.getDayOfWeek()==dayOfWeek:
				if minute==0:
					#Inicio concurso
					print "Inicio Concurso"
					self.iniciarJuego(concurso)
					self.verFoto(concurso)
				if minute==15 or minute==30 or minute==45:
					self.verFoto(concurso)
					print "Ver Foto"
				if minute==59:
					self.solucion(concurso)
					print "Solucion Concurso"
				if minute== 10 or minute == 20 or minute == 40 or minute== 50:
					print "votaciones"
					self.votaciones(concurso)
				if minute== 25:
					print "Clasificacion"
					self.clasificacion(concurso)


			"""Prueba una hora mas, falta reparar el caso en el que al terminar concurso a las 12 ya seria un dias distinto

			if ((concurso.getFechaConcurso() + timedelta(hours=+1)).timetuple()[3] == hour) and concurso.getDayOfWeek()==dayOfWeek:
				if minute==0:
					self.solucion(concurso)
					print "Solucion Concurso: 0 min"
			"""


controlador = Controlador()
controlador.run()
#controlador.runPrueba(hour, minute, dayOfWeek)
"""
i=0
for i in range(0,60):
	print i
	controlador.runPrueba(22, i, 2)

print "aqui"
controlador.runPrueba(23, 0, 2)
"""
