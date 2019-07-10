rmdir /Q /S build
rmdir /Q /S dist
c:\Python27\Scripts\pyinstaller whisperNotify.py --noupx --icon=res\message.ico --version-file=version.txt
pause