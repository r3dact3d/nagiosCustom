#!/usr/bin/env python
import os, sys

# Set logfile and keywords to search and compare
logFile = '/usr/local/jboss/server/expediadc/log/server.log'
start = 'Starting to process ARI records'
end = 'Done processing ARI records'

# Search for keywords in logs and make a list
def logGrep(logFile, start, end):
    openLog = open(logFile, 'r')
    starts = []
    ends = []
    for line in openLog:
        if start in line:
            line = line.strip('\n')
            starts.append(line)
        elif end in line:
            line = line.strip('\n')
            ends.append(line)

# Format the last line of each list for comparisions
    if starts and ends:
        start = starts[-1].split(' ', 2)[1]
        startTimeFull = start.split(',', 1)[0]
        end = ends[-1].split(' ', 2)[1]
        endTimeFull = end.split(',', 1)[0]
        s = ""
        intStart = s.join(startTimeFull.split(':', 3))
        intEnd = s.join(endTimeFull.split(':', 3))
        diff = (int(intStart) - int(intEnd))
        print diff

# Start logic by comparing timestamps of starts and finishes of ARI        
        if intStart < intEnd:
            print 'Expedia ARI Completed: ' + endTimeFull
            sys.exit(0)
        elif intStart == intEnd:
            print 'Expedia ARI Completed: ' + endTimeFull
            sys.exit(0)
        elif intStart > intEnd:
            if diff > 3000:
                print 'Expedia ARI has started, but not completed since: ' + startTimeFull
                sys.exit(2)
            else:
                print 'Expedia ARI has started, but not completed in short time since ' + startTimeFull
        else:
            print 'Something maybe wrong, can NOT find Expedia ARI start or end!'
            sys.exit(2)



logGrep(logFile, start, end)

