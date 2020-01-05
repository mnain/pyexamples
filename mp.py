#!/usr/bin/env python

import time
import sys
import multiprocessing

def logProc(name,logFileName):
	print('LogProc {} starting...'.format(name))
	fh = open(logFileName, 'wt')
	counter = 0
	while counter < 10:
		timeStamp = time.strftime('%Y-%m-%d %H:%M:%S')
		fh.writelines(timeStamp+' '+name+' {}\n'.format(counter))
		print('Value of counter {} {}'.format(counter,name))
		time.sleep(5)
		counter = counter + 1
	fh.close()

if __name__ == "__main__":
	procs = []
	procDict = { 'First' : 'test1.log', 'Second' : 'test2.log'}
	for pd in procDict.keys():
		pr = multiprocessing.Process(target=logProc, args=(pd,procDict[pd],))
		procs.append(pr)
		pr.start()
	for pr in procs:
		pr.join()
		
