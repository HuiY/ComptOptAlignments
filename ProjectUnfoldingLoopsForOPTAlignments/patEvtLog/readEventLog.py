# coding=utf-8
import datetime
from xml.dom.minidom import parse
import xml.dom.minidom
from patEvtLog import defsOfLog
#_traces=[]   # 全局变量，存储的类型为：list<EventTrace>_traces
def readLogFormatXmlWeaning(filePath):
   r=defsOfLog.LogParseResult()   #存储读取结果
   #filePath="ParsedLog.xml"
   DOMTree = xml.dom.minidom.parse(filePath)
   doc= DOMTree.documentElement
   processInstanceList = doc.getElementsByTagName("ProcessInstance") #获取ProcessInstance节点
   traceID = 0
   keyID = ""
   patKeys=[]   #先定义一个局部变量
   dicLog={}
   for processInstance in processInstanceList:
        if (processInstance.getAttribute("KeyID") != ""):
            keyID = processInstance.getAttribute("KeyID")
            patKeys.append(keyID)#add to the list one by one
        tempTrace = defsOfLog.EventTrace( )
        tempTrace.TrID = keyID
        auditList = processInstance.getElementsByTagName("AuditTrailEntry")
        ID = 0
        f_startTime=datetime.datetime.max #初始化时间最大值：9999-12-31 23:59:59.999999
        f_endTime=datetime.datetime.min #初始化时间最小值：0001-01-01 00:00:00
        for audit in auditList:
            sglNode=defsOfLog.AuditTrailEntry()
            sglNode.Name=audit.getElementsByTagName('WorkflowModelElement')[0].childNodes[0].data.replace("-", "").replace(" ", "_") #能读取WorkflowModelElement里面的数据,变为Take_blood_tes
            if (audit.getAttribute("OccurTime")!= "" ):
                datatimestr = audit.getAttribute("OccurTime")
                tt=datatimestr.replace('T', ' ')
                sglNode.OccurTime=datetime.datetime.strptime(tt, '%Y/%m/%d %H:%M:%S')
            reslt= (sglNode.OccurTime>f_endTime)
            if reslt ==True:
                f_endTime = sglNode.OccurTime
            reslt=(sglNode.OccurTime>f_startTime)
            if reslt==False:
                f_startTime= sglNode.OccurTime
            sglNode.ID = str(ID)
            tempTrace.Trace.append(sglNode)
            ID =ID+1
        z=(f_endTime - f_startTime).total_seconds()
        m, s = divmod(z, 60)
        h, m = divmod(m, 60)
        tempTrace.LOS = h
        tempTrace.StartDate = f_startTime
        tempTrace.EndDate = f_endTime
        #_traces.append(tempTrace) #_traces是全局变量，可以被其他函数调用。
        dicLog[keyID]=tempTrace
   if len(dicLog) == 0:
        r.success = False
   return r,patKeys,dicLog#return r,patKeys

def readLogFormatXes(filePath):
   r=defsOfLog.LogParseResult()   #存储读取结果
   #filePath="ParsedLog.xml"
   DOMTree = xml.dom.minidom.parse(filePath)
   doc= DOMTree.documentElement
   processInstanceList = doc.getElementsByTagName("trace") #获取ProcessInstance节点
   traceID = 0
   keyID = ""
   patKeys=[]   #先定义一个局部变量
   dicLog={}
   for processInstance in processInstanceList:
       tempTrace = defsOfLog.EventTrace()
       ID = 0
       f_startTime = datetime.datetime.max  # 初始化时间最大值：9999-12-31 23:59:59.999999
       f_endTime = datetime.datetime.min  # 初始化时间最小值：0001-01-01 00:00:00
       for traceInfo in processInstance.childNodes:
           if traceInfo.localName=="string" and traceInfo.getAttribute("key")=="concept:name":
               keyID = traceInfo.getAttribute("value")
               tempTrace.TrID = keyID
               patKeys.append(keyID)
           if traceInfo.localName=="event":
               sglNode = defsOfLog.AuditTrailEntry()
               for evtInfo in traceInfo.childNodes:
                   if evtInfo.localName=="string" and evtInfo.getAttribute("key")=="concept:name":
                       sglNode.Name = evtInfo.getAttribute("value").replace("-", "").replace(" ", "_")
                   if evtInfo.localName == "date" and evtInfo.getAttribute("key") == "time:timestamp":
                       datatimestr = evtInfo.getAttribute("value")
                       tt = datatimestr[0:datatimestr.__len__()-10].replace('T', ' ').replace('-','/')
                       sglNode.OccurTime = datetime.datetime.strptime(tt, '%Y/%m/%d %H:%M:%S')
                       reslt = (sglNode.OccurTime > f_endTime)
                       if reslt == True:
                           f_endTime = sglNode.OccurTime
                       reslt = (sglNode.OccurTime > f_startTime)
                       if reslt == False:
                           f_startTime = sglNode.OccurTime
                       sglNode.ID = str(ID)
                       tempTrace.Trace.append(sglNode)
                       ID = ID + 1
       z = (f_endTime - f_startTime).total_seconds()
       m, s = divmod(z, 60)
       h, m = divmod(m, 60)
       tempTrace.LOS = h
       tempTrace.StartDate = f_startTime
       tempTrace.EndDate = f_endTime
       # _traces.append(tempTrace) #_traces是全局变量，可以被其他函数调用。
       dicLog[keyID] = tempTrace

   if len(dicLog) == 0:
        r.success = False
   return r,patKeys,dicLog#return r,patKeys

def readLogFormatXmlWeaningdevs(filePath):
    r = defsOfLog.LogParseResult()  # 存储读取结果
    # filePath="ParsedLog.xml"
    DOMTree = xml.dom.minidom.parse(filePath)
    doc = DOMTree.documentElement
    processInstanceList = doc.getElementsByTagName("ProcessInstance")  # 获取ProcessInstance节点
    traceID = 0
    keyID = ""
    patKeys = []  # 先定义一个局部变量
    dicLog = {}
    for processInstance in processInstanceList:
        if (processInstance.getAttribute("KeyID") != ""):
            keyID = processInstance.getAttribute("KeyID")
            patKeys.append(keyID)  # add to the list one by one
        tempTrace = defsOfLog.EventTrace()
        tempTrace.TrID = keyID
        auditList = processInstance.getElementsByTagName("AuditTrailEntry")
        ID = 0
        f_startTime = datetime.datetime.max  # 初始化时间最大值：9999-12-31 23:59:59.999999
        f_endTime = datetime.datetime.min  # 初始化时间最小值：0001-01-01 00:00:00
        for audit in auditList:
            sglNode = defsOfLog.AuditTrailEntry()
            sglNode.Name = audit.getElementsByTagName('WorkflowModelElement')[0].childNodes[0].data.replace("-","").replace(" ", "_")  # 能读取WorkflowModelElement里面的数据,变为Take_blood_tes
            sglNode.ID = str(ID)
            tempTrace.Trace.append(sglNode)
            ID = ID + 1
        dicLog[keyID] = tempTrace
    if len(dicLog) == 0:
        r.success = False
    return r, patKeys, dicLog  # return r,patKeys

if __name__ == '__main__':
    result,patKeysum,dicLog=readLogFormatXmlWeaning()
    '''for index in range(len(_traces)):
        print('The TrID of EventTrace is:',_traces[index].TrID,end="  ")
        print('The StartDate is:',_traces[index].StartDate,end="  ")
        print('The EndDate is:',_traces[index].EndDate,end="  ")
        print('The LOS is:',_traces[index].LOS)
        print('The EventTrace is:')
        lenth=len(_traces[index].Trace)
        for x in range(lenth):
            print((_traces[index].Trace)[x].Name)'''
