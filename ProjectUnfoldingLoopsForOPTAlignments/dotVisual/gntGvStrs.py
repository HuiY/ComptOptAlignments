# coding=utf-8
#from nodeStrTemp import nodeStrTemp
from dotVisual import nodeStrTemp
def sourceExecSpace(dicExecspace):
    strGraphExecGv='digraph g { graph[dpi=300]; node[fontname=\"SimSun\",fontsize=10]; edge[fontname=\"SimSun\",fontsize=11]; size=\"100,100\";'
    for strnode in dicExecspace:
        strGraphExecGv=strGraphExecGv+'N'+strnode[1:strnode.__len__()]+nodeStrTemp.nodeStrTemp(dicExecspace[strnode])
    for strnode in dicExecspace:
        for nxtnode in dicExecspace[strnode].NonloopNxtTasks:
            strGraphExecGv=strGraphExecGv+'N'+strnode[1:strnode.__len__()]+'->'+'N'+nxtnode[1:nxtnode.__len__()]+';\n'
        for nxtnode in dicExecspace[strnode].LoopNxtTasks:
            strGraphExecGv=strGraphExecGv+'N'+strnode[1:strnode.__len__()]+'->'+'N'+nxtnode[1:nxtnode.__len__()]+';\n'
    strGraphExecGv=strGraphExecGv+'}'
    return strGraphExecGv

def gntCoorSystemGv(dicCoorSys,OPEN,CLOSED):
    strGraphExecGv = 'digraph g { graph[dpi=300]; node[fontname=\"SimSun\",fontsize=10]; edge[fontname=\"SimSun\",fontsize=11]; size=\"100,100\";'
    #create a dictionary to store the mapping between original ids and new ids with numbers
    dicMap={}
    id=0
    for childID in dicCoorSys:
        if dicMap.__contains__(childID)==False:
            dicMap[childID]=id
            id = id + 1
        if OPEN.__contains__(childID):
            strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[childID]) + nodeStrTemp.nodeOPEN(dicCoorSys[childID])
        elif CLOSED.__contains__(childID):
            strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[childID]) + nodeStrTemp.nodeCLOSED(dicCoorSys[childID])
    for childID in dicCoorSys:
        for fathId in dicCoorSys[childID].PreActivities:
            if dicMap.__contains__(fathId)==False:
                continue
            elif dicMap.__contains__(childID)==False:
                continue
            else:
                if dicCoorSys[childID].Entry.ID != dicCoorSys[fathId].Entry.ID and dicCoorSys[childID].Task.ID != dicCoorSys[fathId].Task.ID:
                    strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[fathId]) + '->' + 'N' + str(dicMap[childID]) + "[label=\"(" + dicCoorSys[childID].Entry.Name + ',' + dicCoorSys[childID].Task.Elment.name + ")\"];\n"
                    # elif dicCoorSys[childID].Entry.ID == dicCoorSys[fathId].Entry.ID and dicCoorSys[childID].Task.ID != dicCoorSys[fathId].Task.ID:
                elif dicCoorSys[childID].Entry.ID == dicCoorSys[fathId].Entry.ID:
                    strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[fathId]) + '->' + 'N' + str(dicMap[childID]) + "[label=\"(>>," + dicCoorSys[childID].Task.Elment.name + ")\"];\n"
                    #  elif dicCoorSys[childID].Task.Elment.ID != dicCoorSys[fathId].Task.Elment.ID and dicCoorSys[childID].Task.ID == dicCoorSys[fathId].Task.ID:
                elif dicCoorSys[childID].Task.ID == dicCoorSys[fathId].Task.ID:
                    strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[fathId]) + '->' + 'N' + str(dicMap[childID]) + "[label=\"(" + dicCoorSys[childID].Entry.Name + ",>>)\"];\n"
    strGraphExecGv = strGraphExecGv + '}'
    return strGraphExecGv

def gntLeavesGv(dicLeafNodes):
    strGraphExecGv = 'digraph g { graph[dpi=300]; node[fontname=\"SimSun\",fontsize=10]; edge[fontname=\"SimSun\",fontsize=11]; size=\"100,100\";'
    #create a dictionary to store the mapping between original ids and new ids with numbers
    dicMap = {}
    id = 0
    for childID in dicLeafNodes:
        if dicMap.__contains__(childID)==False:
            dicMap[childID]=id
            id = id + 1
        #if dicLeafNodes[childID].__len__()>0:
        strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[childID]) + nodeStrTemp.nodeGenInfo(childID,dicLeafNodes[childID])
    for id in dicLeafNodes:
        fathId=id[0:-6]
        if  dicLeafNodes.__contains__(fathId) is False:
            continue
        if dicLeafNodes.__contains__(id) is False:
            continue
        if dicMap.__contains__(fathId) is False:
            continue
        if dicMap.__contains__(id) is False:
            continue
        if fathId.__len__()>0:
            strGraphExecGv = strGraphExecGv + 'N' + str(dicMap[fathId]) + '->' + 'N' + str(dicMap[id])+";\n"
    strGraphExecGv = strGraphExecGv + '}'
    return strGraphExecGv