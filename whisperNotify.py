#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import json
import time
from datetime import datetime
import pushbullet
from playsound import playsound
import threading

version = '0.9.5'
link = 'https://git.io/fjiyW'

def pushNotify(pushbulletAPItoken, msg):
	try:
		pbInstance = pushbullet.Pushbullet(pushbulletAPItoken)
		pbInstance.push_note("New whisper: ", msg)
		print "Ok"
		print "Waiting for delay..."
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

def MonitorLogs(logPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound, maxLogSizeMB, floodFilterDelay, isFloodFilterDelay):
	try:
		if os.path.getsize(logPath)/1024/1024>maxLogSizeMB:
			print '\nLog file size must be less than '+ str(maxLogSizeMB) + 'MB'
			exitApp()
		with open(logPath,'r') as f:
			f.seek(0, os.SEEK_END)
			checkedPos = f.tell()
			monitorMessage = True
			startTime = time.time()
			floodTimer = floodFilterDelay
			isInitWhisper = True
		while True:
			with open(logPath,'r') as f:
				f.seek(checkedPos)
				newLine = unicode(f.readline().strip(), "utf-8")
				currentPos = f.tell()
				if monitorMessage:
					print "\nWaiting for trade whisper...\n"
					print 'in waiting floodTimer ' + str(floodTimer)
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
								print 'in send floodTimer ' + str(floodTimer)
							elif not isFloodFilterDelay:
								if notificationSound: playNotificationSound(notificationSound)
								print("Sending notification...")
								pushNotify(pushbulletAPItoken, lineToSend)
							else:
								print "Skipping this whisper notifications because of flood filter"
								print "Waiting for delay..."
							monitorMessage = True
							i = 0
				if not isInitWhisper: floodTimer = time.time() - startTime
			print 'in sleep floodTimer ' + str(floodTimer)
			time.sleep(delay)
	except Exception, e:
		print "\nError: " + str(e)
		exitApp()

def main(argv):
	print '\nTradeWhisperNotifier for PoE'
	print 'version: ' + str(version)
	print '(' + link + ')'
	print '(To exit press CTRL+C)'
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
				print "(Log file not found)"
				print "Please check log file"
				print "Exit..."
				exitApp()
			delay = config['settings']['readDelay']
			print "(Log reading delay: " + str(delay) + "sec)"
			pushbulletAPItoken = config['settings']['apiKey'].encode("utf-8")
			isFloodFilterDelay = config['settings']['floodFilter']['enabled']
			if isFloodFilterDelay: 
				floodFilterDelay = config['settings']['floodFilter']['delay']
				print "(Flood filter enabled, delay: " + str(floodFilterDelay) + "sec)"
			filterFrom = config['filters']['filterFrom'].encode("utf-8")
			filterA = config['filters']['filterA'].encode("utf-8")
			filterB = config['filters']['filterB'].encode("utf-8")
			soundEnabled = config['settings']['sound']['enabled']
			if soundEnabled: 
				print "(Sound notifications enabled)"
				notificationSound = config['settings']['sound']['pathToSoundFile'].encode("utf-8")
				if not os.path.isfile(notificationSound): 
					notificationSound = None
					print "(Sound notification file not found)"
			print "Config loaded"
			MonitorLogs(logPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound, maxLogSizeMB, floodFilterDelay, isFloodFilterDelay)
	except Exception, e:
		print "\nError: " + str(e)
		print 'Please check config file (' + "\\" + 'Config' + "\\" + 'config.json)'
		exitApp()

def loadConfig():
	try:
		print "\nLoading config..."
		with open('config\\config.json') as data_file:
			return json.load(data_file)
	except Exception, e:
		print "\nError: " + str(e)
		print 'Please check config file (' + "\\" + 'Config' + "\\" + 'config.json)'
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
		print '\n\nExit... (Keyboard Interrupt)'
		raw_input("\nPress enter to exit")
		sys.exit(2)
