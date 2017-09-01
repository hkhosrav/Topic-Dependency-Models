from random import choice, randint, seed
import numpy as np
seed(123)
import math

def mapTagsToNumbers(QT):
    map = {}
    current =0
    for row in QT:
        tag = row[1]
        if map.has_key(tag)==False:
            map[tag]=current
            current = current+1

    return map, current

def mapUsersToNumbers(SQA):
    map = {}
    current =0
    for row in SQA:
        user = row[0]
        if map.has_key(user)==False:
            map[user]=current
            current = current+1

    return map, current  

def mapQuestionsToNumbers(SQA):
    map = {}
    current =0
    for row in SQA:
        question = row[1]
        if map.has_key(question)==False:
            map[question]=current
            current = current+1
    return map, current 

def createTMatrix(QT, qDict, qSize, tDict, tSize):
    QTMat = np.zeros((qSize, tSize)) 
    for row in QT:
        qid = row[0]
        tag = row[1] 
        if qDict.has_key(qid)==True and tDict.has_key(tag)==True:
            QTMat[qDict[qid]][tDict[tag]] =1
        
    sumRows = QTMat.sum(axis=1)
    for i in range (1, len(sumRows)):
        if sumRows[i]>0:
            QTMat[i] = QTMat[i]/sumRows[i]
    return QTMat

def createAMatrix(SQA, uDict, uSize, qDict, qSize):
    AMat = np.zeros((uSize, qSize))
    i =0
    for row in SQA:
        id1 = row[0]
        id2  = row[1] 
        rating = row[2]
        if uDict.has_key(id1)==True and qDict.has_key(id2)==True:
            AMat[uDict[id1]][qDict[id2]] = rating
    return AMat    

def createIndexMatrix(SQA, uDict, uSize, qDict, qSize):
    AIndexMat = np.zeros((uSize, qSize))
    i =0
    for row in SQA:
        id1 = row[0]
        id2  = row[1] 
        if uDict.has_key(id1)==True and qDict.has_key(id2)==True:
            AIndexMat[uDict[id1]][qDict[id2]] = 1
    return AIndexMat    

# ## From Achivements to Visual Dependency Graph

# In[218]:

def getTopicString(topics):
    tempList = np.nonzero(topics)[0].tolist()
    key = ','.join(str(e) for e in tempList)
    return key

def addTopicCombination(T):
    topicCombinations={}
    for i in range(len(T)):
        topics = T[i]
        key = getTopicString(topics)
        if topicCombinations.has_key(key)==False and key <>'' and key.count(',') <2: #second part is for removing edges with more two nodes for the time being
            topicCombinations[key]=[0,0]
    return topicCombinations



def ComputeScopeCompetency(A, T, I_A,topicCombinations):
    for j in range(len(A[0])):
        # scope
        current_I_A= I_A[:,j]
        key = getTopicString(T[j])
        if  key <>'' and key.count(',') <2: #removing edges with more two nodes for the time being

            values = topicCombinations[key]
            values[0]= values[0] + current_I_A.sum()

            # competencie
            current_A= A[:,j]
            key = getTopicString(T[j])
            values = topicCombinations[key]
            values[1]=(current_A.sum()+ values[1])
       
    return topicCombinations

def ComputeIndividualScopeCompetency(A, T, I_A,topicCombinations,Individual):

    #sort students according to their total scores
    
    unsorted_d={}
    for i in range(len(A)):
        unsorted_d[i] = A[i].sum()
    sorted_d = sorted(unsorted_d,key=lambda x:unsorted_d[x])

    #match Individual's competency with one student

    if Individual == 1:
        target = sorted_d[len(sorted_d)-1]
    else:
        target = sorted_d[int(Individual*len(sorted_d))]
    
    for j in range(len(A[target])):
        # scope
        key = getTopicString(T[j])
        if  key <>'' and key.count(',') <2: #removing edges with more two nodes for the time being

            values = topicCombinations[key]
            values[0]= values[0] + I_A[target][j]

            # competencie
            key = getTopicString(T[j])
            values = topicCombinations[key]
            values[1]=(A[target][j]+ values[1])
       
    return topicCombinations    

def createGraphList(updatedTopicCombinations, tDict):
    output = []
    for key in updatedTopicCombinations:
        values = updatedTopicCombinations[key]
        nodes = key.split(',')
        if len(nodes)==1:
            output.append([tDict.keys()[tDict.values().index(int(nodes[0]))],tDict.keys()[tDict.values().index(int(nodes[0]))],int(values[0]*1), int( values[1]/max(values[0],1)*100 )]   )
        if len(nodes)==2:
            output.append([tDict.keys()[tDict.values().index(int(nodes[0]))],tDict.keys()[tDict.values().index(int(nodes[1]))], int( values[0] *1), int ( values[1]/max(values[0],1)*100)] )
    return output    

def getnodes(tDict):
    nodes = []
    for key in tDict:
        nodes.append(key)
    return nodes


def generateTDM(SQA, QT):
     tDict, tSize = mapTagsToNumbers(QT)
     uDict, uSize = mapUsersToNumbers(SQA) 
     qDict, qSize =mapQuestionsToNumbers(SQA)    
     T =  createTMatrix( QT, qDict, qSize, tDict, tSize)
     A  = createAMatrix(SQA, uDict, uSize, qDict, qSize) 
     I_A = createIndexMatrix(SQA, uDict, uSize, qDict, qSize)
     topicCombinations= addTopicCombination(T)
     updatedTopicCombinations = ComputeScopeCompetency(A, T, I_A,topicCombinations)
     edges = createGraphList(updatedTopicCombinations, tDict)
     nodes = getnodes(tDict)
     return {
        "edges": edges,
        "nodes": nodes
    }

def generateIndividualTDM(SQA, QT, individualComp):
     tDict, tSize = mapTagsToNumbers(QT)
     uDict, uSize = mapUsersToNumbers(SQA) 
     qDict, qSize =mapQuestionsToNumbers(SQA)    
     T =  createTMatrix( QT, qDict, qSize, tDict, tSize)
     A  = createAMatrix(SQA, uDict, uSize, qDict, qSize) 
     I_A = createIndexMatrix(SQA, uDict, uSize, qDict, qSize)
     topicCombinations= addTopicCombination(T)
     updatedTopicCombinations = ComputeIndividualScopeCompetency(A, T, I_A,topicCombinations,individualComp)
     edges = createGraphList(updatedTopicCombinations, tDict)
     nodes = getnodes(tDict)
     return {
        "edges": edges,
        "nodes": nodes
    }





def exists(edges, n1, n2):
    for i in edges:
        if (i[0] == n1 and i[1] == n2) or (i[1] == n1 and i[0] == n2):
            return True
    return False


def createGraph(inputParams):
    nodes = []
    edges = []

    for i in range(int(inputParams['topicNumber'])):
        nodes.append('T'+str(i+1))



    for i in range(30):
        n1 = choice(nodes)
        n2 = choice(nodes)
        if not exists(edges, n1, n2):
            edges.append([
                n1,
                n2,
                randint(0, 100),
                randint(0, 100)
            ])

    return {
        "edges": edges,
        "nodes": nodes
    }