#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, os
#import psutil
import json
import time
#from pushbullet import Pushbullet
import pushbullet


version = '0.9.0'
link = 'https://github.com/Doberm4n/POETradeWhisperNotifier'

def pushNotify(pushbulletAPItoken, msg):
	try:
		pbInstance = pushbullet.Pushbullet(pushbulletAPItoken)
		pbInstance.push_note("New whisper: ", msg)
		#print(pbInstance.push.status_code)
		print "Ok"
	except pushbullet.errors.InvalidKeyError:
		print "Error: Invalid api key. Please check your access token" 
		#print "Exit..."
		return
		#sys.exit(2)
	except pushbullet.errors.PushError as error:
		print "Error: " + str(error)
		return
		#print "CTRL+C to exit..."
	except Exception, e:
		print "Error sending notification: " + str(e)
		return
		#print "CTRL+C to exit..."

def MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB):
	try:
		#print "Monitoring log file..."
		checkedLine = None
		with open(LogPath,'r') as f:
			while True:
				line = f.readline()
				if not line:
					break
				#print(line)
				checkedLine = line.strip()
				checkedLength = sum(1 for line in open(LogPath))
				monitorMessage = True
		while True:
			with open(LogPath,'r') as f:
				lines = f.readlines()
				newCheckedLength = len(lines)
				if monitorMessage:
					print "\nMonitoring log file..."
					monitorMessage = False
			if (lines[-1].strip() != checkedLine) or (newCheckedLength > checkedLength):
				#print 'lines[-1]' + lines[-1]
				#print 'checkedLine' + checkedLine
				checkedLine = lines[-1].strip()
				checkedLength = newCheckedLength
				if checkedLine:
					if (filterFrom in checkedLine and (  (('buy' in checkedLine) or ('wtb' in checkedLine))    or  ((filterA in checkedLine) or (filterB in checkedLine)) )     ):
						print("New whisper: " + '@' + checkedLine.split(' @', 1)[-1])
						print("Sending notification...")
						pushNotify(pushbulletAPItoken, checkedLine)
						monitorMessage = True
			time.sleep(0.500)
	except Exception, e:
		print "Error: " + str(e)
		sys.exit(2)

def main(argv):
	print '\nTradeWhisperNotifier for PoE'
	print 'version: ' + str(version)
	print '(' + link + ')'
	delay = 5
	pushbulletAPItoken = None
	LogPath = None
	filters = None

	try:
		opts, args = getopt.getopt(argv,"t:p:c:l:a:d:r:",["token", "path", "lang" "character", "league", "accountName", "delay", "indexRange"])
	except getopt.GetoptError:
	   print 'Usage: -t <token> -p <path to log file>'
	   sys.exit(2)
	for opt, arg in opts:
		if opt in ("-t", "--token"):
			pushbulletAPItoken = str(arg)
		elif opt in ("-p", "--path"):
			LogPath = str(arg)
		elif opt in ("-l", "--lang"):
			lang = str(arg)

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
		#print filterFrom
		#print filterA
		#print filterB
		#f= open("text.txt","w+")
		#f.write(filterA)
		#f.close
		MonitorLogs(LogPath, pushbulletAPItoken, filterFrom, filterA, filterB)

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
	#CTRL + C
	except KeyboardInterrupt:
		print 'Exit... (Keyboard Interrupt)'
		sys.exit(2)
