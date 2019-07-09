#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
import json
import time
import pushbullet


version = '0.9.0'
link = 'https://git.io/fjiyW'

def pushNotify(pushbulletAPItoken, msg):
	try:
		pbInstance = pushbullet.Pushbullet(pushbulletAPItoken)
		pbInstance.push_note("New whisper: ", msg)
		print "Ok"
	except pushbullet.errors.InvalidKeyError:
		print "Error: Invalid api key. Please check your access token" 
		print "Exit..."
		sys.exit(2)
	except pushbullet.errors.PushError as error:
		print "Error: " + str(error)
		return
	except Exception, e:
		print "Error sending notification: " + str(e)
		return

def MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay):
	try:
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
					print "\nMonitoring log file...\n"
					monitorMessage = False
			if lines[-1].strip() != checkedLine:
				checkedLine = lines[-1].strip()
				if checkedLine:
					if (filterFrom in checkedLine and ('buy' in checkedLine or 'wtb' in checkedLine)):
						lineToSend = '@' + checkedLine.split(' @', 1)[-1]
						print("New whisper: " + lineToSend)
						print("Sending notification...")
						pushNotify(pushbulletAPItoken, lineToSend)
						monitorMessage = True
			time.sleep(delay)
	except Exception, e:
		print "\nError: " + str(e)
		sys.exit(2)

def main(argv):
	print '\nTradeWhisperNotifier for PoE'
	print 'version: ' + str(version)
	print '(' + link + ')'
	print '(To exit press CTRL+C)'
	delay = 0.500
	pushbulletAPItoken = None
	LogPath = None
	filters = None

	try:
		opts, args = getopt.getopt(argv,"t:p:",["token", "path"])
	except getopt.GetoptError:
	   print 'Usage: -t <token> -p <path to log file>'
	   sys.exit(2)
	for opt, arg in opts:
		if opt in ("-t", "--token"):
			pushbulletAPItoken = str(arg)
		elif opt in ("-p", "--path"):
			LogPath = str(arg)

	if not pushbulletAPItoken:
		print '\nPushbullet API token not specified'
		print '\nUsage: -t <token> -p <path to log file>'
		sys.exit(2)
	if not LogPath:
		print '\n Path to log file not specified'
		print '\nUsage: -t <token> -p <path to log file>'
		sys.exit(2)

	config = loadConfig()

	if config:
		filterFrom = config['filters']['filterFrom'].encode("utf-8")
		filterA = config['filters']['filterA'].encode("utf-8")
		filterB = config['filters']['filterB'].encode("utf-8")
		MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB, delay)

def loadConfig():
    try:
        with open('config\\filters.json') as data_file:
            return json.load(data_file)
    except Exception, e:
        print "\nError: " + str(e)
        print 'Please check filters config file (' + "\\" + 'Config' + "\\" + 'filters.json)'

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		print 'Exit... (Keyboard Interrupt)'
		sys.exit(2)
