from random import choice, randint, seed
import numpy as np
#import scipy.stats
seed(123)
import math

def generateUserCompetencies(ClassLevelCompetencies, gamma):
    probs = np.random.dirichlet(gamma * ClassLevelCompetencies)
    return probs

def generatePeakedProbabilities(numCategories, alpha):
    probs = np.random.dirichlet(alpha=[alpha]*numCategories)
   # result = np.round(probs,2).tolist()
    return probs

#generatePeakedProbabilities()

def NormalDistrubtion(Mu, Sigma, min, max):
    generated = int(np.random.normal(Mu, Sigma, 1)[0])
    if generated < min:
        return min
    elif generated > max:
        return max
    return generated
#NormalDistrubtion(Q_mu, Q_sigma, 1, 100)


def getTopicfromDistribution(numCategories, maxTopic,listOfTopics):
    tempTopics = listOfTopics[:] # getting a copy to change
    Q = np.ones(maxTopic)*1/maxTopic
    numOfTopics = np.random.choice(np.arange(1, maxTopic+1), p=Q)
    topics = []
    for i in range(0,numOfTopics):
        P = np.ones(len(tempTopics))*1/len(tempTopics)
        choice = np.random.choice(tempTopics, p=P)
        topics.append(choice)
        tempTopics.remove(choice)                                
                                                                        
    return topics


def createUsers(N, M, T, clasLevelComp,gamma, Q_mu, Q_sigma):
    users = []
    for i in range(N):
        current = []
        current.append('u' + str(i)) #id
        current.append(NormalDistrubtion(Q_mu, Q_sigma,1, M)) #number of questions
        current.append(generateUserCompetencies(clasLevelComp,gamma)) # knowledge gaps
        users.append(current)
        
    return users

def createTopics(numCategories):
    topics = []
    for i in range(numCategories):
        topics.append('T'+str(i+1))
    return topics

    
def createQuestions(M,T, listOfTopics, maxTopic, D_mu, D_sigma):
    questions = []
    for i in range(M):
        current = []
        current.append('q' + str(i)) #id
        current.append(getTopicfromDistribution(T,maxTopic,listOfTopics)) #topic
        current.append(NormalDistrubtion(D_mu, D_sigma,1,5)) #difficulty of question
        questions.append(current)
    return questions
            
#createQuestions(5)  

def computeDifficulty(mean, knowledgeGap):
    return NormalDistrubtion(mean- 1 +2*knowledgeGap, 0.5,1,5)
# computeDifficulty(2, 1)

#def computeanswer(knowledgeGap):
#    return np.random.choice(np.arange(0,2), p=[knowledgeGap, 1-knowledgeGap])                
                
def computeanswer(knowledgeGap):
    competency = 1-knowledgeGap
    probofSuccess =  (1)/(1 + math.exp( -0.5 * (competency*20 - 10) -  0.5))
    return np.random.choice([-1,1], p=[1-probofSuccess, probofSuccess])     
    #return np.random.choice(np.arange(0,2), p=[1-probofSuccess, probofSuccess])     
    #return np.random.choice(np.arange(0,2), p=[knowledgeGap, 1-knowledgeGap])                
   
    

def getAvgCompetencyAcrossTopics(competencies, questionTopics, listOfTopics):
    sumOfComp = 0
    for value in questionTopics:
        indexOfTopic = listOfTopics.index(value)
        sumOfComp= sumOfComp + competencies[indexOfTopic]
        
    return sumOfComp / float(len(questionTopics))
    
    
def createOutput(N,M, Users, Questions, listOfTopics):
    selected = np.zeros((N, M))
    SQA= []
    QT = []
    for u in range(N): # create  SQA
        numQ = Users[u][1] #number of questions done by user i
        for j in range(numQ):
            #pick new question to answer
            q = randint(0,M-1)
            while (selected[u][q]==1):
                q = randint(0,M-1)
            selected[u][q]=1
            A = computeanswer(getAvgCompetencyAcrossTopics(Users[u][2],Questions[q][1],listOfTopics))
            SQA.append([Users[u][0], Questions[q][0], A])            
    for q in range(M): # create  QT
        for topics in Questions[q][1]:
            #QT.append([Questions[q][0], Questions[q][1]])
            QT.append([Questions[q][0], topics])
    
    return SQA, QT


def createDataset(inputParams): 
    N = int(inputParams['studentNumber'])
    M = int(inputParams['questionNumber'])
    numCategories = int(inputParams['topicNumber'])
    A = N * int(round(int(M)/10)) #number of answers
    alpha = float(inputParams['studentDiversity'])
    maxTopic = 2 # Maxuimum number of topics per quewtion
    D_sigma = 2
    Q_mu = A/N #average number of questions per users
    Q_sigma = 10 # Standard deviation on number of questoins
    D_mu = float(inputParams['questionDifficulty'])*4
    gamma = float(inputParams['topicDiversity'])* 100
    clasLevelComp = generatePeakedProbabilities(numCategories, gamma)
    listOfTopics = createTopics(numCategories)
    Users= createUsers(N, M, numCategories, clasLevelComp,gamma, Q_mu, Q_sigma)
    Questions = createQuestions(M,numCategories,listOfTopics, maxTopic, D_mu, D_sigma)
    SQA, QT = createOutput(N,M,Users,Questions,listOfTopics)
    return SQA, QT





def exists(edges, n1, n2):
    for i in edges:
        if (i[0] == n1 and i[1] == n2) or (i[1] == n1 and i[0] == n2):
            return True
    return False

def MakeData(inputParams):
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