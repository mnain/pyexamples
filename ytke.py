#!/usr/bin/env python

import sys
import os
import tkinter
import subprocess
import time
import glob
import logging
import logging.config

class Youtube_DL_TKE:
    # class Vars
    __VERSION__ = "0.1a Jan. 11, 2020"
    YOUTUBE_PATH='.\\youtube-dl'
    LOG_CONFIG = 'tkelog.conf'
    # PYTHON_PATH = 
    logger = None
    globalYtver = "2020.01.01"

    def __init__(self):
        logging.config.fileConfig(self.LOG_CONFIG)
        self.logger = logging.getLogger('YTKE')
        self.logger.info('Starting...')
        self.cleanLogs()
        self.getYoutubeVersion()
        
    def cleanLogs(self):
        outFiles = glob.glob('output*log')
        self.logger.info(str(outFiles))
        for o in outFiles:
            os.remove(o)
        errFiles = glob.glob('error*log')
        self.logger.info(errFiles)
        for e in errFiles:
            os.remove(e)

    def getYoutubeVersion(self):
        self.logger.info('getYoutubeVersion')
        cmds = ['powershell.exe', '.\yver.ps1', ]
        self.logger.info(cmds)
        timeStamp = time.strftime("%H%M%S")
        stdoutName = "output_"+timeStamp+".log"
        stderrName = "error_"+timeStamp+".log"
        self.logger.info("Filenames {} {}".format(stdoutName, stderrName))
        stdoutFh = open(stdoutName, 'wt')
        stderrFh = open(stderrName, 'wt')
        rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
        self.logger.info("RC = {}".format(rc.returncode))
        stdoutFh.close()
        stderrFh.close()
        allOutLines = open(stdoutName, 'rt').readlines()
        allErrLines = open(stderrName, 'rt').readlines()
        lastLine = ''
        for ao in allOutLines:
            lastLine = ao.rstrip()
            self.logger.info('getYoutubeVersion(): {}'.format(lastLine))
        for ae in allErrLines:
            self.logger.error('getYoutubeVersion(): {}'.format(ae.rstrip()))
        if rc.returncode == 0:
            self.globalYtver = lastLine
            print('Version:{}'.format(self.globalYtver))
        # return self.globalYtver

    def updateYoutube(self):
        self.logger.info('updateYoutube')
        cmds = ["python "+_YOUTUBE_PATH+" -U",]
        self.logger.info(cmds)
        timeStamp = time.strftime("%H%M%S")
        stdoutName = "output_"+timeStamp+".log"
        stderrName = "error_"+timeStamp+".log"
        self.logger.info("Filenames {} {}".format(stdoutName, stderrName))
        stdoutFh = open(stdoutName, 'wt')
        stderrFh = open(stderrName, 'wt')
        rc = subprocess.run(cmds, stdout=stdoutFh, stderr=stderrFh, shell=True)
        self.logger.info("RC = {}".format(rc.returncode))
        stdoutFh.close()
        stderrFh.close()
        allOutLines = open(stdoutName, 'rt').readlines()
        allErrLines = open(stderrName, 'rt').readlines()
        for ao in allOutLines:
            self.logger.info('updateYoutube(): {}'.format(ao.rstrip()))
        for ae in allErrLines:
            self.logger.error('updateYoutube(): {}'.format(ae.rstrip()))
        self.globalYtver = self.getYoutubeVersion()
        
    def download(self, url):
        self.logger.info('Download {}'.format(url))

if __name__ == "__main__":
    ytke = Youtube_DL_TKE()
    args = []
    try:
        args = sys.argv[1]
    except:
        pass
    if len(args):
        ytke.download(args)
    else:
        sys.stderr.writelines('no url to download\n')
    
