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

>or download and unpack .zip from [releases](https://github.com/Doberm4n/POETradeWhisperNotifier/releases/latest)

**Usage:** 
- check or/and edit whisper filters in \config\filters.json (app filters log for messages that start with "filterFrom" value and contains "filterA" or "filterB" values). If edited, filters.json must be saved with UTF-8 encoding to support different game languages. By deafult, in this repository filters.json contains filters for EN language
- python whisperNotify.py -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: 1 - 1sec, 0.5 - 0.5sec, 0.05 - 0,05sec and so on) (optional) (without quotes) (if not specified - 0.5sec)> 
>or

> create shortcut for whisperNotify.exe with options: -t <token> -p <path to log file> -s <path to sound file (.wav, .mp3) (optional)> -d <delay interval for reading log file (example: 1 - 1sec, 0.5 - 0.5sec, 0.05 - 0,05sec and so on) (optional) (without quotes) (if not specified - 0.5sec)>
- you can always put cmd line for whisperNotify.py into .bat or .cmd file for quick use (end that file with "pause" to see any errors)
- the smaller the log file, the faster the application, log filesize at start must be less than 7MB to minimize resources consume


POETradeWhisperNotifier application as a standalone package with .exe is available on the [releases page](https://github.com/Doberm4n/POETradeWhisperNotifier/releases/latest)

Repository: https://git.io/fjiyW
