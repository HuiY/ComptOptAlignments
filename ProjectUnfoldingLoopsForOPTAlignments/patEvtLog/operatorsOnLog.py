#coding=utf-8
from patEvtLog.defsOfLog import AuditTrailEntry
def EndOfTrace(entry,trace):
    flagEnd = False
    #if entry not is empty
    if entry.ID=='NoEntry':
        flagEnd=True
        return flagEnd
    if entry in trace:
        if trace.index(entry)==trace.__len__()-1:
            flagEnd=True
    #else, entry is empty (no move in log is made yet)
    else:
        flagEnd=False
    return flagEnd

def findCurrentEntry(fatherMatch,evtrace):#only when fatherMatch.Event is not the last one
    flagEndTrace = EndOfTrace(fatherMatch.Entry, evtrace)
    if flagEndTrace is True:
        myEntry = AuditTrailEntry()  # there is no entry to be aligned
        myEntry.ID = 'NoEntry'
    else:
        myEntry=AuditTrailEntry()
        #fatherMatch is the first Amatch or it is CTaskFEntry
        if fatherMatch.Entry.ID=='IniEntry':
            myEntry=evtrace[0]
        else:
            if fatherMatch.Entry in evtrace:
                myEntry = AuditTrailEntry()  # there is no entry to be aligned
                myEntry.ID = 'NoEntry'
            faIndex=evtrace.index(fatherMatch.Entry)
            myEntry=evtrace[faIndex+1]
    return myEntry
