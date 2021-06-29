# coding=utf-8

from patEvtLog import readEventLog
from execspace import readExcSpace
from dotVisual import gntGvStrs
from graphviz import Source
from cmptOptAlignments import DijkstraCoordSysExplore
from dotVisual.gntCSV import Alignmenttocvs
import time

if __name__ == '__main__':

    mydicExeSpace = readExcSpace.readExecutionSpace("MyExecSpace.grs")
    r0, lsPatKeys, dicLog = readEventLog.readLogFormatXes("CCC19log.xes")

    strExec=gntGvStrs.sourceExecSpace(mydicExeSpace)
    gvExec=Source(strExec)
    gvExec.format = 'png'
    #gvExec.render('PngOutput/model.gv')

    if r0.success == True and mydicExeSpace.__len__() > 0:
        with open('ResultOutput.txt','w') as f:
            for i in range(0,dicLog.__len__()):
                start=time.time()
                fgFail, aMatchFinal, myOptAlignment, strTailTree, dicStrSys, numTot, numSpaces = DijkstraCoordSysExplore.unfoldingLoopsExploreWithDijkstra(mydicExeSpace, list(dicLog.values())[i])

                end=time.time()
                elasp=end-start
                strOutput=list(dicLog.values())[i].TrID+' '+str(aMatchFinal.NumBoth)+' '+str(aMatchFinal.NumDevs)+' '+str(round(elasp,2))+' '+str(numTot)+' '+str(numSpaces)+'\n'
                j = 0
                for onegoalseq in myOptAlignment:
                    logname = 'Log' + str(i)+'optAlig'+str(j)
                    Alignmenttocvs(logname, onegoalseq)
                    j=j+1
                f.write(strOutput)