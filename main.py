from BasicTrafficModel import BasicTrafficModel
import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt



#%% Random Run
timeSteps = 100 
size = [10, 10]
carsPerTimeStep = 2
a = BasicTrafficModel(size=size)
a.initializePlot()
t = 0
a.addNewCar((rd.randint(size[0]),rd.randint(size[1])),(rd.randint(size[0]),rd.randint(size[1])))
while not a.isDone():
    a.moveCars()
    a.updatePlot()
    plt.pause(0.001)
    if t < timeSteps:
        for i in range(carsPerTimeStep):
            a.addNewCar((rd.randint(size[0]),rd.randint(size[1])),(rd.randint(size[0]),rd.randint(size[1])))
        t += 1

        
#%%simpleRun
a = BasicTrafficModel()
a.initializePlot()
t=0
a.addNewCar((rd.randint(size[0]),rd.randint(size[1])),(rd.randint(size[0]),rd.randint(size[1])))
while not a.isDone():
    a.moveCars()
    a.updatePlot()
    if t < 40:
        a.addNewCar((0,0),(7,7),0)
        a.addNewCar((0,7),(7,0),0)
        a.addNewCar((7,0),(0,7),0)
        a.addNewCar((7,7),(0,0),0)
        t += 1


#%% simpleRun2
timeSteps = 100
a = BasicTrafficModel()
nCars = [ [] for i in range(timeSteps)]
a.addNewCar((0,4), (9,4),local = 0)
i = 0
while not a.isDone():
    nCars[i] = a.grabCurrentCarNumbers()
    a.moveCars()
    a.addNewCar((0,4), (9,4),local= 0)
    a.addNewCar((0,4), (9,4),local= 0)
    i += 1
    if i == timeSteps:
        break

nCars = np.array(nCars)

b = BasicTrafficModel()
b.addNewCar((0,4), (9,4),local = 0)
[axH, poPl1,poPl2,poPl3, fig] = a.initializePlot()
i = 0
while not a.isDone():
    b.setAverageCarNumber(nCars[i])
    b.moveCars()
    b.updatePlot(axH, poPl1,poPl2,poPl3, fig)
    b.addNewCar((0,4), (9,4),local= 0)
    b.addNewCar((0,4), (9,4),local= 0)
    if np.mod(i,20) == 0:
        b.addNewCar((0,9), (0,0),local= 2)
    i += 1
    if i == timeSteps:
        break

#%% simpleRun3
timeSteps = 3000
sizeA = [10,7]

start = (0,3)
target = (9,3)
spawnFreq = 5
plotFreq = 3000
predictingFraction = 1
nRepetition = 10
timeEvolution0=np.zeros((nRepetition,))
timeEvolution1=np.zeros((nRepetition,))
timeEvolution2=np.zeros((nRepetition,))

def runScenario(sizeA, timeSteps, start, target, spawnFreq, plotFreq, 
                nCars, predictingFraction): 

    a = BasicTrafficModel(size = sizeA)
    a.initializePlot()
    i = 0
    nEdges = a.G.number_of_edges()
    nCarsNew = np.zeros((timeSteps,nEdges))
    a.setAverageCarNumber(a.grabCurrentCarNumbers())
    if rd.rand() > predictingFraction:
        a.addNewCar(start, target,local= 0)
    else:
        a.addNewCar(start, target,local= 2)
        
    while len(a.cars)!=0:
        a.setAverageCarNumber(nCars[i])
        nCarsNew[i] = a.grabCurrentCarNumbers()
        a.moveCars()
        
        if i/timeSteps < 0.50:
            if i%spawnFreq == 0:
                if rd.rand() > predictingFraction:
                    a.addNewCar(start, target,local= 0)
                else:
                    a.addNewCar(start, target,local= 2)
        i += 1
        if i%100 == 0:
            print(str(i) + '/' + str(timeSteps))
            
        if i%plotFreq == 0:
            a.updatePlot()
            plt.pause(0.001)

    return np.array(nCarsNew), a
    
nCars = np.zeros((timeSteps, 840))    
for i in range(0,nRepetition):
    cumulativeTime0 = 0
    cumulativeTime1 = 0
    cumulativeTime2 = 0
    nAgentType0 = 0
    nAgentType1 = 0
    nAgentType2 = 0
    #oldnCars = nCars
    nCars,a  = runScenario(sizeA, timeSteps, start, target, spawnFreq,
                        plotFreq, nCars, predictingFraction)
    #nCars = (oldnCars + nCars)/2
    for car in a.doneCars:
        if car['local'] == 0:
            cumulativeTime0 = cumulativeTime0 + car['totaltime']
            nAgentType0 +=1
        if car['local'] == 1:
            cumulativeTime1 = cumulativeTime1 + car['totaltime']
            nAgentType1 +=1
        if car['local'] == 2:
            cumulativeTime2 = cumulativeTime2 + car['totaltime']
            nAgentType2 +=1
    print('Average Run times for Agent types:')
    if (nAgentType0)!= 0:
        print('Global Information: ' + str(cumulativeTime0/(nAgentType0)))
        timeEvolution0[i] = cumulativeTime0/(nAgentType0)
    if (nAgentType1)!= 0:
        print('Local Information: ' + str(cumulativeTime1/(nAgentType1)))
        timeEvolution1[i] = cumulativeTime1/(nAgentType1)
    if (nAgentType2)!= 0:
        print('Historical Information: ' + str(cumulativeTime2/(nAgentType2)))
        timeEvolution2[i] = cumulativeTime2/(nAgentType2)
        