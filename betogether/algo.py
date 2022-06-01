import random
from pandas import *
##johnsons = ['Johnson1', 'Johnson2', 'Johnson3', 'Johnson4', 'Johnson5', 'Johnson6', 'Johnson7', 'Johnson8', 'Johnson9', 'Johnson10', 'Johnson11', 'Johnson12', 'Johnson13', 'Johnson14', 'Johnson15', 'Johnson16', 'Johnson17', 'Johnson18', 'Johnson19']
johnsons = ['Johnson1', 'Johnson2', 'Johnson3', 'Johnson4', 'Johnson5', 'Johnson6']
johnsonsDic = {'Johnson1': [1, 2, 3, 6, 4, 5],
               'Johnson2': [2, 4, 3, 1, 6, 5],
               'Johnson3': [3, 2, 6, 1, 5, 4],
               'Johnson4': [4, 2, 5, 1, 3, 6],
               'Johnson5': [5, 1, 6, 2, 3, 4],
               'Johnson6': [6, 5, 2, 4, 1, 3]}

#if group is // 2 for example 6 johnsons into 2 groups of 3 then defacto will try to fill the groups before checking for need, which sets every user into a group regardless of need
#need to add a check if group is //2
#needs check on user not wroking on his own project
#needs fix on needs
#needs allow not exact groups e.g. groups of 3 and one of 4
list1 = []
for ijk in range(1,len(johnsons)+1):
    list1.append(ijk)
    
def createVal(arr, val):
    while True:
        if val in arr:
            val = random.randint(1,6)
        else:
            break
    return val

def genJohnsonsDic():
    dic = {}
    for i in enumerate(johnsons, 1):
        values = []
        for j in range(1,7):
            value = createVal(values, i[0])
            values.append(value)
        dic[i[1]] = values                  
    return dic

def askGrpSize(maxSize):
    grpSize = int(input("what size group, choose between 2=>{}: ".format(maxSize)))
    if not (grpSize >= 2) or not (grpSize <= maxSize):
        print("invalid group size")
        askGrpSize(maxSize)
    return grpSize

def createGroups():
    groups = {}
    maxSize = len(johnsonsDic)//2
    grpSize = askGrpSize(maxSize)
    for i in range(len(johnsonsDic)//grpSize):
        groups[i] = []
##    for i in johnsonsDic:
##        for j in johnsonsDic[i]:
##            print(j)
    return groups

def getIdDic():
    id = {}
    for i,j in enumerate(johnsons):
        id["id{}".format(i+1)] = 0
    return id

def findAcceptedProjectsValues():
    id = getIdDic()
    for i in johnsonsDic:
        for j,k in enumerate(johnsonsDic[i]):
            id["id{}".format(k)] += len(johnsons)-int(j)
    return id

def findAcceptedProjects():
    grp = createGroups()#get groups to see the length
    id = findAcceptedProjectsValues() # get values of the projects chosen
    accPro = []#create accepted Prjects
    print(id)
    for i,j in enumerate(id): #for each project value
        if i < len(grp): #if is porject 1 to len(grp) by default accepted
           accPro.append(j)
        else: #for the rest of the projects verify best values
            val = [] #create values list to sort best values
            for k in accPro: #for each item in accepted project add their value for comparaison
                val.append(id[k])
            index = val.index(min(val)) #get index of minimum value
            if id[accPro[index]] < id[j]:#finally replace id of minimum value by current best value in accepted projects
                accPro[index] = j
    return accPro, grp
        
def projectsMatrix():#projectsMatrix
    projects, grp = findAcceptedProjects() #get accepted projects id
    print(projects)
    accPro = []
    matrix = []
    for l in projects: # transform the id's into values
        accPro.append(int(l.lstrip("id")))
    for k,i in enumerate(johnsonsDic):#for each wishlist
        matrix.append([])#create a row
        for j in johnsonsDic[i]:#for each row/ for each wishlist
            if j in accPro: #if wish is an accepted Project add project
                matrix[k].append(j)
            else:#else add null
                matrix[k].append(0)
    return matrix, projects, accPro, grp

def nestedLoops(i,groups):
    for i2 in groups:
        for j2 in groups[i2]:
            for k2 in j2:
                if (i+1) == k2:
                    return True
    return False
        

def iterate(matrix,groups,finalMatrix,grp,index=0):
    index += 1
    if index > len(matrix): # to verify if > or >= probably out of index if >
        return
    for i in range(len(matrix)):
        for j,k in enumerate(matrix[i]):
            if k != 0:
                if j == 0 and index == 1:
##                    print({k:index},groups["id{}".format(k)])
                    if {k:index} not in groups["id{}".format(k)]:
                        finalMatrix[i][j] = k
                        groups["id{}".format(k)].append({k:index})#"user{}".format(k)
                        for z in range(1,len(matrix[i])):
                            matrix[i][z] = 0
                elif index > 1 and j != 0:
                    isBreak = nestedLoops(i,groups)
                    if isBreak:
                        break
                    finalMatrix[i][j] = k
                    if len(groups["id{}".format(k)]) < len(johnsonsDic)//len(grp):
                        if index <= j+1:
                            groups["id{}".format(k)].append({i+1:index})
                            #matrix[i][j] = 0
                            break
                    else:
                        isBreak = False
                        for i3 in groups: # for list in group
                            for z2,j3 in enumerate(groups[i3]): #for objects in list
                                if z2 != 0: #if objects (= to first user in group) is 0 then skip
                                    for x in j3: #for associated index of user added in group
                                        print(groups,index)
                                        if j3[x] < index:
##                                            print(groups[i3][z2][x])
                                            groups[i3][z2] = {i+1:index}
                                            index = j3[x]-1
                                            isBreak = True
                                            break
                                    else:
                                        if isBreak:
                                            break
                            else:
                                if isBreak:
                                    break
    iterate(matrix,groups,finalMatrix,grp,index)

def test():#algoV1
    matrix, projects, accPro, grp = projectsMatrix() #accPro maybe not useful
    global groups
    groups = {} #create groups with the project's id
    print(DataFrame(matrix,list1,list1))
    finalMatrix = []#create the final matrix
    for a in range(len(matrix)):
        finalMatrix.append([])
        for b in range(len(matrix[a])):
            finalMatrix[a].append(0)
##    print(DataFrame(finalMatrix))
    for x,y in enumerate(projects):
        groups[y] = []
    print(groups, grp)
    iterate(matrix,groups,finalMatrix,grp)
    print(groups)
    return finalMatrix


print(johnsonsDic)
print(DataFrame(test(),list1,list1))
