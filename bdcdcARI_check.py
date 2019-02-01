#!/usr/bin/env python
import os
import time
import sys

logName = "server.log"
log = "/usr/local/jboss/server/bdcdc/log/%s" % logName

def logTime(log, logName):
    if os.path.exists(log):
        eTime = os.path.getmtime(log)
        mTime = time.ctime(eTime)
    else:
        print "%s not created yet today - Please Check" % logName
        sys.exit(2)
    nowTime = time.time()
    diffTime = nowTime - eTime
    if diffTime > 2500:
        print "%s not being updated since %s- Please Check" % (logName, mTime)
        sys.exit(2)

def logGrep(log):
    pat = "CheckLastActivityCacheTask"
    badPat = "ERROR"
    goodPat = "AvailabilityRatesModule"
    openLog = open(log, 'r')
    for line in openLog:
        if pat in line and badPat in line:
            badMatch = line
        if goodPat in line:
            goodMatch = line
    print badMatch
    print goodMatch

logTime(log, logName)
logGrep(log)
