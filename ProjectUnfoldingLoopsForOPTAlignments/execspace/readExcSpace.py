#coding=utf-8
import re, os
from execspace import assignFloors
from execspace.defsOfModel import LoopStruct
from execspace import defsOfModel
filePath = "toSpecify.grs"
#TypeOfElement0 = Enum("TypeOfElement",('Empty','StartEvent','Task','GateWay','EndEvent','Sequence','LoopTask','BlockActivity','IntermediateThrowEvent','IntermediateCatchEvent'))


# 匹配ID规则
#str_ID_rex = r'(?<=ExecutedTask[(]\$=\").\S{3}'
str_ID_rex = r'(?<=ExecutedTask[(]\$=[\"]).*(?=[\"],name)'
# 匹配name规则
str_name_rex=r'(?<=name=\").*(?=[\"],state)'
# 匹配state规则
str_state_rex=r'(?<=state=\").*(?=[\"],type)'
# 匹配type规则
str_type_rex=r'(?<=type=\").*(?=[\"])'
#匹配边的源节点ID
str_source_rex=r'(?<=@[(]\").*(?=\"[)]-:ExcRelation)'
#匹配边的目标节点ID
str_goal_rex=r'(?<=->@[(]\").*(?=\"[)])'

def prunEndEvents(dicExcspace):
    for nodeid in dicExcspace:
        if dicExcspace[nodeid].Elment.name=='EndEvent':
            for preid in dicExcspace[nodeid].PreExcTaskIDlist:
                dicExcspace[preid].NonloopNxtTasks.remove(nodeid)
    i=0
    while i< len(dicExcspace):
        nodeid=list(dicExcspace.keys())[i]
        if dicExcspace[nodeid].Elment.name == 'EndEvent':
            dicExcspace.pop(nodeid)
            i=i-1
        i=i+1
def readExecutionSpace(path):
    if not os.path.isfile(path):
        return "Path is not file !"
    # 初始化变量用于保存所有匹配的字典
    dicExecutedSpace = {}
    #match_ID=[]
    # 创建匹配ID正则表达式对象
    rex_ID_obj = re.compile(str_ID_rex)
    #创建匹配name正则表达式对象
    rex_name_obj = re.compile(str_name_rex)
    # 创建匹配state正则表达式对象
    rex_state_obj = re.compile(str_state_rex)
    # 创建匹配type正则表达式对象
    rex_type_obj = re.compile(str_type_rex)
    # 创建匹配source正则表达式对象
    rex_source_obj = re.compile(str_source_rex)
    ## 创建匹配goal正则表达式对象
    rex_goal_obj = re.compile(str_goal_rex)
    # 只读形式打开文件
    f_name_obj = open(path, 'r')  #
    # 获取到该文件所有行
    f_lines = f_name_obj.readlines()
    # 及时关闭文件，避免造成文件占用
    f_name_obj.close()
   #tempTask= ExecutedTask()
   # tempElement=Elment()
    #tempElement.name=''
    #逐行匹配
    for i in f_lines:
        if i.__contains__('#'):
            continue
        tempTask = defsOfModel.ExecutedTask()
        tempElement = defsOfModel.Elment()
        tempTask.ID = ''
        if rex_ID_obj.search(i):
            tempTask.ID=rex_ID_obj.search(i).group()
            tempElement.ID=rex_ID_obj.search(i).group()
        if rex_name_obj.search(i):
            tempElement.name=rex_name_obj.search(i).group()
        if rex_state_obj.search(i):
            tempElement.state=rex_state_obj.search(i).group()
        else:
            tempElement.state=''
        if rex_type_obj.search(i):
            tempElement.type = defsOfModel.InTypeEnums(rex_type_obj.search(i).group())
        tempTask.Elment=tempElement
        if tempTask.ID!="":
            dicExecutedSpace[tempTask.ID]=tempTask
    for j in f_lines:
        if j.__contains__('#'):
            continue
        if rex_source_obj.search(j) and rex_goal_obj.search(j):
            snode=rex_source_obj.search(j).group()
         #   print(snode)
         #  print(type(snode))
            gnode=rex_goal_obj.search(j).group()
        #    print(gnode)
            dicExecutedSpace[snode].NonloopNxtTasks.append(gnode)
            dicExecutedSpace[gnode].PreExcTaskIDlist.append(snode)
    prunEndEvents(dicExecutedSpace)
    return assignFloors.assignFloors(dicExecutedSpace)


if __name__ == '__main__':
    mydicExeSpace=readExecutionSpace(filePath)
    tpID=mydicExeSpace.keys()
    print(tpID)
    tptask=list(mydicExeSpace.values())
    for k in range(len(tptask)):
        print('The ID is:',tptask[k].Elment.ID)
        print('The name is:',tptask[k].Elment.name)
        print('The state is:',tptask[k].Elment.state)
        print('The type is:',tptask[k].Elment.type)
        print('The PreExcTaskIDlist is:',tptask[k].PreExcTaskIDlist)
        print('The NextExcTaskIDlist is:',tptask[k].NextExcTaskIDlist)
        print('___________________')