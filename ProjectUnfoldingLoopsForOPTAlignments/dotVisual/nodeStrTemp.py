# coding=utf-8
from cmptOptAlignments import operatorsOfMatches


def nodeStrTemp(execTask):
    s=''
    if execTask.Elment.name=='StartEvent':
        s='[shape=circle,color=black, label="Start"];\n'
    elif execTask.Elment.name=='EndEvent':
        s = '[shape=circle,color=black,style=bold,label="End"];\n'
    else:
        #s = "[color=black, label=\"" + execTask.Elment.name +' ' + str(execTask.Floor) + "\"];\n"
        s = "[color=black, label=\"" + execTask.Elment.ID + ' ' + str(execTask.Floor) + "\"];\n"
    return s
def nodeOPEN(match):
    s=''
    if match.Type== operatorsOfMatches.TypeOfMatch.NotMatched:
        s='[shape=circle,color=blue, label="IniEntry,IniTask"];\n'
    elif match.Type== operatorsOfMatches.TypeOfMatch.BothCorrect:
        #s = "[shape=box,color=blue,style=bold, label=\"("+ match.Entry.Name +'_'+match.Entry.ID+',' + match.Task.Elment.name+'_'+match.Task.Elment.ID + ")\"];\n"
        s = "[shape=box,color=blue,style=bold, label=\"(" + match.Entry.Name+'-'+str(match.Entry.ID)+',' + match.Task.Elment.ID+'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+")\"];\n"
    elif match.Type== operatorsOfMatches.TypeOfMatch.FTaskCEntry:
        #s = "[shape=box,color=blue,style=bold, label=\"("+ match.Entry.Name +'_'+match.Entry.ID+ ",>>)\"];\n"
      #  s = "[shape=box,color=blue,style=bold, label=\"(" + match.Entry.Name + ",>>)\"];\n"
       # s = "[shape=box,color=blue,style=bold, label=\"(" + match.Entry.Name + ','+ match.PreActivities+",>>)\"];\n"
        s = "[shape=box,color=blue,style=bold, label=\"(" + match.Entry.Name+ '-'+str(match.Entry.ID)+',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+  ','+str(match.NumBoth)+','+str(match.NumDevs)+ ")\"];\n"
    elif match.Type == operatorsOfMatches.TypeOfMatch.CTaskFEntry:
        #s = "[shape=box,color=blue,style=bold, label=\"(>>_"+match.Entry.ID+","+ match.Task.Elment.name +'_'+match.Task.Elment.name+ ")\"];\n"
        #s = "[shape=box,color=blue,style=bold, label=\"(>>," + match.Task.Elment.name + ")\"];\n"
        s = "[shape=box,color=blue,style=bold, label=\"("+ match.Entry.Name+'-'+str(match.Entry.ID)+ ',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+")\"];\n"
    return s
def nodeNewCLOSED(match):
    s=''
    if match.Type == operatorsOfMatches.TypeOfMatch.NotMatched:
        s = '[shape=circle,color=red, label="IniEntry,IniTask"];\n'
    elif match.Type == operatorsOfMatches.TypeOfMatch.BothCorrect:
        #s = "[color=red,style=bold, label=\"(" + match.Entry.Name +'_'+match.Entry.ID+ ',' + match.Task.Elment.name +'_'+match.Task.Elment.ID+ ")\"];\n"
        s = "[color=red,style=bold, label=\"(" + match.Entry.Name+ '-'+str(match.Entry.ID)+',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+")\"];\n"
    elif match.Type == operatorsOfMatches.TypeOfMatch.FTaskCEntry:
        #s = "[color=red,style=bold, label=\"(" + match.Entry.Name + '_' + match.Entry.ID + ",>>)\"];\n"
        #s = "[color=red,style=bold, label=\"(" + match.Entry.Name + ",>>)\"];\n"
        s = "[color=red,style=bold, label=\"(" + match.Entry.Name+ '-'+str(match.Entry.ID)+',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+ ")\"];\n"
    elif match.Type == operatorsOfMatches.TypeOfMatch.CTaskFEntry:
        #s = "[color=red,style=bold, label=\"(>>_"+match.Entry.ID+"," + match.Task.Elment.name + ")\"];\n"
        #s = "[color=red,style=bold, label=\"\"](>>," + match.Task.Elment.name + ");\n"
        s = "[color=red,style=bold, label=\"(" + match.Entry.Name+ '-'+str(match.Entry.ID)+',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+")\"];\n"
    return s
def nodeCLOSED(match):
    s=''
    if match.Type is operatorsOfMatches.TypeOfMatch.NotMatched:
        s = '[shape=circle,color=black, label="IniEntry,IniTask"];\n'
    elif match.Type is operatorsOfMatches.TypeOfMatch.BothCorrect:
        #s = "[color=black,style=bold, label=\"(" + match.Entry.Name +'_'+match.Entry.ID+ ',' + match.Task.Elment.name +'_'+match.Task.Elment.ID+ ")\"];\n"
        s = "[color=black,style=bold, label=\"(" + match.Entry.Name+ '-'+str(match.Entry.ID)+',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+ ")\"];\n"
    elif match.Type == operatorsOfMatches.TypeOfMatch.FTaskCEntry:
        #s = "[color=black,style=bold, label=\"(" + match.Entry.Name+'_'+match.Entry.ID + ",>>)\"];\n"
        #s = "[color=black,style=bold, label=\"(" + match.Entry.Name + ",>>)\"];\n"
        s = "[color=black,style=bold, label=\"(" + match.Entry.Name+'-'+str(match.Entry.ID)+ ',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+")\"];\n"
    elif match.Type == operatorsOfMatches.TypeOfMatch.CTaskFEntry:
        #s = "[color=black,style=bold, label=\"(>>_"+match.Entry.ID+"," +'_'+match.Task.Elment.ID+ match.Task.Elment.name + ")\"];\n"
        #s = "[color=black,style=bold, label=\"(>>," + match.Task.Elment.name + ")\"];\n"
        s = "[color=black,style=bold, label=\"(" + match.Entry.Name+ '-'+str(match.Entry.ID)+',' + match.Task.Elment.ID +'-'+str(match.Task.Floor) +'\n'+ str(round(match.Cost,2))+ ','+str(match.NumBoth)+','+str(match.NumDevs)+")\"];\n"
    return s

def nodeGenInfo(showid,match):
    s=''
    #s="[shape=box,color=black,style=bold, label=\"(" + showid+":\n"+str(match.NumBoth)+ '_'+str(match.NumDevs)+")\"];\n"
    s = "[shape=box,color=black,style=bold, label=\"" + str(match.NumBoth) + '_' + str(
        match.NumDevs) + "\("+str(match.NumMvLog)+":"+str(match.NumDevs-match.NumMvLog)+"\)\"];\n"
    return s