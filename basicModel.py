import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rd

#%% Functions:

def plotGrid(P):
  nodeMatrix = P.nodes()
  n = np.shape(nodeMatrix)[0]
  for i in range(0,n):
    plt.plot(nodeMatrix[i][0],nodeMatrix[i][1],'bo')
    
  edgeMatrix = P.edges()
  m = np.shape(edgeMatrix)[0]
  for i in range(0,m):
    plt.plot(np.array([edgeMatrix[i][0][0],edgeMatrix[i][1][0]]), 
        np.array([edgeMatrix[i][0][1],edgeMatrix[i][1][1]]),'k') 
        #TODO: Make color map depending on 'vel'
        #TODO: Make two lanes
    
def edgeVelocity(distance, nCars, vMax, vMin):
   maxCars = distance/5
   v = (vMin-vMax)/(maxCars-maxCars/2) * (nCars - maxCars/2) + vMax
   v = np.max([vMin,np.min([v,vMax])])
   return v


#%% Initiations
vMin, vMax = 1, 50
G = nx.DiGraph(nx.grid_graph([4,4]))

for _, _, nodeData in G.edges_iter(data=True): #CodingLife #BestGroup
    nCars = rd.randint(1,50)
    distance = 200
    v = edgeVelocity(distance, nCars, vMax, vMin)
    nodeData['dist'] = distance
    nodeData['nCars'] = nCars
    nodeData['vel'] = v
    nodeData['weight'] = distance/v

for pos, data in G.nodes(data=True):
    data['pos'] = pos

#%% THE REST!

pos = nx.get_node_attributes(G,'pos')
nx.draw(G, pos)

plotGrid(G)
