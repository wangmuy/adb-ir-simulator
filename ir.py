#!/usr/bin/python
## @package ir
#  @author wangzhongdi

import sys
import time
from java.net import SocketException
from java.lang import NullPointerException
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import subprocess

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            error = subprocess.CalledProcessError(retcode, cmd)
            error.output = output
            raise error
        return output
    subprocess.check_output = f

class IrToolMonkey:
	def connect(self, serialName):
		print "connecting %s" % serialName
		self.device = MonkeyRunner.waitForConnection(10, serialName)
		print "device=%s" % self.device

	def press(self, keyCode, flags):
		self.device.press(keyCode, flags)

class IrToolAdb:
	def connect(self, serialName):
		cmd="adb connect "+serialName
		out, ret = self.safeCall(cmd)
		print out

	def press(self, keyCode, flags):
		out, ret = self.safeCall("adb shell input keyevent "+keyCode)
		if out != None and out != "":
			print out

	def safeCall(self, cmd):
		try:
			output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
			return (output,0)
		except subprocess.CalledProcessError, e:
			return (e.output, e.returncode)

commandDict = {
'up'	:	'KEYCODE_DPAD_UP',
'down'	:	'KEYCODE_DPAD_DOWN',
'dn'	:	'KEYCODE_DPAD_DOWN',
'left'	:	'KEYCODE_DPAD_LEFT',
'lt'	:	'KEYCODE_DPAD_LEFT',
'right'	:	'KEYCODE_DPAD_RIGHT',
'rt'	:	'KEYCODE_DPAD_RIGHT',
'back'	:	'KEYCODE_BACK',
'bk'	:	'KEYCODE_BACK',
'enter'	:	'KEYCODE_ENTER',
'et'	:	'KEYCODE_ENTER',
'ok'	:	'KEYCODE_ENTER',
'menu'	:	'KEYCODE_MENU',
'home'	:	'KEYCODE_HOME',
'search':	'KEYCODE_SEARCH',
'pgup'	:	'KEYCODE_PAGE_UP',
'pgdn'	:	'KEYCODE_PAGE_DOWN',
'red'	:	'KEYCODE_PROG_RED',
'green'	:	'KEYCODE_PROG_GREEN',
'yellow':	'KEYCODE_PROG_YELLOW',
'blue'	:	'KEYCODE_PROG_BLUE',
'0'		:	'KEYCODE_0',
'1'		:	'KEYCODE_1',
'2'		:	'KEYCODE_2',
'3'		:	'KEYCODE_3',
'4'		:	'KEYCODE_4',
'5'		:	'KEYCODE_5',
'6'		:	'KEYCODE_6',
'7'		:	'KEYCODE_7',
'8'		:	'KEYCODE_8',
'9'		:	'KEYCODE_9',
'*'		:	'KEYCODE_STAR',
'#'		:	'KEYCODE_POUND',
'volup'	:	'KEYCODE_VOLUME_UP',
'voldn'	:	'KEYCODE_VOLUME_DOWN',
'caps'	:	'KEYCODE_CAPS_LOCK',
'A'		:	'KEYCODE_A',	'B'		:	'KEYCODE_B',
'C'		:	'KEYCODE_C',	'D'		:	'KEYCODE_D',
'E'		:	'KEYCODE_E',	'F'		:	'KEYCODE_F',
'G'		:	'KEYCODE_G',	'H'		:	'KEYCODE_H',
'I'		:	'KEYCODE_I',	'J'		:	'KEYCODE_J',
'K'		:	'KEYCODE_K',	'L'		:	'KEYCODE_L',
'M'		:	'KEYCODE_M',	'N'		:	'KEYCODE_N',
'O'		:	'KEYCODE_O',	'P'		:	'KEYCODE_P',
'Q'		:	'KEYCODE_Q',	'R'		:	'KEYCODE_R',
'S'		:	'KEYCODE_S',	'T'		:	'KEYCODE_T',
'U'		:	'KEYCODE_U',	'V'		:	'KEYCODE_V',
'W'		:	'KEYCODE_W',	'X'		:	'KEYCODE_X',
'Y'		:	'KEYCODE_Y',	'Z'		:	'KEYCODE_Z',
','		:	'KEYCODE_COMMA',
'.'		:	'KEYCODE_PERIOD',
'\t'	:	'KEYCODE_TAB',
'tab'	:	'KEYCODE_TAB',
' '		:	'KEYCODE_SPACE',
'space'	:	'KEYCODE_SPACE',
'del'	:	'KEYCODE_DEL',
'`'		:	'KEYCODE_GRAVE',
'-'		:	'KEYCODE_MINUS',
'='		:	'KEYCODE_EQUALS',
'\\'	:	'KEYCODE_BACKSLASH',
'/'		:	'KEYCODE_SLASH',
';'		:	'KEYCODE_SEMICOLON',
'@'		:	'KEYCODE_AT',
'['		:	'KEYCODE_LEFT_BRACE',
']'		:	'KEYCODE_RIGHT_BRACE',
}

def my_raw_input(hint):
    print hint
    return sys.stdin.readline()

def repl(irTool):
	global commandDict
	while True:
		try:
			cmd = raw_input("ir: ")
			#print 'cmd=%s' % cmd
			if cmd in commandDict:
				irTool.press(commandDict[cmd], MonkeyDevice.DOWN_AND_UP)
			elif cmd == "quit":
				break
			else:
				splitted = cmd.split(' ', 2)
				if len(splitted) == 2:
					if splitted[0] == "connect":
						irTool.connect(splitted[1])
					elif splitted[0] == 'lp' and splitted[1] in commandDict:
						for i in range(0, 10):
							irTool.press(commandDict[splitted[1]], MonkeyDevice.DOWN_AND_UP)
		except NullPointerException:
			print 'run command "%s" failed, not connected?' % cmd
		except EOFError:
			break
		except Exception, e:
			print 'unknown error: %s' % str(e)
			break

if __name__ == "__main__":
	if(len(sys.argv) < 2):
		print  "ir: a tool to send key strokes to connected android emulator/device\nusage: monkeyrunner.bat /path/to/ir.py DEVICE_SERIAL_NAME\n"
		sys.exit(0)
	irTool = IrToolAdb() # IrToolMonkey
	irTool.connect(sys.argv[1])
	repl(irTool)

