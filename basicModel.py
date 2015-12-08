import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rd
import matplotlib.cm as cm

class BasicTrafficModel:
    
    
    def __init__(self, vMin = 1, vMax = 15, size=[8,8], distance = 200, nSimCars = 1, local = False):
        
        self.dist = distance
        self.vMin = vMin
        self.vMax = vMax
        self.G = nx.DiGraph(nx.grid_graph(size))
        self.nSimCars = nSimCars
        self.simpleG = self.G.copy()
        
        for _, _, edgeData in self.G.edges_iter(data=True): #CodingLife #BestGroup
            edgeData['dist'] = distance
            edgeData['nCars'] = 0
            edgeData['traverseT'] = lambda eD = edgeData: eD['dist']/self.edgeVelocity(eD['nCars'])
            edgeData['weight'] = edgeData['traverseT']()
        
        for _, _, edgeData in self.simpleG.edges_iter(data=True): #For adding only local information
            edgeData['weight'] = distance/vMax
        
        for pos, data in self.G.nodes(data=True):
            data['pos'] = pos   
        
        start = []
        target = []
        l = size[0]-1
        
        for i in range(nSimCars):
            start.append((rd.randint(0,l/2),rd.randint(0,l/2)))
            target.append((rd.randint(l/2,l),rd.randint(l/2,l)))
         
        cars = [{'edge':0,'edgeTravT':0, 'path':None, 'time':0, 'local':False, 'totaltime':0} for i in range(nSimCars)]
        
        for i in range(nSimCars):
            car = cars[i]
            if cars[i]['local'] == True:
              path = self.localShortestPath(start[i],target[i])
            else:
              path = nx.shortest_path(self.G,start[i],target[i])
            car['path'] = path
            self.G[path[0]][path[1]]['nCars'] += 1
            
        for car in cars:
            edge = self.getCarEdge(car)
            car['edgeTravT'] = edge['traverseT']()
            
            edge['weight'] = edge['traverseT']()
            
        self.cars = cars
        self.doneCars = []


    def moveCars(self):
        
        for car in self.cars:
            car['time'] += 1
            if car['time'] >= car['edgeTravT']:
                edge = self.getCarEdge(car)
                edge['nCars'] -= 1
                car['edge'] += 1
                car['totaltime'] = car['totaltime'] + car['time']
                
                edge['weight'] = edge['traverseT']() #Recalculate weights for 
                
                if len(car['path']) > 2:
                    car['time'] = 0
                    if car['local'] == True:
                      car['path'] = self.localShortestPath(car['path'][1],car['path'][-1])
                      car['edge'] = 0
                    else:
                      car['path'] = nx.shortest_path(self.G,car['path'][1],car['path'][-1], weight = 'weight')
                      car['edge'] = 0
                    
                    edge = self.getCarEdge(car)
                    edge['nCars'] += 1
                    car['edgeTravT'] = edge['traverseT']() #edge['dist']/edge['nCars'] #
                    
                    edge['weight'] = edge['traverseT']()
        
                    
                else:
                    self.doneCars.append(car)
                    self.cars.remove(car)


    def getCarEdge(self, car):
        path = car['path']
        return self.G[ path[car['edge']] ][ path[ car['edge'] + 1 ] ]
    
    
    def isDone(self):
        return len(self.cars) == 0


    def addNewCar(self, start, target,local=False):
        if start == target:
            return
        self.nSimCars += 1
        car = {'edge':0,'edgeTravT':0, 'path':None, 'time':0, 'local':local, 'totaltime':0}
        if local == True:
              path = self.localShortestPath(start,target)
        else:
              path = nx.shortest_path(self.G,start,target)
             
        car['path'] = path
        self.G[path[0]][path[1]]['nCars'] += 1
        edge = self.getCarEdge(car)
        car['edgeTravT'] = edge['traverseT']()
        
        self.cars.append(car)
        
    def initializePlot(self, axHandle = None):
        pos = nx.get_node_attributes(self.G,'pos')
        if axHandle is None:
              plt.close('all')
              fig = plt.figure()
              axHandle = fig.add_subplot(111)
        nx.draw_networkx_edges(self.G ,pos, ax = axHandle, width = 3, arrows = False)
                               
        positions = self.getCarPositions()
        positionplot, = axHandle.plot(positions[0],positions[1],'ro')
        positionplot.set_data(positions[0],positions[1])
        return axHandle, positionplot


    def updatePlot(self, axHandle, positionplot): 
        positions = self.getCarPositions()
        positionplot.set_data(positions[0],positions[1])
        
        
    def getCarPositions(self):
        positions = np.zeros((2,self.nSimCars))
        i = 0
        for car in self.cars:
            edge = car['edge']
            nodes = [car['path'][edge], car['path'][edge+1]]
            fraction = car['time']/car['edgeTravT']
            positions[0][i] = nodes[0][0] + fraction*(nodes[1][0]-nodes[0][0])
            positions[1][i] = nodes[0][1] + fraction*(nodes[1][1]-nodes[0][1])
            i += 1
        for car in self.doneCars:
            node = car['path'][-1]
            positions[0][i] = node[0]
            positions[1][i] = node[1]
            i += 1
        return positions
    
    def edgeVelocity(self, nCars):
        maxCars = self.dist/10
        v = (self.vMin-self.vMax)/(maxCars-maxCars/2) * 0.75*(nCars - maxCars/2) + self.vMax/2
        v = np.max([self.vMin,np.min([v,self.vMax])])
        return v

    def localShortestPath(self, start, target, infoRange = 1):
        
        P = self.simpleG.copy()
        
        def copyEdgeWeights(infoRange, start):
            for node in P[start]:
                P[start][node]['weight'] =  self.G[start][node]['weight']
                if infoRange>1:
                    copyEdgeWeights(infoRange-1, node)
        
        copyEdgeWeights(infoRange,start)
        
        localShortestPath = nx.shortest_path(P, start, target, weight = 'weight')
        return localShortestPath
    
def randomRun(timeSteps, size = [10, 10]):
    a = BasicTrafficModel(nSimCars = 1,size=size)
    [c,d] = a.initializePlot()
    t = 0
    while not a.isDone():
        a.moveCars()
        a.updatePlot(c,d)
        plt.pause(0.001)
        if t < timeSteps:
            po = [tuple(rd.randint(10,size=2)) for i in range(4)]
            a.addNewCar(po[0],po[1])
            a.addNewCar(po[2],po[3])
            t += 1
            
def simpleRun():
    a = BasicTrafficModel(nSimCars = 10)
    [c,d] = a.initializePlot()
    t=0
    while not a.isDone():
        a.moveCars()
        a.updatePlot(c,d)
        plt.pause(0.01)
        if t < 40:
            a.addNewCar((0,0),(7,7),True)
            a.addNewCar((0,7),(7,0),True)
            a.addNewCar((7,0),(0,7),True)
            a.addNewCar((7,7),(0,0),True)
            t+=1

def Visualize(loc):
  a = BasicTrafficModel(nSimCars = 10, local = loc)
  [c,d] = a.initializePlot()
  x = a.getCarPositions()
  
  i =0
  while not a.isDone():
      a.moveCars()
      a.updatePlot(c,d)
      plt.pause(0.001)
      #if np.mod(i,10) == 0:
      a.addNewCar((0,4), (9,4),local= loc)
      a.addNewCar((0,4), (9,4),local= loc)
      i=+1