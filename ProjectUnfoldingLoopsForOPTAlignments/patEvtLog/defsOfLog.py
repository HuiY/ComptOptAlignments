#coding=utf-8
__all__ = ['AuditTrailEntry']
class AuditTrailEntry:
    def __init__(self):
        self.Type =''
        self.OccurTime =''
        self.SubType =''
        self.Name =''
        self.OrigName = ''
        self.Result =''
        self.State = ''
        self.ID =''
        self.StartTime =''
        self.EndTime =''
        #print("a new Event")
class EventTrace:
    def __init__(self):
        self.TrID=''
        self.LOS=0
        self.Trace=[]  #数据类型为：List<AuditTrailEntry>
        self.StartDate=''
        self.EndDate=''
class LogParseResult:
     def __init__(self):
           self.success = True
           self.excepe = Exception()