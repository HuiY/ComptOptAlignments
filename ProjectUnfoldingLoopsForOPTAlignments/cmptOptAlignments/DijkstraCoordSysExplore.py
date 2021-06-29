from patEvtLog.defsOfLog import AuditTrailEntry
from execspace.operatorsOnModel import EndOfModel,findNormTasks
from patEvtLog.operatorsOnLog import EndOfTrace,findCurrentEntry
from cmptOptAlignments.multiGenOperators import fatherGen,allFatherChildrenTree,isChildWorse,isGrandChildWorse,findLpPairs,oneGeneration
from cmptOptAlignments.operatorsOfMatches import AMatch,findLsLowCost,nodesPlace,findlsOptAlignment
from dotVisual.gntGvStrs import gntLeavesGv,gntCoorSystemGv
from cmptOptAlignments.dijkstraNodeExpan import dFirstMatch,dFTaskCEntry,dCTaskFEntry,dBothMatch

def exploreFaChRelation(faGEN,dicFaChGens,execspace, evtrace, OPEN, CLOSED, mydicCoorSys,Leaves):
    flagFaLeave=False
    paGenID = fatherGen(faGEN)
    flagWorse = isChildWorse(paGenID, faGEN, Leaves)
    if flagWorse is False:
        flagFaLeave = False
    else:
        flagStop = True
        if dicFaChGens.__contains__(faGEN) is False:
            SufixPairs = findLpPairs(execspace)
            dicFaChGens[faGEN] = oneGeneration(faGEN, SufixPairs)
            #dicStatFaChGens[faGEN] = copy.deepcopy(dicFaChGens[faGEN])
        for sonGenID in dicFaChGens[faGEN]:
            sonoptNode = exploreOne2DsystemUsingDijkstra(sonGenID, execspace, evtrace, OPEN, CLOSED, mydicCoorSys)
            Leaves[sonGenID] = sonoptNode
            nwFlagWorse = isChildWorse(faGEN, sonGenID, Leaves)
            if nwFlagWorse is False:#
                grandWorse = isGrandChildWorse(paGenID, sonGenID, Leaves)
                if grandWorse is False:
                    flagStop = False
        if flagStop is True:
            flagFaLeave = True
            # finalOptNodes[faGenID] = dicLeaves[faGenID]
        else:
            flagFaLeave = False
    return flagFaLeave

def exploreOne2DsystemUsingDijkstra(cskey, execspace, evtrace, OPENS, CLOSEDS, CORSYSMS):

    while True:
        flagStop=False
        if OPENS[cskey].__len__() > 0:
            newCLOSE = findLsLowCost(OPENS[cskey])
        else:
            break
        for tNode in newCLOSE:
            if EndOfTrace(tNode.Entry, evtrace.Trace) & EndOfModel(tNode.Task,execspace):  # fMatch符合结尾事件日志与结尾可执行任务完成匹配的条件
                optNode=tNode
                flagStop=True
        if flagStop is True:
            break
        for nodeClose in newCLOSE:
            OPENS[cskey].pop(nodeClose.ID)
            CLOSEDS[cskey][nodeClose.ID] = nodeClose  # Remove from OPEN a node ni whose cost is minimum and place it on a set CLOSED

            curNonLpTasks = findNormTasks(nodeClose.Task, execspace)#start: execspace[0], end:[][] (lengths are both zero)
            curEntry = findCurrentEntry(nodeClose, evtrace.Trace)#start: evtrace[0],end: 'NoEntry'
            if curNonLpTasks.__len__()==0:
                node_new=dFTaskCEntry(cskey,nodeClose,curEntry,object)
                node_new.GENID = cskey
                nodesPlace(node_new,OPENS[cskey], CLOSEDS[cskey],CORSYSMS[cskey], nodeClose)
                continue
            flagBoth = False
            for curTask in curNonLpTasks:#use BothCorrect, otherwise CTaskFEntry and FTaskCEntry ...
                #if task makes a BothCorrect with myEntry, then use myEntry's nxtEntry and task's nxtTask in loopNxt for generating nodes
                #otherwise, make a CTaskFEntry and a FTaskCEntry; also use task's nxtTask in loopNxt and myEntry for generating...
                tempEntry=AuditTrailEntry()
                if curTask.Elment.name==curEntry.Name:
                    flagBoth=True
                    node_new = dBothMatch(cskey,nodeClose, curEntry, curTask)
                    node_new.GENID = cskey
                    nodesPlace(node_new,OPENS[cskey], CLOSEDS[cskey], CORSYSMS[cskey],nodeClose)
                    nxtEntry=findCurrentEntry(node_new, evtrace.Trace)
                    tempEntry=nxtEntry
                else:
                    node_new = dCTaskFEntry(cskey,nodeClose, object, curTask)
                    node_new.GENID = cskey
                    nodesPlace(node_new,OPENS[cskey], CLOSEDS[cskey], CORSYSMS[cskey],nodeClose)
                    tempEntry=curEntry
                for lpTask in curTask.LoopNxtTasks:#BothCorrect, otherwise CTaskFEntry
                    genID=cskey + '_' + str(abs(curTask.Floor - execspace[lpTask].Floor)) + lpTask
                    if execspace[lpTask].Elment.name==tempEntry.Name:
                        node_lp=dBothMatch(genID,node_new, tempEntry, execspace[lpTask])
                    else:
                        node_lp = dCTaskFEntry(genID,node_new, object, execspace[lpTask])
                    node_lp.GENID = genID
                    if CORSYSMS.__contains__(node_lp.GENID) is False:
                        #CORKEYS.append(node_lp.GENID)
                        CORSYSMS[node_lp.GENID] = {}
                        OPENS[node_lp.GENID] = {}
                        CLOSEDS[node_lp.GENID] = {}
                        node_lp.PreActivities.append(node_new.ID)
                        CORSYSMS[node_lp.GENID][node_lp.ID] = node_lp
                        OPENS[node_lp.GENID][node_lp.ID] = node_lp
                    else:
                        nodesPlace(node_lp, OPENS[node_lp.GENID], CLOSEDS[node_lp.GENID], CORSYSMS[node_lp.GENID],node_new)
            if flagBoth is False:
                node_new=dFTaskCEntry(cskey,nodeClose, curEntry,object)
                node_new.GENID = cskey
                nodesPlace(node_new, OPENS[cskey], CLOSEDS[cskey], CORSYSMS[cskey],nodeClose)
            for lpTask in nodeClose.Task.LoopNxtTasks:
                genID = cskey + '_' + str(abs(nodeClose.Task.Floor - execspace[lpTask].Floor)) + lpTask
                if execspace[lpTask].Elment.name==curEntry.Name:
                    node_new = dBothMatch(genID, nodeClose, curEntry, execspace[lpTask])
                else:
                    node_new = dCTaskFEntry(genID, nodeClose, object, execspace[lpTask])
                node_new.GENID = genID
                if CORSYSMS.__contains__(node_new.GENID) is False:
                    #CORKEYS.append(node_new.GENID)
                    CORSYSMS[node_new.GENID] = {}
                    OPENS[node_new.GENID] = {}
                    CLOSEDS[node_new.GENID] = {}
                    #dicLeaves[node_new.GENID] = AMatch()
                    node_new.PreActivities.append(nodeClose.ID)
                    CORSYSMS[node_new.GENID][node_new.ID] = node_new
                    OPENS[node_new.GENID][node_new.ID] = node_new
                else:
                    nodesPlace(node_new, OPENS[node_new.GENID], CLOSEDS[node_new.GENID], CORSYSMS[node_new.GENID],
                               nodeClose)

    return optNode

def unfoldingLoopsExploreWithDijkstra(execspace, evtrace):
    # added Apirl 23th, 2021
    SufixPairs = findLpPairs(execspace)
    dicFaChGens = allFatherChildrenTree(SufixPairs, 100)
    # Added May 29th, to use as labeling which has finished exploration
    maxFlr = sorted(list(execspace.values()), key=lambda x: x.Floor, reverse=True)[0].Floor  # maxFloor,找出最大层数。
    myFirst = dFirstMatch(evtrace.Trace.__len__(), maxFlr)

    mydicCoorSys = {}
    mydicCoorSys['Root'] = {}
    mydicCoorSys['Root']['Root'] = myFirst

    OPEN = {}  # 待扩展的匹配集合,将起始匹配放入OPEN中。
    OPEN['Root'] = {}
    OPEN['Root']['Root'] = myFirst

    CLOSED = {}  # stores the nodes which have been expanded
    CLOSED['Root'] = {}
    dicLeaves = {}

    dicWorseThanFath = {}
    myLsCorKeys = list(mydicCoorSys.keys())
    flagFailed = True
    finalOptNodes = {}
    i = 0
    J=0
    while myLsCorKeys.__len__()>0 and i<30:
        i=i+1
        CSkey = myLsCorKeys.pop(myLsCorKeys.__len__()-1)
        if CSkey=='Root':
            optNode = exploreOne2DsystemUsingDijkstra('Root', execspace, evtrace, OPEN, CLOSED, mydicCoorSys)
            dicLeaves['Root'] = optNode

        flagFinal = True
        if dicFaChGens.__contains__(CSkey) is False:
            dicFaChGens[CSkey] = oneGeneration(CSkey, SufixPairs)
        for item in dicFaChGens[CSkey]:
            optNode = exploreOne2DsystemUsingDijkstra(item, execspace, evtrace, OPEN, CLOSED, mydicCoorSys)
            dicLeaves[item] = optNode
            flagLeave=exploreFaChRelation(item,dicFaChGens,execspace, evtrace, OPEN, CLOSED, mydicCoorSys,dicLeaves)
            if flagLeave is False:
                flagFinal=False
                myLsCorKeys.append(item)
        if flagFinal is True:
            finalOptNodes[CSkey] = dicLeaves[CSkey]

        gvSystem = ''
        # gvSystem = gntCoorSystemGv(mydicCoorSys[CSkey], OPEN[CSkey], CLOSED[CSkey], newCLOSE)
    myOptAlignment = []
    # 1. select global optimal from finalOptNodes
    # 2. output the opt alignments for that node
    finalOpt = AMatch()
    maxBoth = 0
    if finalOptNodes.__len__() == 1:
        finalOpt = list(finalOptNodes.values())[0]
        myOptAlignment.append(findlsOptAlignment(finalOpt, CLOSED, OPEN))
    else:
        for optNode in finalOptNodes.values():
            if optNode.NumBoth > maxBoth:
                maxBoth = optNode.NumBoth
        minDev = 1000
        for optNode in finalOptNodes.values():
            if optNode.NumBoth == maxBoth and optNode.NumDevs < minDev:
                minDev = optNode.NumDevs
        for optNode in finalOptNodes.values():
            if optNode.NumBoth == maxBoth and optNode.NumDevs == minDev:
                finalOpt = optNode
                myOptAlignment.append(findlsOptAlignment(finalOpt, CLOSED, OPEN))
    gvLeaves = gntLeavesGv(dicLeaves)
    #gvLeaves = gntLeavesGv(finalOptNodes)
    dicGvSystems = {}
    for genid in mydicCoorSys:
        gvSystem = gntCoorSystemGv(mydicCoorSys[genid], OPEN[genid], CLOSED[genid])
        dicGvSystems[genid] = gvSystem
    numTNodes = 0
    for iLs in mydicCoorSys:
        numTNodes = numTNodes + mydicCoorSys[iLs].__len__()

    return flagFailed, finalOpt, myOptAlignment, gvLeaves, dicGvSystems, numTNodes, dicLeaves.__len__()