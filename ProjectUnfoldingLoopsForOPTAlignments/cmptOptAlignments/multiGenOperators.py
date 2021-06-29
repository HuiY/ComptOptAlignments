from execspace.defsOfModel import LoopStruct
#Hui added April 21st, 2021
def fatherGen(cskey):
    splitKey = cskey.split('_')
    lenSuffxix = splitKey[splitKey.__len__() - 1].__len__()
    faGenID = cskey[0:cskey.__len__() - lenSuffxix - 1]
    return faGenID

def findLpPairs(execSpace):
    dicLpInitTargt={}
    dicLpChildren={}
    for taskId in execSpace:
        if execSpace[taskId].LoopNxtTasks.__len__()>0:
            intInitPos=execSpace[taskId].Floor
            for lpTaskID in execSpace[taskId].LoopNxtTasks:
                intTargPos=execSpace[lpTaskID].Floor
                lpKey='_'+str(abs(intInitPos-intTargPos))+lpTaskID
                dicLpInitTargt[lpKey]=LoopStruct(intInitPos,intTargPos)
    for lpKey in dicLpInitTargt:
        dicLpChildren[lpKey]=[]
        targFlr=dicLpInitTargt[lpKey].TargFlr
        for lpKey1 in dicLpInitTargt:
            if dicLpInitTargt[lpKey1].InitFlr>=targFlr:
                dicLpChildren[lpKey].append(lpKey1)
    return dicLpChildren

def siblings(curKey,LPPairs):
    lsSiblings = []
    # find curKey's father Generation
    splitKey = curKey.split('_')
    lenLst = splitKey[splitKey.__len__() - 1].__len__()
    faGen = curKey[:-lenLst - 1]
    splitKey = faGen.split('_')
    lenLst = splitKey[splitKey.__len__() - 1].__len__()
    suffix = faGen[-lenLst - 1:]
    if suffix == 'Root':
        for id in LPPairs:
            lsSiblings.append('Root' + id)
    else:
        for subid in LPPairs[suffix]:
            lsSiblings.append(faGen + subid)
    return lsSiblings

def oneGeneration(curKey,LPPairs):
    lsGenIds=[]
    if curKey=='Root':
        for sfxkey in LPPairs:
            lsGenIds.append(curKey+sfxkey)
    else:
        #get the suffix of curKey
        splitKey = curKey.split('_')
        lenSuffxix = splitKey[splitKey.__len__() - 1].__len__()
        suffix = curKey[-lenSuffxix - 1:]
        for sfx in LPPairs[suffix]:
            lsGenIds.append(curKey+sfx)
    return lsGenIds

def isChildWorse(faGenId,chiGenId,dicLeaves):
    fNBoth = dicLeaves[faGenId].NumBoth
    fNDev = dicLeaves[faGenId].NumDevs
    fNMMod=dicLeaves[faGenId].NumDevs-dicLeaves[faGenId].NumMvLog
    sNBoth = dicLeaves[chiGenId].NumBoth
    sNDev = dicLeaves[chiGenId].NumDevs
    sNMMod = dicLeaves[chiGenId].NumDevs - dicLeaves[chiGenId].NumMvLog
    flagWorse = True
    #condition1: NumBoth equals, NumDev increase
    #condition2: NumBoth increase, NumMvModel increase, but the latter is larger
    detBoth=sNBoth-fNBoth
    detDev=sNDev-fNDev
    detMvMod=sNMMod-fNMMod

    #if devBoth>0:
        #flagWorse=False
    #else:
    if detBoth==0:
        if sNDev <= fNDev:  # condition 1
            flagWorse = False
    else:#condition2
        '''if detMvMod<=detBoth:
            flagWorse = False'''
        if detDev<=detBoth:
            flagWorse = False
    return flagWorse

def isoldChildWorse(faGenId,chiGenId,dicLeaves):
    fNBoth = dicLeaves[faGenId].NumBoth
    fNDev = dicLeaves[faGenId].NumDevs
    fNMMod=dicLeaves[faGenId].NumDevs-dicLeaves[faGenId].NumMvLog
    sNBoth = dicLeaves[chiGenId].NumBoth
    sNDev = dicLeaves[chiGenId].NumDevs
    sNMMod = dicLeaves[chiGenId].NumDevs - dicLeaves[chiGenId].NumMvLog
    flagWorse = True
    #condition1: NumBoth equals, NumDev increase
    #condition2: NumBoth increase, NumMvModel increase, but the latter is larger
    detBoth=sNBoth-fNBoth
    detDev=sNDev-fNDev
    detMvMod=sNMMod-fNMMod

    #if devBoth>0:
        #flagWorse=False
    #else:
    if detBoth==0:
        if sNDev <= fNDev:  # condition 1
            flagWorse = False
    else:#condition2
        if detMvMod<=detBoth:
            flagWorse = False
        '''if detDev<=detBoth:
            flagWorse = False'''
    return flagWorse

def isGrandChildWorse(faGenId,chiGenId,dicLeaves):
    fNBoth = dicLeaves[faGenId].NumBoth
    fNDev = dicLeaves[faGenId].NumDevs
    fNMMod=dicLeaves[faGenId].NumDevs-dicLeaves[faGenId].NumMvLog
    sNBoth = dicLeaves[chiGenId].NumBoth
    sNDev = dicLeaves[chiGenId].NumDevs
    sNMMod = dicLeaves[chiGenId].NumDevs - dicLeaves[chiGenId].NumMvLog
    flagWorse = True
    #condition1: NumBoth equals, NumDev increase
    #condition2: NumBoth increase, NumMvModel increase, but the latter is larger
    detBoth=sNBoth-fNBoth
    detDev=sNDev-fNDev
    detMvMod=sNMMod-fNMMod

    #if devBoth>0:
        #flagWorse=False
    #else:
    if detBoth==0:
        if sNDev <= fNDev:  # condition 1
            flagWorse = False
    else:#condition2
        if detMvMod<=detBoth:
            flagWorse = False
        '''if detDev<=detBoth:
            flagWorse = False'''
    return flagWorse

def removeChidren(fathGenID,LSCorKeys):
    i = 0
    while i<LSCorKeys.__len__():
        if LSCorKeys[i].find(fathGenID) > -1:
            del LSCorKeys[i]
            i = i - 1
        i = i + 1

def allFatherChildrenTree(lpPairs,numIter):
    dicTree={}
    #lsSiblings, faGenID = siblings('Root',lpPairs)
    lsFaths=[]
    lsFaths.append('Root')
    i=0
    while lsFaths.__len__()>0:
        i=i+1
        faKey=lsFaths[0]
        lsFaths.pop(0)
        dicTree[faKey]=[]
        chGens=oneGeneration(faKey, lpPairs)
        for chKey in chGens:
            dicTree[faKey].append(chKey)
            lsFaths.append(chKey)
        #dicTree[faKey]=chGens
        if i>numIter:
            break
    return dicTree


