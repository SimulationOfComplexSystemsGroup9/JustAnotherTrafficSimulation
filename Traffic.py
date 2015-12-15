import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from heapq import heappop, heappush
from itertools import count
class BasicTrafficModel:
    
    
    def __init__(self, vMin = 1, vMax = 15, size=[10,10], distance = 200):
        
        self.dist = distance
        self.vMin = vMin
        self.vMax = vMax
        self.G = nx.DiGraph(nx.grid_graph(size))
        self.simpleG = self.G.copy()
        self.minWeight = distance/vMax
        
        for _, _, edgeData in self.G.edges_iter(data=True): #CodingLife #BestGroup
            edgeData['dist'] = distance
            edgeData['nCars'] = 0
            edgeData['traverseT'] = lambda eD = edgeData: eD['dist']/self.edgeVelocity(eD['nCars'])
            edgeData['weight'] = edgeData['traverseT']()
                    
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
                        newPath = self.shortestPath(car['path'][1], car['path'][-1], weight = 'weight')
                    elif car['local'] == 1:
                        newPath = self.shortestPath(car['path'][1], car['path'][-1], weight = 'weight', infoRange = car['infoR'])
                    elif car['local'] == 2:
                        newPath = self.shortestPath(car['path'][1], car['path'][-1], weight = 'histWeight')
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
        i = 0
        for _, _, edgeData in self.G.edges_iter(data=True):
            edgeData['histWeight'] = (edgeData['weight'] + edgeData['dist']/self.edgeVelocity(self.nCarsAv[i]))/2.0
            i += 1

    def getCarEdge(self, car):
        path = car['path']
        return self.G[ path[car['edge']] ][ path[ car['edge'] + 1 ] ]
    
    def isDone(self):
        return len(self.cars) == 0 and len(self.doneCars) != 0

    def addNewCar(self, start, target, local = 0, infoRange = 0):
        start = (start[0],start[1])
        target = (target[0],target[1])
        if start == target:
            return
      
        car = {'edge':0, 'edgeTravT':0, 'path':None, 'time':0, 'local':local, 'totaltime':0, 'infoR': infoRange}
        
        if local == 0:
            path = self.shortestPath(start, target, weight = 'weight')
        elif local == 1:
            path = self.shortestPath(start, target, weight = 'weight', infoRange = infoRange)
        elif local == 2:
            path = self.shortestPath(start, target, weight = 'histWeight')
        
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
        
        
    def shortestPath(self, source, target, weight, infoRange = None):
        """Implementation of Dijkstra's algorithm, based on 
        implementation in networkx.
    
        Parameters
        ----------
        G : NetworkX graph
    
        source : node label
           Starting node for path
           
        target : node label
           Ending node for path
    
        weight: key for weights
            Key to use on edges to get the weight
    
        infoRange: int, optional,
            Defining usage of weight, higher means further from source
            eeeh 
    

    
        Returns
        -------
        path
           Returns the shortest path from the source to target.
           
        
        """
        #get_weight = lambda u, v, data: data.get(weight, 1)
        if source == target:
            return ({source: 0}, {source: [source]})
            
        if infoRange is not None:
            center = self.G.node[source]['pos']

        get_weight = lambda u, v, data: data.get(weight, 1)
        paths = {source: [source]}        
        
        G_succ = self.G.succ if self.G.is_directed() else self.G.adj
        
        
        push = heappush
        pop = heappop
        dist = {}  # dictionary of final distances
        seen = {source: 0}
        c = count()
        fringe = []  # use heapq with (distance,label) tuples
        push(fringe, (0, next(c), source))
        while fringe:
            (d, cnt, v) = pop(fringe)
            if v in dist:
                continue  # already searched this node.
            dist[v] = d
            if v == target:
                break
            if infoRange is None or cnt == 0:
                realWeights = True
            else:
                node = self.G.node[v]['pos']
                if abs(center[0] - node[0])< infoRange and abs(center[1] - node[1])< infoRange:
                    print(center)
                    print(node)
                    realWeights = True
            for u, e in G_succ[v].items():
                if realWeights:
                    cost = get_weight(v, u, e)
                else:
                    cost = self.minWeight
                if cost is None:
                    continue
                vu_dist = dist[v] + cost

                if u not in seen or vu_dist < seen[u]:
                    seen[u] = vu_dist
                    push(fringe, (vu_dist, next(c), u))
                    if paths is not None:
                        paths[u] = paths[v] + [u]
                
        try:
            return paths[target]
        except KeyError:
            raise nx.NetworkXNoPath(
                "node %s not reachable from %s" % (source, target))