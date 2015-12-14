import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rd
import matplotlib.cm as cm

class BasicTrafficModel:
    
    
    def __init__(self, vMin = 1, vMax = 15, size=[10,10], distance = 200):
        
        self.dist = distance
        self.vMin = vMin
        self.vMax = vMax
        self.G = nx.DiGraph(nx.grid_graph(size))
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
            
        self.cars = []
        self.doneCars = []

    def moveCars(self):
        
        for car in self.cars:
            car['time'] += 1
            
            if car['time'] >= car['edgeTravT']: # Is the the car at the end of its' edge
                edge = self.getCarEdge(car)

                if len(car['path']) > 2: # Is the car not done

                    if car['local'] == 0:
                        newPath = nx.shortest_path(self.G,car['path'][1],car['path'][-1], weight = 'weight')
                    elif car['local'] == 1:
                        newPath = self.localShortestPath(car['path'][1],car['path'][-1])
                    elif car['local'] == 2:
                        newPath = self.shortestPathUsingAverage(car['path'][1],car['path'][-1], self.nCarsAv)                    
                    newEdge = self.G[newPath[0]][newPath[1]]

                    if newEdge['nCars'] < newEdge['dist']/10:
                        edge['nCars'] -= 1                        
                        newEdge['nCars'] += 1
                        car['path'] = newPath
                        car['edgeTravT'] = newEdge['traverseT']() 
                        newEdge['weight'] = newEdge['traverseT']()
                        edge['weight'] = edge['traverseT']()
                        car['totaltime'] = car['totaltime'] + car['time']                        
                        car['time'] = 0
                        
                    
                else:
                    edge['nCars'] -= 1
                    self.doneCars.append(car)
                    self.cars.remove(car)

    def setAverageCarNumber(self, avCars):
        self.nCarsAv = avCars
    
    def getCarEdge(self, car):
        path = car['path']
        return self.G[ path[car['edge']] ][ path[ car['edge'] + 1 ] ]
    
    def isDone(self):
        return len(self.cars) == 0

    def addNewCar(self, start, target, local = 0):
        if start == target:
            return
      
        car = {'edge':0,'edgeTravT':0, 'path':None, 'time':0, 'local':local, 'totaltime':0}
        if local == 0:
            path = nx.shortest_path(self.G,start,target, weight='weight')
        elif local == 1:
            path = self.localShortestPath(start,target)
        elif local == 2:
            path = self.shortestPathUsingAverage(start,target, self.nCarsAv)
        
        car['path'] = path
        self.G[path[0]][path[1]]['nCars'] += 1
        edge = self.getCarEdge(car)
        car['edgeTravT'] = edge['traverseT']()
        
        self.cars.append(car)
        
    def initializePlot(self, axHandle = None):
        pos = nx.get_node_attributes(self.G,'pos')
        if axHandle is None:
              plt.close('all')
              self.fig = plt.figure()
              self.axHandle = self.fig.add_subplot(111)
        nx.draw_networkx_edges(self.G ,pos, ax = self.axHandle, width = 3, arrows = False)
                               
        [positions1, positions2, positions3] = self.getCarPositions()
        self.positionplot1, = self.axHandle.plot(positions1[0],positions1[1], 'bo')
        self.positionplot2, = self.axHandle.plot(positions2[0],positions2[1], 'ro')
        self.positionplot3, = self.axHandle.plot(positions3[0],positions3[1], 'go')
        self.fig.canvas.draw()

    def updatePlot(self): 
        [positions1, positions2, positions3] = self.getCarPositions()
        self.positionplot1.set_data(positions1[0],positions1[1])
        self.positionplot2.set_data(positions2[0],positions2[1])
        self.positionplot3.set_data(positions3[0],positions3[1])
        plt.pause(0.00001)
        self.fig.canvas.draw()
        
    def getCarPositions(self):
        positions1,positions2,positions3 = [[],[]],[[],[]],[[],[]]
        for car in self.cars:
            edge = car['edge']
            nodes = [car['path'][edge], car['path'][edge+1]]
            fraction = min(car['time']/car['edgeTravT'],1)
            loc = car['local'] 
            if loc == 0:
                positions1[0].append(nodes[0][0] + fraction*(nodes[1][0]-nodes[0][0]))
                positions1[1].append(nodes[0][1] + fraction*(nodes[1][1]-nodes[0][1]))
            elif loc == 1:
                positions2[0].append(nodes[0][0] + fraction*(nodes[1][0]-nodes[0][0]))
                positions2[1].append(nodes[0][1] + fraction*(nodes[1][1]-nodes[0][1]))
            elif loc == 2:
                positions3[0].append(nodes[0][0] + fraction*(nodes[1][0]-nodes[0][0]))
                positions3[1].append(nodes[0][1] + fraction*(nodes[1][1]-nodes[0][1]))
                
        for car in self.doneCars:
            node = car['path'][-1]
            loc = car['local'] 
            if loc == 0:
                positions1[0].append(node[0])
                positions1[1].append(node[1])
            elif loc == 1:
                positions2[0].append(node[0])
                positions2[1].append(node[1])
            elif loc == 2:
                positions3[0].append(node[0])
                positions3[1].append(node[1])
                
        return positions1, positions2, positions3
    
    def edgeVelocity(self, nCars):
        maxCars = self.dist/50
        v = (self.vMin-self.vMax)/(maxCars-maxCars/2) * 0.75*(nCars - maxCars/2) + self.vMax/2
        v = np.max([self.vMin,np.min([v,self.vMax])])
        return v
    
    def grabCurrentCarNumbers(self):
        return [edge['nCars'] for _, _, edge in self.G.edges_iter(data=True)]

    def localShortestPath(self, start, target, infoRange = 2):
        
        P = self.simpleG.copy()
        
        def copyEdgeWeights(infoRange, start):
            for node in P[start]:
                P[start][node]['weight'] =  self.G[start][node]['weight']
                if infoRange>1:
                    copyEdgeWeights(infoRange-1, node)
        
        copyEdgeWeights(infoRange,start)
        
        localShortestPath = nx.shortest_path(P, start, target, weight = 'weight')
        return localShortestPath
        
    def shortestPathUsingAverage(self, start, target, nCarsAv):
        i = 0
        for _, _, edgeData in self.G.edges_iter(data=True):
            edgeData['weight'] = (edgeData['weight'] + edgeData['dist']/self.edgeVelocity(nCarsAv[i]))/2.0
            i += 1
        
        shortestPath = nx.shortest_path(self.G, start, target, weight = 'weight')
        
        for _, _, edgeData in self.G.edges_iter(data=True):
            edgeData['weight'] = edgeData['traverseT']()
            
        return shortestPath
        
    def createGraph(self, nSideTracks, length):
        G = nx.grid_graph([length,nSideTracks*2+1])
        mid = nSideTracks
        if nSideTracks != 0:
            for i in range(length):
                if np.mod(i,3) != 0:
                    G.remove_edge((i,mid),(i,mid+1))
                    G.remove_edge((i,mid),(i,mid-1))
              
            G.add_edge((0,mid),(-1,mid))
            G.add_edge((length-1,mid),(length,mid))
            for i in range(nSideTracks):
                G.add_edge((-1,mid),(0,mid+i+1))
                G.add_edge((-1,mid),(0,mid-i-1))
                G.add_edge((length,mid),(length-1,mid+i+1))
                G.add_edge((length,mid),(length-1,mid-i-1))
            
        G = nx.DiGraph(G)
        return G
        