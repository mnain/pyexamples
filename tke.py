#!/usr/bin/env python

import sys
import os
import tkinter
import subprocess
import time
import glob
import logging
import logging.config

__VERSION__ = "0.1a Jan. 11, 2020"
_YOUTUBE_PATH='../python/youtube-dl'
_LOG_CONFIG = 'tkelog.conf'
_logger = None
_globalYtver = "2020.01.01"

def updateYoutube():
	_logger.info('updateYoutube')
	cmds = ["python "+_YOUTUBE_PATH+" -U",]
	_logger.info(cmds)
	timeStamp = time.strftime("%H%M%S")
	stdoutName = "output_"+timeStamp+".log"
	stderrName = "error_"+timeStamp+".log"
	_logger.info("Filenames {} {}".format(stdoutName, stderrName))
	stdoutFh = open(stdoutName, 'wt')
	stderrFh = open(stderrName, 'wt')
	rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
	_logger.info("RC = {}".format(rc.returncode))
	stdoutFh.close()
	stderrFh.close()
	allOutLines = open(stdoutName, 'rt').readlines()
	allErrLines = open(stderrName, 'rt').readlines()
	for ao in allOutLines:
		_logger.info('updateYoutube(): {}'.format(ao.rstrip()))
	for ae in allErrLines:
		_logger.error('updateYoutube(): {}'.format(ae.rstrip()))
	_globalYtver = getYoutubeVersion()

def getYoutubeVersion():
	_logger.info('getYoutubeVersion')
	cmds = ["python "+_YOUTUBE_PATH+" --version",]
	_logger.info(cmds)
	timeStamp = time.strftime("%H%M%S")
	stdoutName = "output_"+timeStamp+".log"
	stderrName = "error_"+timeStamp+".log"
	_logger.info("Filenames {} {}".format(stdoutName, stderrName))
	stdoutFh = open(stdoutName, 'wt')
	stderrFh = open(stderrName, 'wt')
	rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
	_logger.info("RC = {}".format(rc.returncode))
	stdoutFh.close()
	stderrFh.close()
	allOutLines = open(stdoutName, 'rt').readlines()
	allErrLines = open(stderrName, 'rt').readlines()
	for ao in allOutLines:
		_logger.info('getYoutubeVersion(): {}'.format(ao.rstrip()))
	for ae in allErrLines:
		_logger.error('getYoutubeVersion(): {}'.format(ae.rstrip()))
	if rc.returncode == 0:
		_globalYtver = allOutLines[0].rstrip()
		#print('Version:{}'.format(_globalYtver))
	return _globalYtver

def cleanLogs():
	outFiles = glob.glob('output*log')
	_logger.info(str(outFiles))
	for o in outFiles:
		os.remove(o)
	errFiles = glob.glob('error*log')
	_logger.info(errFiles)
	for e in errFiles:
		os.remove(e)

def download(url, audio):
	_logger.info("Url: "+url+" audio: "+audio)
	if audio.startswith('Audio'):
		cmds = ["python "+_YOUTUBE_PATH+" --no-progress -i -x --audio-format  mp3 --no-check-certificate "+url+" &",]
	if audio.startswith('Video'):
		cmds = ["python "+_YOUTUBE_PATH+" --no-progress -f mp4 --no-check-certificate "+url+" &",]
	_logger.info(cmds)
	timeStamp = time.strftime("%H%M%S")
	stdoutName = "output_"+timeStamp+".log"
	stderrName = "error_"+timeStamp+".log"
	_logger.info("Filenames {} {}".format(stdoutName, stderrName))
	stdoutFh = open(stdoutName, 'wt')
	stderrFh = open(stderrName, 'wt')
	rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
	_logger.info("RC = {}".format(rc))
	stdoutFh.close()
	stderrFh.close()

def handleEntry():
	global lbl
	txt = entry.get()
	svar.set(txt)
	aOnly = audioVar.get()
	lbl.update()
	download(txt, aOnly)

if __name__ == "__main__":
	logging.config.fileConfig(_LOG_CONFIG)
	_logger = logging.getLogger('TKE')
	_logger.info('Starting...')
	cleanLogs()
	_globalYtver=getYoutubeVersion()
	root = tkinter.Tk()
	appVer = tkinter.StringVar()
	appVer.set(sys.argv[0] + ' : '+__VERSION__)
	appVerLbl = tkinter.Label(width=80, textvariable=appVer)
	appVerLbl.pack()
	entry = tkinter.Entry(width=45)
	entry.pack(),
	svar = tkinter.StringVar()
	svar.set('NONE')
	lbl = tkinter.Label(width=80, textvariable=svar)
	lbl.pack()
	audioVar = tkinter.StringVar()
	audioVar.set('Audio')
	audioOnly = tkinter.Checkbutton(text="Audio only", variable=audioVar, onvalue='Audio', offvalue='Video')
	audioOnly.pack()
	btn1 = tkinter.Button(text="Submit", command=handleEntry)
	btn1.pack()
	quit = tkinter.Button(text="Quit", command="exit")
	quit.pack()
	updateBtn = tkinter.Button(text='Update',  command="updateYoutube")
	updateBtn.pack()
	ytVer = tkinter.StringVar()
	ytVer.set(_globalYtver)
	ytVerLbl = tkinter.Label(width=80, textvariable=ytVer)
	ytVerLbl.pack()
	root.mainloop()
	cleanLogs()
	_logger.info('End')
