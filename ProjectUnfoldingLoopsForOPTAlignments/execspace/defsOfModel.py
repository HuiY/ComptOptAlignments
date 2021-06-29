#coding=utf-8
from enum import Enum

class TypeOfElement(Enum): #派生，即Enum是父类
    Empty = 1
    StartEvent = 2
    Task = 3
    GateWay=4
    EndEvent=5
    Sequence=6
    LoopTask=7
    BlockActivity=8
    IntermediateThrowEvent=9
    IntermediateCatchEvent=10

class Elment:
    def __init__(self):
        self.ID=''
        self.name=''
        self.state =''
        self.type=TypeOfElement.Empty

class ExecutedTask:
    def __init__(self):
        self.ID=''
        self.Elment=Elment()
        self.PreExcTaskIDlist=[]
        #self.NextExcTaskIDlist=[]
        self.LoopNxtTasks=[]
        self.NonloopNxtTasks=[]#firstly,all the next tasks are placed into nonloop, then move some into loop
        self.loop=0
        self.Floor=0

class LoopStruct:
    def __init__(self,startFlr,endFlr):
        self.InitFlr=startFlr
        self.TargFlr=endFlr

def InTypeEnums(searchObj):
    typeEnum=TypeOfElement.Empty
    if searchObj=='StartEvent':
        typeEnum=typeEnum.StartEvent
    if searchObj=='EndEvent':
        typeEnum=typeEnum.EndEvent
    if searchObj == 'Task':
        typeEnum = typeEnum.Task
    if searchObj == 'Gateway':
        typeEnum = typeEnum.GateWay
    if searchObj=='Sequence':
        typeEnum=typeEnum.Sequence
    if searchObj=='LoopTask':
        typeEnum=typeEnum.LoopTask
    if searchObj=='BlockActivity':
        typeEnum=typeEnum.BlockActivity
    if searchObj=='IntermidiateThrow':
        typeEnum=typeEnum.IntermediateThrowEvent
    if searchObj=='IntermediateCatch':
        typeEnum=typeEnum.IntermediateCatchEvent
    return typeEnum