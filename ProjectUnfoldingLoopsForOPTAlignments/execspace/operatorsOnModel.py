#coding=utf-8
from execspace.defsOfModel import TypeOfElement
def EndOfModel(task,exespace):
    flagEnd=False
    #task is empty, move in model is not made yet
    if task.ID=='IniTask':
        flagEnd=False
    elif task.NonloopNxtTasks.__len__() == 0:
        flagEnd = True
    '''if task.NonloopNxtTasks.__len__()==1:
        if exespace[task.NonloopNxtTasks[0]].Elment.name=='EndEvent':
            flagEnd=True'''
    return flagEnd

def findCurrentTasks(fatherMatch,execspace):#only when fatherMatch.Task is not the last one
    faMatchTaskID=''
    lsTasks=[]
    #when fatherMatch is the first AMatch
    if fatherMatch.Task.ID=='IniTask':
        faMatchTaskID=sorted(execspace.values(),key=lambda x:x.PreExcTaskIDlist.__len__())[0].ID
    #when fatherMatch.Task is not the first nor the last
    else:
        faMatchTaskID=fatherMatch.Task.ID
    for i in execspace[faMatchTaskID].NonloopNxtTasks:
        lsTasks.append(execspace[i])
    for i in execspace[faMatchTaskID].LoopNxtTasks:
        lsTasks.append(execspace[i])
    return lsTasks

def findNormTasks(task,execspace):
    lsNonLoopTasks = []
    flagEndModel = EndOfModel(task, execspace)
    if flagEndModel is True:
        lsNonLoopTasks = []  # there is no tasks to be aligned
    else:
        # when fatherMatch is the first AMatch
        if task.ID == 'IniTask':
            faMatchTaskID = sorted(execspace.values(), key=lambda x: x.PreExcTaskIDlist.__len__())[0].ID
        # when fatherMatch.Task is not the first nor the last
        else:
            faMatchTaskID = task.ID
        for i in execspace[faMatchTaskID].NonloopNxtTasks:
            lsNonLoopTasks.append(execspace[i])
    return lsNonLoopTasks