#!/usr/bin/env python
import os
import datetime
import time
import sys

# Set log to monitor and location of log then create function to open and read log
logName = "bdcdc.log"
log = "/usr/local/resin/log/%s" % logName
def getLog(log):
    openLog = open(log, 'r')
    return(openLog)

# Check if log exists (some are rotated daily or on restart
# Check if log is being updated
def logTime(log, logName):
    if(os.path.exists(log)):
        eTime = os.path.getmtime(log)
        mTime = time.ctime(eTime)
    else:
        print("%s not created yet today - Please Check") % logName
        sys.exit(2)
    nowTime = time.time()
    diffTime = int(nowTime) - int(eTime)
    if diffTime > '3500':
        print("%s not being updated since %s- Please Check") % (logName, mTime)
        sys.exit(2)

# Check if InvocationTargetExceptions are being generated
def exceptionCheck(log):
    error = "InvocationTargetException occurred"
    errorException = 'XmlException'
    count = 0
    errorCount = 0
    exceptionCount = 0
    for line in getLog(log):
        if error in line:
            errorCount = errorCount + 1
        elif errorException in line:
            exceptionCount = exceptionCount + 1
    count = errorCount - exceptionCount
    dateTime(count)

# Format todays date and time into a string that can be compared to timestamp in log
def dateTime(count):
    dateTime = datetime.datetime.now()
    #checkTime = str(dateTime).split(' ',1)[1].split(':',1)[0]
    checkTimeSplit = str(dateTime).split(' ',1)[1].split('.')[0].split(':')
    del(checkTimeSplit[2])
    s = ''
    checkTime = s.join(checkTimeSplit)
    checkTime = int(checkTime) - 15
    pullGrep(count, log, checkTime)

# Create a list of PullTasks found in current log
def pullGrep(count, log, checkTime):
    pullTask = "PullTask"
    init = "initialization"
    pulls = []
    for line in getLog(log):
        if pullTask in line and init not in line:
            line = line.strip('\n')
            pulls.append(line)
# If there are PullTasks found return them for more checks
# If there are NO PullTasks found yet, check against current time, and
# if the current time is greater than 1am then report no pulltasks found.
    if pulls:
        print('[+] Running pullData')
        pullData(count, pulls, checkTime)
    else:
        if (checkTime > 1):
            print("PullTasks have not run yet today!")
            sys.exit(2)

def pullData(count, pulls, checkTime):
    p1 = "InvocationTargetException occurred"
    pull = pulls[-1].split(' ',2)
    pullTime = pull[1]
    pullTime = pullTime.split(':')
    del(pullTime[2])
    s = ''
    pullTime = s.join(pullTime)
    pullTime = int(pullTime)
    if(pullTime < checkTime):
        print("PullTasks not running!")
        sys.exit(2)
    elif(count > 25):
        print("%s logged %s times") % (p1, count)
        sys.exit(2)
    elif(count < 25) and (count > 15):
        print("%s logged %s times") % (p1, count)
        sys.exit(1)
    else:
        print("Logs Clean")
        sys.exit(0)

logTime(log, logName)
exceptionCheck(log)
