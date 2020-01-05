#!/usr/bin/env python

import sys
import os
import tkinter
import subprocess
import time
import glob
import logging
import logging.config
import multiprocessing

_YOUTUBE_PATH='../python/youtube-dl'
_LOG_CONFIG = 'tkelog.conf'
_logger = None

class Download(multiprocessing.Process):
	def __initialize__(self, url, audio):
		multiprocessing.Process.__init__()
		_logger.info('Download initialize with : {} {}'.format(url,audio))
		self.url = url
		self.audioOnly = audio

	def run(self):
		_logger.info('Download run: {} {}'.format(self.url, self.audioOnly))

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
		cmds = ["python "+_YOUTUBE_PATH+" --no-progress -i -x --audio-format  mp3 --no-check-certificate "+url,]
	if audio.startswith('Video'):
		cmds = ["python "+_YOUTUBE_PATH+" --no-progress -f mp4 --no-check-certificate "+url,]
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
	dl = Download(txt, aOnly)

if __name__ == "__main__":
	logging.config.fileConfig(_LOG_CONFIG)
	_logger = logging.getLogger('TKE')
	_logger.info('Starting...')
	cleanLogs()
	root = tkinter.Tk()
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
	lbl.text = 'So far'
	lbl.update()
	root.mainloop()
	cleanLogs()
	_logger.info('End')
