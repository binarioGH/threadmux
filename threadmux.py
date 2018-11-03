#-*-coding: utf-8-*-
from socket import *
from os import popen, getcwd, chdir, system
from platform import python_version as pv
from platform import system as s
from threading import *
'''
La idea principal es que hayan varios servidores ejecutandose en 127.0.0.1
a cuales les puedas mandar comandos.
'''



class Console():
	def __init__(self):
		if str(s()).lower() == "windows":
			#Esto es para que se pueda usar en varios sistemas operativos.
			self.clear = "cls"
		else:
			self.clear = "clear"
		self.consoles = {}
		'''en esta lista se va a guardar una tupla con un int (que va a 
		ser el numero de puerto), una lista (que va a tener la lista de 
		directorios en donde se ejecutó cada comando) y una ultima lista
		con el output de cada comando, así cuando se cambie de consola el progreso
		seguirá ahí.'''
	def createconsole(self):
		port = int(raw_input("Ingresa el puerto: "))
		consolesock = socket()
		consolesock.bind(("127.0.0.1", port))
		thisconsole = "Console {}".format(len(self.consoles))
		'''La idea es crear un socket y que se cree en 127.0.0.1
		al cual te conectes y se ejecuten los comandos.'''
		self.consoles[thisconsole] = [port, True,[getcwd()],[],[]]
		while self.consoles[thisconsole][1]:

			consolesock.listen(1)
			conn = consolesock.accept()
			conn[0].send(thisconsole.encode())
			#ad significa actual dir
			ad = self.consoles[thisconsole][2]
			#lo significa last output
			lo = self.consoles[thisconsole][3]
			while True:

				if self.consoles[thisconsole][1] == False:
					break
				try:
					cmd = conn[0].recv(1024).decode()
					self.consoles[thisconsole][4].append(cmd)
					if cmd[:2] == "cd":
						chdir(cmd[3:])
						out = " "
					elif cmd == self.clear:
						system(self.clear)
					elif cmd.lower() == "exit":
						del self.consoles[thisconsole]
						return 0
					else:
						out = popen(cmd).read()
					ad.append(getcwd())
					lo.append(out)
					conn[0].send("{}\n{}".format(ad[len(ad) - 1],lo[len(lo) - 1]).encode())
				except Exception as e:
					print(e)
			del self.consoles[thisconsole]
			return 0





if __name__ == '__main__':
	if str(pv())[0] == "3":
		raw_input = input

	main = Console()
	usersock = socket()
	ucmd = " "
	while ucmd != "exit":
		ucmd = raw_input("(lobby)>")
		ucmd = ucmd.lower()
		try:
			if ucmd == "help":
				print("cmdthread: Crear socket de consola.")
				print("show: Mostrar consolas.")
				print("connect (puerto): Conectarse a una consola.")
				print("close (numero de consola): cerrar hilo de tal consola.")
				print("exit: salir.")
			elif ucmd == "show":
				for consolenum in main.consoles:
					print("{}: {}".format(consolenum, main.consoles[consolenum][0]))
			elif ucmd == "cmdthread":
				cnsl = Thread(target=main.createconsole)
				cnsl.daemon = True
				cnsl.start()
			elif ucmd[:5] == "close":
				main.consoles["Console {}".format(ucmd[6:])][1] = False
			elif ucmd[:7] == "connect":
				p = int(ucmd[8:])
				usersock.connect(("127.0.0.1", p))
				console = usersock.recv(1024).decode()
				try:
					for i in range(0,len(main.consoles[console][2])):
						c = main.consoles[console][4][i]
						d = main.consoles[console][3][i]
						o = main.consoles[console][2][i]
						print("{}>{}\n{}".format(d,c,o))
						chdir(d)
				except:
					pass
				cc = " "
				while cc != "disconnect":
					cc = raw_input("{}({})>".format(getcwd(),console))
					if cc.lower() == "disconnect" or cc.lower() == "exit":
					    usersock.send("exit".encode())
					    break 
					usersock.send(cc.encode())
					print(usersock.recv(1024).decode())
		except Exception as e:
			print(e)

	