#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import json
import time
from datetime import datetime
import pushbullet
from playsound import playsound
import threading

version = '0.9.42'
link = 'https://git.io/fjiyW'

def pushNotify(pushbulletAPItoken, msg):
	try:
		pbInstance = pushbullet.Pushbullet(pushbulletAPItoken)
		pbInstance.push_note("New whisper: ", msg)
		print "Ok"
	except pushbullet.errors.InvalidKeyError:
		print "Error: Invalid api key. Please check your access token" 
		print "Exit..."
		exitApp()
	except pushbullet.errors.PushError as error:
		print "Error: " + str(error)
		return
	except Exception, e:
		print "Error sending notification: " + str(e)
		return

def MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound, maxLogSizeMB, floodFilterDelay, isFloodFilterDelay):
	try:
		if os.path.getsize(LogPath)/1024/1024>maxLogSizeMB:
			print '\nLog file size must be less than '+ str(maxLogSizeMB) + 'MB'
			exitApp()
		with open(LogPath,'r') as f:
			f.seek(0, os.SEEK_END)
			checkedPos = f.tell()
			monitorMessage = True
			startTime = time.time()
			floodTimer = floodFilterDelay
			isInitWhisper = True
		while True:
			with open(LogPath,'r') as f:
				f.seek(checkedPos)
				newLine = unicode(f.readline().strip(), "utf-8")
				currentPos = f.tell()
				if monitorMessage:
					print "\nWaiting for trade whisper...\n"
					monitorMessage = False
					i = 0
					print 'Reading...' + str(i)+ ' (in progress...)\r',
				if checkedPos < currentPos:
					checkedLine = newLine.strip()
					checkedPos = f.tell()
					i += 1
					print 'Reading...' + str(i)+ ' (in progress...)\r',
					if checkedLine:
						if (filterFrom in checkedLine and (filterA in checkedLine or filterB in checkedLine)):
							lineToSend = '@' + checkedLine.split(' @', 1)[-1]
							print '\n\n' + datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
							print("New whisper: " + lineToSend)	
							if (floodTimer >= floodFilterDelay) and isFloodFilterDelay:
								if notificationSound: playNotificationSound(notificationSound)
								print("Sending notification...")
								pushNotify(pushbulletAPItoken, lineToSend)
								startTime = time.time()
								floodTimer = 0
								isInitWhisper = False
							elif not isFloodFilterDelay:
								if notificationSound: playNotificationSound(notificationSound)
								print("Sending notification...")
								pushNotify(pushbulletAPItoken, lineToSend)
							else:
								print "Skipping this whisper notifications because of flood filter"
							monitorMessage = True
							i = 0
				if not isInitWhisper: floodTimer = time.time() - startTime
			time.sleep(delay)
	except Exception, e:
		print "\nError: " + str(e)
		exitApp()

def main(argv):
	print '\nTradeWhisperNotifier for PoE'
	print 'version: ' + str(version)
	print '(' + link + ')'
	print '(To exit press CTRL+C)'
	delay = 2.00
	pushbulletAPItoken = None
	LogPath = None
	filters = None
	notificationSound = None
	maxLogSizeMB = 50
	floodFilterDelay = 5.00
	isFloodFilterDelay = False

	try:
		opts, args = getopt.getopt(argv,"t:p:s:d:f:",["token", "path", "sound", "delay", "floodDelay"])
	except getopt.GetoptError:
	   print '\nUsage: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: -d 0.5 - 0.5sec and so on) (optional) (if not specified - 2sec) -f <flood filter delay (notify not often than this value)(example: -f 10 - 10sec and so on) (optional) (if not specified - 5sec)>'
	   exitApp()
	for opt, arg in opts:
		if opt in ("-t", "--token"):
			pushbulletAPItoken = str(arg)
		elif opt in ("-p", "--path"):
			LogPath = str(arg)
		elif opt in ("-s", "--sound"):
			notificationSound = str(arg)
		elif opt in ("-d", "--delay"):
			try:
				if (isinstance(float(arg), float)): delay = float(arg)
			except Exception, e:
				print "\nError: bad delay parameter (example: 1, 0.5, 0.05 ...). Using defaults (2 sec)..."		
		elif opt in ("-f", "--floodDelay"):
			try:
				if (isinstance(float(arg), float)): 
					floodFilterDelay = float(arg)
					isFloodFilterDelay = True
			except Exception, e:
				print "\nError: bad flood delay parameter (example: 1, 0.5, 0.05 ...). Using defaults (5 sec)..."		

	if not pushbulletAPItoken:
		print '\nPushbullet API token not specified'
		print '\nUsage: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: -d 0.5 - 0.5sec and so on) (optional) (if not specified - 2sec) -f <flood filter delay (notify not often than this value)(example: -f 10 - 10sec and so on) (optional) (if not specified - 5sec)>'
		exitApp()
	if not LogPath:
		print '\n Path to log file not specified'
		print '\nUsage: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: -d 0.5 - 0.5sec and so on) (optional) (if not specified - 2sec) -f <flood filter delay (notify not often than this value)(example: -f 10 - 10sec and so on) (optional) (if not specified - 5sec)>'
		exitApp()

	config = loadConfig()

	try:
		if config:
			filterFrom = config['filters']['filterFrom'].encode("utf-8")
			filterA = config['filters']['filterA'].encode("utf-8")
			filterB = config['filters']['filterB'].encode("utf-8")
			MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound, maxLogSizeMB, floodFilterDelay, isFloodFilterDelay)
	except Exception, e:
		print "\nError: " + str(e)
		print 'Please check filters config file (' + "\\" + 'Config' + "\\" + 'filters.json)'
		exitApp()

def loadConfig():
	try:
		with open('config\\filters.json') as data_file:
			return json.load(data_file)
	except Exception, e:
		print "\nError: " + str(e)
		print 'Please check filters config file (' + "\\" + 'Config' + "\\" + 'filters.json)'
		exitApp()

def playNotificationSound(path):
	try:
		print 'Playing sound notification...'
		playsound(path, False)
	except Exception, e:
		print "Error playing sound notification. Please check sound file"
		return

def floodTimer():
	return True

def exitApp():
	raw_input("\nPress enter to exit")
	sys.exit(2)

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		print 'Exit... (Keyboard Interrupt)'
		raw_input("\nPress enter to exit")
		sys.exit(2)
