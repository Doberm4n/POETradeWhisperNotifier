#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import json
import time
from datetime import datetime
import pushbullet
from playsound import playsound
from colorama import init
from colorama import Fore, Back, Style

version = '0.9.50'
link = 'https://git.io/fjiyW'

def pushNotify(pushbulletAPItoken, msg):
	try:
		pbInstance = pushbullet.Pushbullet(pushbulletAPItoken)
		#pbInstance.push_note("New whisper: ", msg)
		printLine ("S","Ok")
		printLine('C', "Waiting for delay...")
	except pushbullet.errors.InvalidKeyError:
		printLine('E', "Error: Invalid api key. Please check your access token") 
		printLine('E', "Exit...")
		exitApp()
	except pushbullet.errors.PushError as error:
		printLine('E', "Error: " + str(error))
		return
	except Exception, e:
		printLine('E', "Error sending notification: " + str(e))
		return

def MonitorLogs(logPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound, maxLogSizeMB, floodFilterDelay, isFloodFilterDelay):
	try:
		if os.path.getsize(logPath)/1024/1024>maxLogSizeMB:
			printLine('E', '\nLog file size must be less than '+ str(maxLogSizeMB) + 'MB')
			exitApp()
		with open(logPath,'r') as f:
			f.seek(0, os.SEEK_END)
			checkedPos = f.tell()
			monitorMessage = True
			startTime = time.time()
			floodTimer = floodFilterDelay
			isInitWhisper = True
			curProgressIndicator = 0
			indicatorsList = ['|', '/', '-', '\\', '|', '/', '-', '\\']
		while True:
			with open(logPath,'r') as f:
				f.seek(checkedPos)
				newLine = unicode(f.readline().strip(), "utf-8")
				currentPos = f.tell()
				if monitorMessage:
					printLine('WW', "\nWaiting for trade whisper...\n")
					monitorMessage = False
					i = 0
					#print ' Reading...' + str(i)+ ' (in progress...)\r',
					printLine('P', '  Reading...' + str(i)+ ' (in progress...)\r')
				if checkedPos < currentPos:
					checkedLine = newLine.strip()
					checkedPos = f.tell()
					if checkedLine:
						i += 1
						#print ' Reading...' + str(i)+ ' (in progress...)\r',
						printLine('P', '  Reading...' + str(i)+ ' (in progress...)\r')
						if (filterFrom in checkedLine and (filterA in checkedLine or filterB in checkedLine)):
							lineToSend = '@' + checkedLine.split(' @', 1)[-1]
							printLine('C', '\n\n' + datetime.now().strftime('[%Y-%m-%d %H:%M:%S]'))
							printLine('NW', "New whisper: " + lineToSend)	
							if (floodTimer >= floodFilterDelay) and isFloodFilterDelay:
								if notificationSound: playNotificationSound(notificationSound)
								printLine('C', "Sending notification...")
								pushNotify(pushbulletAPItoken, lineToSend)
								startTime = time.time()
								floodTimer = 0
								isInitWhisper = False
							elif not isFloodFilterDelay:
								if notificationSound: playNotificationSound(notificationSound)
								printLine('C', "Sending notification...")
								pushNotify(pushbulletAPItoken, lineToSend)
							else:
								printLine('Y', "Skipping this whisper notifications because of flood filter")
								printLine('C', "Waiting for delay...")
							monitorMessage = True
							i = 0
				if not monitorMessage: print indicatorsList[curProgressIndicator] + '\r',
				curProgressIndicator += 1
				if curProgressIndicator > 7: curProgressIndicator = 0
			time.sleep(delay)
			if not isInitWhisper: floodTimer = time.time() - startTime
			
	except Exception, e:
		printLine('E', "\nError: " + str(e))
		exitApp()

def main(argv):
	init()
	printLine('A' ,'\n                              ')
	printLine('A' ,' TradeWhisperNotifier for PoE ')
	printLine('A' ,' version: ' + str(version) + '              ')
	printLine('A' ,' (' + link + ')       ')
	printLine('A' ,'                              ')
	printLine('W' ,' (To exit press CTRL+C)       ')

	delay = None
	pushbulletAPItoken = None
	logPath = None
	filters = None
	notificationSound = None
	soundEnabled = None
	maxLogSizeMB = 50
	floodFilterDelay = None
	isFloodFilterDelay = None

	try:
		config = loadConfig()
		if config:
			logPath = config['settings']['logPath'].encode("utf-8")
			if not os.path.isfile(logPath): 
				printLine('E' ,"(Log file not found)")
				printLine('E' ,"Please check log file")
				printLine('E' ,"Exit...")
				exitApp()
			delay = config['settings']['readDelay']
			printLine('C', "(Log reading delay: " + str(delay) + "sec)")
			pushbulletAPItoken = config['settings']['apiKey'].encode("utf-8")
			isFloodFilterDelay = config['settings']['floodFilter']['enabled']
			if isFloodFilterDelay: 
				floodFilterDelay = config['settings']['floodFilter']['delay']
				printLine('C', "(Flood filter enabled, delay: " + str(floodFilterDelay) + "sec)")
			filterFrom = config['filters']['filterFrom'].encode("utf-8")
			filterA = config['filters']['filterA'].encode("utf-8")
			filterB = config['filters']['filterB'].encode("utf-8")
			soundEnabled = config['settings']['sound']['enabled']
			if soundEnabled: 
				printLine('C', "(Sound notifications enabled)")
				notificationSound = config['settings']['sound']['pathToSoundFile'].encode("utf-8")
				if not os.path.isfile(notificationSound): 
					notificationSound = None
					printLine('E', "(Sound notification file not found)")
			printLine('S', "Config loaded")
			MonitorLogs(logPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound, maxLogSizeMB, floodFilterDelay, isFloodFilterDelay)
	except Exception, e:
		printLine('E', "\nError: " + str(e))
		printLine('E', 'Please check config file (' + "\\" + 'Config' + "\\" + 'config.json)')
		exitApp()

def loadConfig():
	try:
		printLine ('C', "\nLoading config...")
		with open('config\\config.json') as data_file:
			return json.load(data_file)
	except Exception, e:
		printLine('E', "\nError: " + str(e))
		printLine('E', 'Please check config file (' + "\\" + 'Config' + "\\" + 'config.json)')
		exitApp()

def playNotificationSound(path):
	try:
		printLine('C', 'Playing sound notification...')
		playsound(path, False)
	except Exception, e:
		printLine('E', "Error playing sound notification. Please check sound file")
		return

def printLine(style, line):
	if style == 'A':
		print (Fore.WHITE + Back.GREEN + Style.BRIGHT + line)
	if style == 'W':
		print (Fore.WHITE + Style.BRIGHT + line)
	elif style == 'S':
		print (Fore.GREEN + Style.BRIGHT + line)
	elif style == 'P':
		print (Fore.WHITE + Style.DIM + line),
	elif style == 'NW':
		print (Fore.CYAN + Style.BRIGHT + line)
	elif style == 'WW':
		print (Fore.WHITE + Back.MAGENTA + Style.DIM + line)
	elif style == 'C':
		print (Fore.WHITE + Style.DIM + line)
	elif style == 'Y':
		print (Fore.YELLOW + Style.DIM + line)
	elif style == 'E':
		print (Fore.RED + Style.BRIGHT + line)
	print Style.RESET_ALL + '\r',
 
def exitApp():
	raw_input("\nPress [ENTER] to exit")
	sys.exit(2)

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		print '\n\nExit... (Keyboard Interrupt)'
		raw_input("\nPress [ENTER] to exit")
		sys.exit(2)
