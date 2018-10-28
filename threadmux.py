#-*-coding: utf-8-*-
from threading import *
from os import system, popen, getcwd, chdir
from platform import python_version as pv

if __name__ == '__main__':
	if str(pv())[0] == "3":
		raw_input = input
	cmd = ""
	while cmd.lower() != "exit":
		cmd = raw_input("{}>".format(getcwd()))
		try:
			if cmd[:3].lower() == "thr" and len(cmd) > 4:
				st = Thread(target = system, args=(cmd[4:],))
				st.daemon = True
				st.start()
			elif cmd[:12] == "inhibitedthr" and len(cmd) > 13:
				st = Thread(target = popen, args=(cmd[13:],))
				st.daemon = True
				st.start()
			else:
				if cmd[:2].lower() == "cd":
					chdir(cmd[3:])
				else:
					system(cmd)
		except Exception as e:
			print(e)
