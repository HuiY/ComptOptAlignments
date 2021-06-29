# coding=utf-8
from cmptOptAlignments.operatorsOfMatches import TypeOfMatch, AMatch
import math

def dFirstMatch(LPart, MPart):
    fistMatch=AMatch()
    fistMatch.ID='Root'
    fistMatch.Task.ID='IniTask'
    fistMatch.Task.Elment.name='IniTask'
    fistMatch.Entry.ID='IniEntry'
    fistMatch.Entry.Name='IniEntry'
    fistMatch.HScore=0
    fistMatch.Cost=0
    fistMatch.CostDevs=0  # 12.16
    fistMatch.NumMvLog = 0
    fistMatch.LTrace='L'
    fistMatch.MTrace='M'
    return fistMatch

def dFTaskCEntry(genID,faMatch,entry,object): #事件日志上移动
    cMatch=AMatch()

    cMatch.NumDevs = faMatch.NumDevs + 1
    cMatch.NumBoth = faMatch.NumBoth
    cMatch.NumMvLog = faMatch.NumMvLog + 1
    deltaCost = 100
    cMatch.CostDevs=faMatch.CostDevs+deltaCost # 12.16
    cMatch.Cost = faMatch.Cost + deltaCost
    cMatch.Type = TypeOfMatch.FTaskCEntry
    cMatch.Entry = entry
    cMatch.Task = faMatch.Task
    cMatch.LTrace = faMatch.LTrace+entry.ID
    cMatch.MTrace = faMatch.MTrace

    cMatch.ID = 'L' + entry.ID+'M' + genID[5:] +'_' + faMatch.Task.ID
    return cMatch

def dCTaskFEntry(genID,faMatch,object,task): #模型上移动
    cMatch=AMatch()
    deltaFlr = task.Floor - faMatch.Task.Floor  # when no loop, deltaFlr is always greater than 0
    if task.Floor > faMatch.Task.Floor:
        deltaCost = math.fabs(deltaFlr) * 100
    else:
        deltaCost =100

    cMatch.Cost = faMatch.Cost + deltaCost
    cMatch.CostDevs = faMatch.CostDevs + deltaCost
    cMatch.GENID = faMatch.GENID
    cMatch.NumDevs = faMatch.NumDevs + 1
    cMatch.NumBoth = faMatch.NumBoth
    cMatch.NumMvLog = faMatch.NumMvLog
    cMatch.Type = TypeOfMatch.CTaskFEntry
    cMatch.Entry = faMatch.Entry
    cMatch.Task = task
    cMatch.LTrace = faMatch.LTrace
    cMatch.MTrace = faMatch.MTrace + task.ID
    cMatch.ID ='L' + faMatch.Entry.ID+'M'+ genID[5:] +'_'+ task.ID
    return cMatch

def dBothMatch(genID,faMatch,entry,task):
    cMatch=AMatch()
    deltaFlr=task.Floor-faMatch.Task.Floor#when no loop, deltaFlr is always greater than 0
    cMatch.NumDevs = faMatch.NumDevs
    cMatch.NumBoth = faMatch.NumBoth + 1
    cMatch.NumMvLog = faMatch.NumMvLog
    if task.Floor > faMatch.Task.Floor:
        deltaCost=math.sqrt(deltaFlr*deltaFlr+1)*100
        #newID = task.ID
    else:
        deltaCost = math.sqrt(1 + 1) * 100
        #newID = faMatch.Task.ID + task.ID
    cMatch.GENID = faMatch.GENID
    cMatch.CostDevs=faMatch.CostDevs+deltaCost # 12.16
    cMatch.Cost=faMatch.Cost+deltaCost
    cMatch.NumBoth = faMatch.NumBoth + 1
    cMatch.Type=TypeOfMatch.BothCorrect
    cMatch.Entry=entry
    cMatch.Task=task
    cMatch.LTrace=faMatch.LTrace+entry.ID
    cMatch.MTrace=faMatch.MTrace+task.ID

    cMatch.ID='L' + entry.ID + 'M' + genID[5:] +'_'+task.ID
    return cMatch

#not use any more, June 7, 2021
def dijkstraNodesExpansion(fathMatch,entry,lsTasks):
    lsNodes=[]
    #entry is empty, namely EndOfTrace
    if entry.ID=='NoEntry':
        for task in lsTasks:
            lsNodes.append(dCTaskFEntry(fathMatch,object,task))
    elif lsTasks.__len__()==0:#lsTask is empty, namely EndOfModel
        dFTaskCEntry(fathMatch,entry,object)
    else:
        flagBoth = False
        for task in lsTasks:
            if task.Floor > fathMatch.Task.Floor:   #Root展开正常情况
                if task.Elment.name == entry.Name:  ##12.22加
                    flagBoth = True
                    lsNodes.append(dBothMatch(fathMatch, entry, task))
                else:
                    lsNodes.append(dCTaskFEntry(fathMatch, object, task))  # 在模型移动节点更新
            elif task.Floor == fathMatch.Task.Floor:    #自循环情况
                newAMatch=AMatch()
                if task.Elment.name == entry.Name:  ##12.22加
                    flagBoth = True
                    newAMatch=dBothMatch(fathMatch, entry, task)
                else:
                    newAMatch = dCTaskFEntry(fathMatch, object, task)
                newAMatch.GENID=fathMatch.GENID+'_0'+task.ID
               # newAMatch.Task.ID=fathMatch.Task.ID+task.ID
                lsNodes.append(newAMatch)
            else:                               #跳回循环
                newAMatch = AMatch()
                moveFloor=abs(task.Floor-fathMatch.Task.Floor)
                if task.Elment.name == entry.Name :  ##12.22加
                    flagBoth = True
                    newAMatch = dBothMatch(fathMatch, entry, task)
                else:
                    newAMatch = dCTaskFEntry(fathMatch, object, task)
                newAMatch.GENID = fathMatch.GENID + '_'+str(moveFloor) + fathMatch.Task.ID
              #  newAMatch.Task.ID = fathMatch.Task.ID + task.ID
                lsNodes.append(newAMatch)
        if flagBoth is False:
            lsNodes.append(dFTaskCEntry(fathMatch, entry,object)) #在日志移动节点更新
    return lsNodes