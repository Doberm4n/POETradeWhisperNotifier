# POETradeWhisperNotifier
## Trade whisper notifier for PoE

> Simple app that monitors PoE log file with specified filters for trade whispers and sends a Pushbullet notification

**Installation:**
- install Python 2.7
- pip install pushbullet.py

**Usage:** 
- check or/and edit whisper filters in \Config\filters.json (app filters log for messages that start with <filterFrom> and contains <filterA> or <filterB>)
- python whisperNotify.py -t "pushbullet API token" (without quotes) -p "full path to Client.txt file" (with quotes)
- you can always put cmd line into .bat or .cmd file for quick use (end that file with "pause" to see any errors)
