import csv
from cmptOptAlignments.operatorsOfMatches import TypeOfMatch
def Alignmenttocvs(tocvsname,myOptAlignment):   #类型字典
    k = len(myOptAlignment[1])
    tocvsname = tocvsname + '.csv'
    with open(tocvsname, 'w', encoding='GBK', newline="") as csvfile:
        fieldnames = []
        for j in range(0, k + 1):
            fieldnames.append(str(j))
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        listx = []
        listy = []
        listno = []
        i=0
        for v in myOptAlignment.values():
            j = 0
            v.reverse()
            listx.append('Alignment' + str(i + 1))
            listy.append('')
            while (j < len(v)):
                if v[j].Type == TypeOfMatch.NotMatched:
                    listx.append(v[j].Entry.Name)
                    listy.append(v[j].Task.Elment.name)
                    j = j + 1
                elif v[j].Entry.ID != v[j - 1].Entry.ID and v[j].Task.ID != v[j - 1].Task.ID:
                    listx.append(v[j].Entry.Name)
                    listy.append(v[j].Task.Elment.name)
                    j = j + 1
                elif v[j].Entry.ID == v[j - 1].Entry.ID:
                    listx.append("<<")
                    listy.append(v[j].Task.Elment.name)
                    j = j + 1
                elif v[j].Task.ID == v[j - 1].Task.ID:
                    listx.append(v[j].Entry.Name)
                    listy.append("<<")
                    j = j + 1
            writer.writerow(listx)
            writer.writerow(listy)
            listx = []
            listy = []
            writer.writerow(listno)
            i=i+1