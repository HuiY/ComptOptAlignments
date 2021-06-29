# coding=utf-8
def assignFloors(dicExcspace):
    assignFloorsStep1(dicExcspace)
    # find loops
    lsPairs = []  # list containing tuples
    for nodeid in dicExcspace:
        fathFloor = dicExcspace[nodeid].Floor
        for nxtElem in dicExcspace[nodeid].NonloopNxtTasks:
            nxtFloor = dicExcspace[nxtElem].Floor
            if (nxtFloor < fathFloor):  # 如果子层数<父层数，证明存在循环。
                lsPairs.append(nodeid + '%' + nxtElem)
    if lsPairs.__len__() == 0:
        assignFloorsNoLoop(dicExcspace)
    else:
        assignFloorsLoop(lsPairs, dicExcspace)
    #Added by Hui on Apirl 16th, 2021, to distinguish LoopnxtTasks from NonLoopNxtTasks
    for task in dicExcspace:
        for childTask in dicExcspace[task].NonloopNxtTasks:
            if dicExcspace[childTask].Floor<=dicExcspace[task].Floor:
                dicExcspace[task].LoopNxtTasks.append(childTask)
                dicExcspace[task].NonloopNxtTasks.remove(childTask)

    return dicExcspace


def assignFloorsStep1(dicSpace):
    for nodeid in dicSpace:
        dicSpace[nodeid].Floor = 0  # 每个节点层数赋值0
    # find the node has no precedessor
    strStartId = sorted(list(dicSpace.values()), key=lambda x: x.PreExcTaskIDlist.__len__())[0].ID  # 找Start节点
    dicSpace[strStartId].Floor = 0
    layerInfoMatrix = []
    layerInfoMatrix.append(dicSpace[strStartId].NonloopNxtTasks)
    imaxLayer = 0
    while True:
        tobeList = []
        i = 0
        if layerInfoMatrix[imaxLayer].__len__() > 0:  # remove loop connection for each layer
            while i < layerInfoMatrix[imaxLayer].__len__():
                j = 0
                while j < i:
                    strIthID = layerInfoMatrix[imaxLayer][i]
                    strJthID = layerInfoMatrix[imaxLayer][j]
                    if dicSpace[strIthID].NonloopNxtTasks.__contains__(strJthID):
                        layerInfoMatrix[imaxLayer].remove(strJthID)
                        i = i - 1
                        j = j - 1
                        break
                    if dicSpace[strJthID].NonloopNxtTasks.__contains__(strIthID):
                        layerInfoMatrix[imaxLayer].remove(strIthID)
                        i = i - 1
                        j = j - 1
                        break
                    j = j + 1
                i = i + 1
            for elem in layerInfoMatrix[imaxLayer]:
                dicSpace[elem].Floor = imaxLayer + 1
            for elem in layerInfoMatrix[imaxLayer]:  # for each element in the imaxLayer layer of layerInofoMatrix
                for nxtEle in dicSpace[elem].NonloopNxtTasks:
                    if dicSpace[nxtEle].Floor == 0:
                        tobeList.append(nxtEle)
                uniList = list(set(tobeList))
            layerInfoMatrix.append(uniList)
        else:
            break
        imaxLayer = imaxLayer + 1
    return dicSpace


def assignFloorsNoLoop(disSpace):
    for nodeid in disSpace:
        disSpace[nodeid].Floor = 0
    # find the node has no precedessor
    strStartId = sorted(list(disSpace.values()), key=lambda x: x.PreExcTaskIDlist.__len__())[0].ID
    disSpace[strStartId].Floor = 0
    layerInfoMatrix = []
    layerInfoMatrix.append(disSpace[strStartId].NonloopNxtTasks)
    imaxLayer = 0
    while True:
        tobeList = []
        i = 0
        if layerInfoMatrix[imaxLayer].__len__() > 0:  # remove loop connection for each layer
            while i < layerInfoMatrix[imaxLayer].__len__():
                j = 0
                while j < i:
                    strIthID = layerInfoMatrix[imaxLayer][i]
                    strJthID = layerInfoMatrix[imaxLayer][j]
                    if disSpace[strIthID].NonloopNxtTasks.__contains__(strJthID):
                        layerInfoMatrix[imaxLayer].remove(strJthID)
                        i = i - 1
                        j = j - 1
                        break
                    if disSpace[strJthID].NonloopNxtTasks.__contains__(strIthID):
                        layerInfoMatrix[imaxLayer].remove(strIthID)
                        i = i - 1
                        j = j - 1
                        break
                    j = j + 1
                i = i + 1
            for elem in layerInfoMatrix[imaxLayer]:
                disSpace[elem].Floor = imaxLayer + 1
            for elem in layerInfoMatrix[imaxLayer]:  # for each element in the imaxLayer layer of layerInofoMatrix
                for nxtEle in disSpace[elem].NonloopNxtTasks:
                    if disSpace[nxtEle].Floor == 0:
                        tobeList.append(nxtEle)
                    elif disSpace[nxtEle].Floor <= imaxLayer + 1:
                        if nxtEle != elem:
                            tobeList.append(nxtEle)
                uniList = list(set(tobeList))
            layerInfoMatrix.append(uniList)
        else:
            break
        imaxLayer = imaxLayer + 1
    return disSpace


def assignFloorsLoop(lsLoops, dicSpace):
    for nodeid in dicSpace:
        dicSpace[nodeid].Floor = 0
    # find the node has no precedessor
    strStartId = sorted(list(dicSpace.values()), key=lambda x: x.PreExcTaskIDlist.__len__())[0].ID
    dicSpace[strStartId].Floor = 0
    layerInfoMatrix = []
    layerInfoMatrix.append(dicSpace[strStartId].NonloopNxtTasks)
    imaxLayer = 0
    while True:
        tobeList = []
        i = 0
        if layerInfoMatrix[imaxLayer].__len__() > 0:  # remove loop connection for each layer
            while i < layerInfoMatrix[imaxLayer].__len__():
                j = 0
                while j < i:
                    strIthID = layerInfoMatrix[imaxLayer][i]
                    strJthID = layerInfoMatrix[imaxLayer][j]
                    if dicSpace[strIthID].NonloopNxtTasks.__contains__(strJthID):
                        layerInfoMatrix[imaxLayer].remove(strJthID)
                        i = i - 1
                        j = j - 1
                        break
                    if dicSpace[strJthID].NonloopNxtTasks.__contains__(strIthID):
                        layerInfoMatrix[imaxLayer].remove(strIthID)
                        i = i - 1
                        j = j - 1
                        break
                    j = j + 1
                i = i + 1
            for elem in layerInfoMatrix[imaxLayer]:
                dicSpace[elem].Floor = imaxLayer + 1
            for elem in layerInfoMatrix[imaxLayer]:
                flagLoop = False
                myLpChild = []
                for pair in lsLoops:
                    subPr = pair.split('%')
                    if subPr[0] == elem:
                        flagLoop = True
                        myLpChild.append(subPr[1])
                for nxtEle in dicSpace[elem].NonloopNxtTasks:
                    if flagLoop and myLpChild.__contains__(nxtEle):
                        continue  # 如果父节点->子节点存在返回，就不将子节点加入到layerInfoMatrix中
                    else:
                        if dicSpace[nxtEle].Floor == 0:
                            tobeList.append(nxtEle)
                        elif dicSpace[nxtEle].Floor <= imaxLayer + 1:
                            if nxtEle != elem:
                                tobeList.append(nxtEle)
                uniList = list(set(tobeList))
            layerInfoMatrix.append(uniList)
        else:
            break
        imaxLayer = imaxLayer + 1
    return dicSpace