#!/usr/bin/env python

import logging
import logging.config

logConfigFile='pylog.conf'
#logging.config.fileConfig(logConfigFile)
logging.config.fileConfig('log.ini')
moduleName = 'X'
logger = logging.getLogger(moduleName)
for i in range(5):
	logger.info('value = '+str(i))
#logger = logging.getLogger('mylog')
logger.info('Level info')
logger.debug('Level debug')
logger.warning('Level warn')
logger.error('Level error')
logger.fatal('Level fatal')
