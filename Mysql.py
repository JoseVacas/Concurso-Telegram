# -*- coding: utf-8 -*-

import MySQLdb


class BD:
	def __init__(self,servidor,usuario, contrasena,basedatos):
		try:
			self.db = MySQLdb.connect(host=servidor, user=usuario, passwd=contrasena, db=basedatos)
			self.cursor = self.db.cursor()
		except:
			print "Error Conexion SQL"

	def getDb(self):
		return self.db

	def getCursor(self):
		return self.cursor

	def closeDB(self):
		self.db.close()

	def getJuegos(self):
		consulta ="SELECT * FROM JUEGO"
		salida=[]

		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'idJuego':registro[0],'pregunta':registro[1],'opciones':registro[2],'solucion':registro[3],'imagen':registro[4],\
				'imagenSolucion':registro[5]}
				salida.append(dictio)

			return salida
		except:
			return "noEncontrado"

	def getJuegoByID(self,idJuego):
		consulta ="SELECT * FROM JUEGO WHERE IDjUEGO='%s'" %(idJuego)
		salida=[]

		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'idJuego':registro[0],'pregunta':registro[1],'opciones':registro[2],'solucion':registro[3],'imagen':registro[4],\
				'imagenSolucion':registro[5]}
				salida.append(dictio)

			return salida
		except:
			return "noEncontrado"

	def getConcurosActivos(self):
		consulta ="SELECT con.*,ju.* FROM CONCURSO con, JUEGO ju WHERE con.juego = ju.idJuego and con.activo"
		salida=[]

		#try:
		self.cursor.execute(consulta)
		resultado = self.cursor.fetchall()
		for registro in resultado:
			dictio={'idConcurso':registro[0],'inicioConcurso':registro[1],'activo':registro[4],'idJuego':registro[5],\
			'pregunta':registro[6],'opciones':registro[7],'solucion':registro[8],'imagen':registro[9],'imagenSolucion':registro[10],\
			'idGrupo':registro[2]}
			salida.append(dictio)

		return salida
		#except:
		#	return "noEncontrado"

	def getJuegoGrupo(self,idGrupo):
		consulta ="SELECT ju.* FROM `JUEGO` ju WHERE NOT exists (SELECT * FROM \
		`JUEGOS_JUGADOS` jujuga WHERE ju.idJuego = jujuga.idJuego and jujuga.idGrupo='%s') ORDER BY RAND()" %(idGrupo)

		salida=[]

		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'idJuego':registro[0],'pregunta':registro[1],'opciones':registro[2],'solucion':registro[3],\
				'imagen':registro[4],'imagenSolucion':registro[5]}
				salida.append(dictio)
			return salida
		except:
			return "noEncontrado"

	def getIdConcurso(self,idGrupo,idJuego):
		consulta ="SELECT `idConcurso` FROM CONCURSO WHERE `idGrupo` = %s and juego =%s and `activo`=1" %(idGrupo,idJuego)
		salida=[]
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				registro[0]
				salida.append(registro[0])

			return salida
		except:
			return "noEncontrado"


	def insertaConcurso(self,concurso):
		consulta = "INSERT INTO `CONCURSO`(`inicioConcurso`,`idGrupo`,`juego`,`activo`) VALUES ('%s',%s,%s,%s)"%(concurso.getInicioConcurso(),concurso.getIdGrupo(),concurso.getJuego().getIdJuego(),1)
		try:
			self.cursor.execute(consulta)
			self.db.commit()

		except:
			pass

	def updateConcursoActivo(self,idConcurso,activo):
		consulta = "UPDATE `CONCURSO` SET `activo`=%d WHERE idConcurso=%d" %(activo,idConcurso)
		try:
			self.cursor.execute(consulta)
			self.db.commit()
		except:
			print "Error Update"

	def insertaJuegoJugado(self,idGrupo,idJuego):
		consulta = "INSERT INTO `JUEGOS_JUGADOS`(`idGrupo`,`idJuego`) VALUES (%d,%d)"%(idGrupo,idJuego)
		try:
			self.cursor.execute(consulta)
			self.db.commit()

		except:
			pass

	def insertaUsuario(self,idUsuario,nombre):
		consulta = "INSERT INTO `USUARIO`(`idUsuario`,`nombre`) VALUES (%d,'%s')"%(idUsuario,nombre)
		try:
			self.cursor.execute(consulta)
			self.db.commit()

		except:
			pass

	def updateUsuario(self,idUsuario,nombre):
		consulta = "UPDATE `USUARIO` SET `nombre`='%s' WHERE idUsuario='%d'" %(nombre,idUsuario)
		try:
			self.cursor.execute(consulta)
			self.db.commit()
		except:
			print "Error Update"

	def getClasificacion(self,idGrupo):
		consulta ="SELECT ca.idGrupo,ca.puntuacion, u.nombre FROM `CLASIFICACION` ca, `USUARIO` u WHERE `idGrupo` = %s and ca.idUsuario = u.idUsuario ORDER BY ca.puntuacion DESC" %(idGrupo)
		salida=[]
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				t=(registro[2],registro[1])
				salida.append(t)

			return salida
		except:
			return "noEncontrado"

	def getUsuariosClasificacionByIdGrupo(self,idGrupo):
		consulta="SELECT * FROM `CLASIFICACION` WHERE `idGrupo` = %d" %(idGrupo)
		salida={}
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'idGrupo':registro[1],'idUsuario':registro[2],'puntuacion':registro[3]}
				salida[registro[2]]=dictio

			return salida
		except:
			return "noEncontrado"

	def actualizaClasificacionUsuario(self,idUsuario,idGrupo,puntuacion):
		consulta = "UPDATE `CLASIFICACION` SET `idGrupo`=%d,`idUsuario`=%d,`puntuacion`=%d WHERE `idUsuario`=%d and `idGrupo` = %d" %(idGrupo,idUsuario,puntuacion,idUsuario,idGrupo)
		try:
			self.cursor.execute(consulta)
			self.db.commit()
		except:
			print "Error Update"

	def insertaUsuarioClasificacion(self,idUsuario,idGrupo,puntuacion):
		consulta = "INSERT INTO `CLASIFICACION`(`idUsuario`,`idGrupo`,`puntuacion`) VALUES (%d,%d,%d)"%(idUsuario,idGrupo,puntuacion)
		try:
			self.cursor.execute(consulta)
			self.db.commit()
			return True

		except:
			return False

	def getVotosConcursos(self,idConcurso):
		consulta="SELECT DISTINCT v.*,u.* FROM `VOTO` v, USUARIO u WHERE  idConcurso=%s and v.idUsuario = u.idUsuario" %(idConcurso)
		salida=[]
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'idConcurso':registro[1],'respuesta':registro[2],'idUsuario':registro[3],'tiempoRespuesta':registro[4],'nombreUsuario':registro[6]}
				salida.append(dictio)
			return salida
		except:
			return "noEncontrado"

	def getUsuarioById(self,idUsuario):
		consulta ="SELECT `idUsuario`, `nombre` FROM USUARIO WHERE `idUsuario` = %d" %(idUsuario)
		dictio=[]
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'idUsuario':registro[0],'nombre':registro[1]}


			return dictio
		except:
			return "noEncontrado"

	def votarEnConcurso(self,idConcurso,respuesta,idUsuario,tiempoRespuesta):
		consulta = "INSERT INTO `VOTO`(`idConcurso`,`respuesta`,`idUsuario`,`tiempoRespuesta`) VALUES (%d,'%s','%s','%s')"%(idConcurso,respuesta,idUsuario,tiempoRespuesta)

		try:
			self.cursor.execute(consulta)
			self.db.commit()
			return True

		except:
			return False

	def getNumJornada(self,idGrupo):
		consulta="SELECT * FROM `CONCURSO` WHERE `activo` = 0 and `idGrupo` = %d" %(idGrupo)
		dictio=[]
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio.append(registro[0])
			return len(dictio)
		except:
			return "noEncontrado"


	def getConcursosControlador(self):
		consulta ="SELECT * FROM CONTROLADOR WHERE `activo` = 1"
		salida=[]
		try:
			self.cursor.execute(consulta)
			resultado = self.cursor.fetchall()
			for registro in resultado:
				dictio={'id':registro[0],'idGrupo':registro[1],'nombreGrupo':registro[2],'horaConcurso':registro[3]}
				salida.append(dictio)


			return salida
		except:
			return "noEncontrado"


	def update(self,consulta):
		try:
			self.cursor.execute(consulta)
			self.db.commit()
		except:
			print "Error Update"


#bd =BD('localhost', 'externo', 'cipotona', 'trivialBot')
#print bd.getConcursosControlador()
