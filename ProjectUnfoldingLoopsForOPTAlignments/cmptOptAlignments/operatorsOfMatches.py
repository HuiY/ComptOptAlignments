from execspace import defsOfModel
from patEvtLog import defsOfLog

from enum import Enum

class ResCtrTree:
    def __init__(self):
        self.succeed=False
        self.numBoth=0
        self.numDev=0
        self.numCountTree=0

class TypeOfMatch(Enum):
    NotMatched = 1
    BothCorrect = 2
    FTaskCEntry = 3
    CTaskFEntry=4
    BothFake=5

class AMatch:
    def __init__(self):
        self.ID=''
        self.GENID='Root'
        self.PreActivities=[]
        self.Cost=0
        self.CostDevs=0   # 12.16
        self.NumDevs=0
        self.NumBoth=0
        self.NumMvLog=0
        self.Type=TypeOfMatch.NotMatched
        self.Task=defsOfModel.ExecutedTask()
        self.Entry=defsOfLog.AuditTrailEntry()
        #self.TraceID=''
        self.GScore=0
        self.HScore=0
        self.LTrace=''
        self.MTrace=''

def nodesPlace(childNode, subOPEN, subCLOSED, subCoorSys,fathNode):
    if subCLOSED.__contains__(childNode.ID):  # ?
        if childNode.Cost == subCLOSED[childNode.ID].Cost:
            subCLOSED[childNode.ID].PreActivities.append(fathNode.ID)
    elif subOPEN.__contains__(childNode.ID):  # ?
        if childNode.Cost < subOPEN[childNode.ID].Cost:
            subOPEN.pop(childNode.ID)
            childNode.PreActivities.append(fathNode.ID)
            subOPEN[childNode.ID] = childNode
        elif childNode.Cost == subOPEN[childNode.ID].Cost:
            if fathNode.ID not in subOPEN[childNode.ID].PreActivities:
                subOPEN[childNode.ID].PreActivities.append(fathNode.ID)
    else:
        # link it to fatherMatch
        childNode.PreActivities.append(fathNode.ID)
        subCoorSys[childNode.ID] = childNode
        # add it to OPEN
        subOPEN[childNode.ID] = childNode

def findLsLowCost(lsOPEN):
    lsLow=[]
    lowestCost=sorted(lsOPEN.values(),key= lambda x:x.Cost)[0].Cost
    for nodeID in lsOPEN:
        if lsOPEN[nodeID].Cost==lowestCost:
            lsLow.append(lsOPEN[nodeID])
    return lsLow

def findlsOptAlignment(endAmatch, dicCLOSED,dicOPEN):
    dicOptAligns={}
    dicOptAligns[1]=[]
    dicOptAligns[1].append(endAmatch)
    #ls.insert(0,endAmatch)
    #dicOptAligns[1]=ls
    #dicOptAligns[1].append(endAmatch)
    lsOptAligns=list(dicOptAligns)
    count=0
    while lsOptAligns.__len__() > 0:
        if count>5:
            break
        lsOptAligns.sort()
        curId=lsOptAligns.pop(0)
        tempAmatch=dicOptAligns[curId][len(dicOptAligns[curId])-1]#the last item in dicOptAligns[curId]
        lsPreAMatches = tempAmatch.PreActivities#PreActivities
        if len(lsPreAMatches)==0:
            count = count + 1
            continue
        else:
            lsOptAligns.append(curId)
            temList=[]
            if len(lsPreAMatches)>1:
                for item in dicOptAligns[curId]:
                    temList.append(item)
            i=0
            for one in lsPreAMatches:
                #get the GenID of one
                split0=one.split('_')
                noTaskOne=one[:-len(split0[len(split0)-1])-1]
                split1=noTaskOne.split('M')
                genOfOne='Root_'+noTaskOne[len(split1[0])+1:]
                if genOfOne=='Root_':
                    genOfOne='Root'
                if i==0:
                    if one in dicCLOSED[genOfOne]:
                        tempAmatch = dicCLOSED[genOfOne][one]
                        dicOptAligns[curId].append(tempAmatch)
                    elif one in dicOPEN[genOfOne]:
                        tempAmatch = dicOPEN[genOfOne][one]
                        dicOptAligns[curId].append(tempAmatch)
                    i=i+1
                else:
                    newID=len(dicOptAligns)+1
                    lsOptAligns.append(newID)
                    dicOptAligns[newID] = []  # copy an existing list into a new list, and put it in dicOptAligns
                    dicOptAligns[newID] = temList
                    if one in dicCLOSED[genOfOne]:
                        dicOptAligns[newID].append(dicCLOSED[genOfOne][one])
                    elif one in dicOPEN[genOfOne]:
                        tempAmatch = dicOPEN[genOfOne][one]
                        dicOptAligns[newID].append(tempAmatch)
    k=1
    dicfinalOptAligns={}
    while k<5 and k<dicOptAligns.__len__():
        dicfinalOptAligns[k]=[]
        dicfinalOptAligns[k]=dicOptAligns[k]
        k=k+1
    return dicfinalOptAligns

'''
def nodesExpansion(fathMatch,entry,lsTasks):
    lsNodes=[]
    #entry is empty, namely EndOfTrace
   # lsNloop=[]
   #lsloop=[]
    if entry.ID=='NoEntry':
        for task in lsTasks:
            lsNodes.append(CTaskFEntry(fathMatch,object,task))
    elif lsTasks.__len__()==0:#lsTask is empty, namely EndOfModel
        FTaskCEntry(fathMatch,entry,object)
    else:
        flagBoth=False
        for task in lsTasks:
            if task.Elment.name==entry.Name:
                flagBoth=True
                lsNodes.append(BothMatch(fathMatch, entry,task))
            else:
                lsNodes.append(CTaskFEntry(fathMatch, object, task))#在模型移动节点更新
        if flagBoth is False:
            lsNodes.append(FTaskCEntry(fathMatch, entry,object))#在日志移动节点更新
    for Node in lsNodes:
        if Node.Task.Floor > fathMatch.Task.Floor:
            lsNloop.append(Node)
        else:
            lsloop.append(Node)

    return lsNodes
'''