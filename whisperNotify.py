#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import json
import time
from datetime import datetime
import pushbullet
from playsound import playsound

version = '0.9.3'
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

def MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound):
	try:
		if os.path.getsize("E:\\Client.txt")/1024/1024>10:
			print '\nLog file size must be less than 5MB'
			exitApp()
		checkedLine = None
		with open(LogPath,'r') as f:
			while True:
				line = f.readline()
				if not line:
					break
				checkedLine = line.strip()
				monitorMessage = True
		while True:
			with open(LogPath,'r') as f:
				lines = f.readlines()
				if monitorMessage:
					print "\nWaiting for trade whisper...\n"
					monitorMessage = False
			if lines[-1].strip() != checkedLine:
				checkedLine = lines[-1].strip()
				if checkedLine:
					if (filterFrom in checkedLine and (filterA in checkedLine or filterB in checkedLine)):
						lineToSend = '@' + checkedLine.split(' @', 1)[-1]
						print datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
						print("New whisper: " + lineToSend)
						if notificationSound: playNotificationSound(notificationSound)
						print("Sending notification...")
						pushNotify(pushbulletAPItoken, lineToSend)
						monitorMessage = True
			time.sleep(delay)
	except Exception, e:
		print "\nError: " + str(e)
		exitApp()

def main(argv):
	print '\nTradeWhisperNotifier for PoE'
	print 'version: ' + str(version)
	print '(' + link + ')'
	print '(To exit press CTRL+C)'
	delay = 0.500
	pushbulletAPItoken = None
	LogPath = None
	filters = None
	notificationSound = None

	try:
		opts, args = getopt.getopt(argv,"t:p:s:d:",["token", "path", "sound", "delay"])
	except getopt.GetoptError:
	   print '\nUsage: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: 1 - 1sec, 0.5 - 0.5sec, 0.05 - 0,05sec and so on) (optional) (if not specified - 0.5sec)>'
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
				print "\nError: bad delay parameter (example: 1, 0.5, 0.05 ...). Using defaults (0.5 sec)..."			

	if not pushbulletAPItoken:
		print '\nPushbullet API token not specified'
		print '\nUsage: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: 1 - 1sec, 0.5 - 0.5sec, 0.05 - 0,05sec and so on) (optional) (if not specified - 0.5sec)>'
		exitApp()
	if not LogPath:
		print '\n Path to log file not specified'
		print '\nUsage: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: 1 - 1sec, 0.5 - 0.5sec, 0.05 - 0,05sec and so on) (optional) (if not specified - 0.5sec)>'
		exitApp()

	config = loadConfig()

	try:
		if config:
			filterFrom = config['filters']['filterFrom'].encode("utf-8")
			filterA = config['filters']['filterA'].encode("utf-8")
			filterB = config['filters']['filterB'].encode("utf-8")
			MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay, notificationSound)
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

def exitApp():
	raw_input("\nPress enter to exit")
	sys.exit(2)

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		print 'Exit... (Keyboard Interrupt)'
		sys.exit(2)
