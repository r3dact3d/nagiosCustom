#!/usr/bin/env python
import os
import time
import sys

logName = "server.log"
log = '/usr/local/jboss/server/bdcdc/log/%s' % logName

def logTime(log, logName):
    if(os.path.exists(log)):
        logTime = os.path.getmtime(log)
        prettyTime = time.ctime(logTime)
        nowTime = time.time()
        diffTime = nowTime - logTime
        if(diffTime > 2500):
            print('%s not being updated since %s- Please Check') % (logName, prettyTime)
            sys.exit(2)
        else:
            logGrep(log)
    else:
        print("%s not created yet today - Please Check") % logName
        sys.exit(2)

def writeCarry(lineWrite):
    wc = open('/tmp/bdcdcLast.txt', 'w')
    wc.write(lineWrite)
    wc.close()

def readCarry():
    rc = open('/tmp/bdcdcLast.txt', 'r')
    return(rc.read())

def logic(outLine):
    outLines = outLine.split()
    outDate, outTime = outLines[0][-2:], outLines[1].split(',',1)[0].split(':', 3)[0]
    nowDate, nowTime = time.localtime()[2], time.localtime()[3]
    print('[=] Date of last ARI is %s') % outDate
    print('[=] Current date is %s') % nowDate
    print('[=] Time of last ARI is %s') % outTime
    print('[=] Current time is %s') % nowTime
    diff = int(nowTime) - int(outTime)
    if(int(nowDate) == int(outDate)):
        if(diff > 1) and (diff < 3):
            print('BookingDC ARI WARNING not run for over an hour')
            sys.exit(1)
        elif(diff > 3):
            print('BookingDC ARI CRITICAL not run for over 3 hours')
            sys.exit(2)
        else:
            print('BookingDC ARI is running')
            sys.exit(0)
    else:
        diff = int(outTime) - int(nowTime)
        if(diff < 19):
            print('BookingDC ARI CRITICAL not run for over 3 hours')
            sys.exit(2)

def logGrep(log):
    outARI = 'com.accor.bdcdc.bdcavailabilityratesmodule.impl.BookingdotcomAvailabilityRatesModule'
    sanity = 'java'
    openLog = open(log, 'r')
    outLine = ''
    for line in openLog:
        if(outARI in line) and (sanity not in line):
            outLine = line
    if(outLine != ''):
        writeCarry(outLine)
        logic(outLine)
    elif(outLine == ''):
        outLine = readCarry()
        logic(outLine)
    else:
        print('Something must be wrong, logic can not complete')

logTime(log, logName)
                      
