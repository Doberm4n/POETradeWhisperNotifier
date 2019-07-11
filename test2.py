import os
import time
from datetime import datetime

lp = 0

#with open("E:\\test.txt",'r') as f:
	#while True:
		#f.seek(lp)
		#line = f.readline()
		#lp = f.tell()
		#print 
		#print line
		#print str(f.seek(2))
#time.sleep(5)

with open("E:\\Client.txt_",'r') as f:
			f.seek(0, os.SEEK_END)
			checkedPos = f.tell()
			#line = f.readline()
			print str(checkedPos)
			#endf = f.tell() 
			#print 'endf ' + str(endf)
			#while True:

				#line = f.readline()
				#print line
				#if not line:
					#break
				#print 'str ' + str(line.strip()) + '   Tell ' + str(f.tell())
			
				
			#checkedLine = line.strip()
			# = f.tell()
			#print str(checkedPos)
			monitorMessage = True
			#f.seek(199)
			#test = f.readline().strip()
			#print test
			#if len(test)>5: print "Ok"
			#print len(f.readline().strip()
			#print f.readline()

while True:
	with open("E:\\Client.txt_",'r') as f:
		f.seek(checkedPos)
		print 'checkedPos  ' + str(checkedPos)
		newLine = f.readline().strip()
		lineLength = len(newLine)
		currentPos = f.tell()
		if monitorMessage:
			print "\nWaiting for trade whisper...\n"
			monitorMessage = False
		if checkedPos < currentPos:
			checkedLine = newLine.strip()
			checkedPos = f.tell()
			if checkedLine:
				print datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
				print("New whisper: " + newLine)
				monitorMessage = True
				
	time.sleep(0.05)