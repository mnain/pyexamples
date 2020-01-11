#!/usr/bin/env python

import os
import sys
import subprocess
import time
import logging
import logging.config

_YOUTUBE_PATH='C:\\Users\\mnain\\Documents\\Src\\youtube-dl'
_PYTHON_PATH='C:\\Users\\mnain\\AppData\\Local\\Programs\\Python\\Python38\\python.exe '
_LOG_CONFIG = 'tkelog.conf'
_logger = None

if __name__ == "__main__":
	logging.config.fileConfig(_LOG_CONFIG)
	_logger = logging.getLogger('TKE')
	"""
	if os.path.exists(_YOUTUBE_PATH):
		print(_YOUTUBE_PATH+" found")
	else:
		print(_YOUTUBE_PATH+" not found")
	if os.path.exists(_PYTHON_PATH):
		print(_PYTHON_PATH+" found")
	else:
		print(_PYTHON_PATH+" not found")
	"""
	cmds = [_PYTHON_PATH,_YOUTUBE_PATH,"--version",]
	# cmds = [ "dir", ]
	timeStamp = time.strftime("%H%M%S")
	stdoutName = "output_"+timeStamp+".log"
	stderrName = "error_"+timeStamp+".log"
	_logger.info("Filenames {} {}".format(stdoutName, stderrName))
	stdoutFh = open(stdoutName, 'wt')
	stderrFh = open(stderrName, 'wt')
	rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
	# print(dir(rc))
	# print("rc = "+str(rc))
	_logger.info("RC = {}".format(rc))
	stdoutFh.close()
	stderrFh.close()
	allOutLines = open(stdoutName, 'rt').readlines()
	allErrLines = open(stderrName, 'rt').readlines()
	allOutLines = map(lambda x: x.rstrip(), allOutLines)
	allErrLines = map(lambda x: x.rstrip(), allErrLines)
	for ao in allOutLines:
		print('OUT: '+ao)
	for ae in allErrLines:
		print('ERR: '+ae)
