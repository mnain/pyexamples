#!/usr/bin/env python

import time
import sys
import multiprocessing
import subprocess
import time
import glob
import logging
import logging.config

_YOUTUBE_PATH='../python/youtube-dl'
_LOG_CONFIG = 'tkelog.conf'

class LogProc(multiprocessing.Process):

	logger = None

	def __init__(self, daemon=True):
		print("LogProc::init")
		logging.config.fileConfig(_LOG_CONFIG)
		self.logger = logging.getLogger('TKEM')
	
	def run(self, url, audioOnly):
		print("LogProc::Run {} {}".format(url,audioOnly))
		self.logger.info('LogProc::Run {} {}'.format(url,audioOnly))
		if audioOnly.startswith('Audio'):
			cmds = ["python "+_YOUTUBE_PATH+" --no-progress -i -x --audio-format  mp3 --no-check-certificate "+url,]
		else:
			cmds = ["python "+_YOUTUBE_PATH+" --no-progress -f mp4 --no-check-certificate "+url,]
		self.logger.info('CMDS: {}'.format(str(cmds)))
		timeStamp = time.strftime("%H%M%S")
		stdoutName = "output_"+timeStamp+".log"
		stderrName = "error_"+timeStamp+".log"
		self.logger.info("Filenames {} {}".format(stdoutName, stderrName))
		stdoutFh = open(stdoutName, 'wt')
		stderrFh = open(stderrName, 'wt')
		rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
		self.logger.info("RC = {}".format(rc))
		stdoutFh.close()
		stderrFh.close()

if __name__ == "__main__":
	ytUrl = 'None'
	while ytUrl.startswith('q') == False:
		ytUrl = input('Enter Url:')
		#print('URL: {}'.format(ytUrl))
		lp = LogProc()
		lp.run(ytUrl, 'Audio')
		#print(multiprocessing.get_start_method())
		#print(multiprocessing.cpu_count())
