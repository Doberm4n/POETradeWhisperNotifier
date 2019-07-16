<img align="left" width="100" height="100" src="https://github.com/Doberm4n/POETradeWhisperNotifier/blob/master/res/message.png">

# POETradeWhisperNotifier 
<br>

## Trade whisper notifier for PoE

> Simple console app that monitors PoE log file with specified filters for trade whispers and sends a Pushbullet notification

> This app does not change any of the game files and do not interfere with memory used by game. All that it does is reading Client.txt file

![alt text](https://github.com/Doberm4n/POETradeWhisperNotifier/blob/master/res/screenshot.png)
 
**Installation:**
- install Python 2.7
- pip install pushbullet.py
- pip install playsound
- pip install colorama

>or download and unpack .zip from [releases](https://github.com/Doberm4n/POETradeWhisperNotifier/releases/latest)

**Usage:** 
1. before first run, open \config\config.json:
   - set path to log file:
     - for example: "logPath": "D:\\\Test\\\Client.txt" (two slashes)
   - set your API token
     - for example: "apiKey": "your api token"
   - disable or enable flood filter and set flood filter delay ("floodFilter": {) (values: 0.5 - 0.5sec and so on), for example:
     - "enabled": true,
     - "delay": 5
   - set log read delay (values: 0.5 - 0.5sec and so on)
     - for example: "readDelay": 2
   - disable or enable sound notifications ("sound": {), for example:
     - "enabled": true
     - "pathToSoundFile": "D:\\\Test\\\notification.mp3" (two slashes)
2. check or/and edit whisper filters in \config\config.json ("filters": {) (app filters log for messages that start with "filterFrom" value and contains "filterA" or "filterB" values). By deafult, in this repository config.json contains filters for EN language:
   - "filterFrom": "@From",
   - "filterA": "buy",
   - "filterB": "wtb"
4. save \config\config.json with UTF-8 encoding
3.  python whisperNotify.py
>or
run whisperNotify.exe 
4. the smaller the log file, the faster the application, log filesize at start must be less than 50MB


POETradeWhisperNotifier application as a standalone package with .exe is available on the [releases page](https://github.com/Doberm4n/POETradeWhisperNotifier/releases/latest)

Repository: https://git.io/fjiyW
