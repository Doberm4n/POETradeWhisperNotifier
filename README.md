# POETradeWhisperNotifier
## Trade whisper notifier for PoE

> Simple app that monitors PoE log file with specified filters for trade whispers and sends a Pushbullet notification

**Installation (if not using executable from releases):**
- install Python 2.7
- pip install pushbullet.py

**Usage:** 
- check or/and edit whisper filters in \Config\filters.json (app filters log for messages that start with <filterFrom> and contains <filterA> or <filterB>)
- python whisperNotify.py -t <pushbullet API token>
