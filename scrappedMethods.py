



def plotGrid1(P):
  pos = nx.get_node_attributes(G,'pos')
  nx.draw_networkx_nodes(P,pos)
  
  nodeMatrix = P.nodes()
  n = np.shape(nodeMatrix)[0]
  for i in range(0,n):
    plt.plot(nodeMatrix[i][0],nodeMatrix[i][1],'bo')
  
  edgeMatrix = P.edges()
  m = np.shape(edgeMatrix)[0]
  for i in range(0,m):
    
    dify = 0.05*(edgeMatrix[i][0][0] < edgeMatrix[i][1][0])-0.025
    difx = 0.05*(edgeMatrix[i][0][1] < edgeMatrix[i][1][1])-0.025
    
    plt.plot(np.array([edgeMatrix[i][0][0] + difx, edgeMatrix[i][1][0] + difx]), 
        np.array([edgeMatrix[i][0][1] + dify, edgeMatrix[i][1][1] + dify]),'k') 
        #TODO: Make color map depending on 'vel'
        #TODO: Make it prety, Don't know if the way i chose is any good... /benki
    nx.draw_networkx_nodes(P,pos)
    
def getEdgeColors(self):
    weights = self.G.edges(data = True)
    n = np.shape(weights)[0]
    colors = np.zeros(n)
    for i in range(0,n):
        colors[i] = weights[i][2]['nCars']
    
    return colors;

def Simulation1(nRuns):
  #t1 = np.zeros(nRuns)
  t1 = np.zeros(nRuns)
  t2 = np.zeros(nRuns)
  a = BasicTrafficModel()
  
  for i in range(0,nRuns):
    a = BasicTrafficModel()
    while not a.isDone():
      a.moveCars()
    t1[i] = a.doneCars[0]['totaltime']
    t2[i] = a.doneCars[1]['totaltime']
    print(str(i) + '/' + str(nRuns))
    
  fig = plt.figure()
  ax = fig.add_subplot(111)
  colors = ['green','red']
  plotData = np.transpose(np.vstack((t1,t2)))
  
  ax.hist(plotData,bins = 35, normed=1, histtype='bar', color=colors, 
          label = ['Global information','Local information'])
  ax.set_xlabel('time')  
  ax.legend(prop={'size': 10})
  ax.set_title('2 agent traffic simulation')
  plt.show()
  plt.savefig('/Users/beinwaubertdepuiseau/Dropbox/Kursmaterial/Simulation of Complex Systems/Project/InitialSim3.pdf', format = 'pdf', dpi = 1000)

def Simulation2(nRuns):
  #t1 = np.zeros(nRuns)
  t1 = np.zeros(nRuns)
  t2 = np.zeros(nRuns)
  a = BasicTrafficModel()
  
  for i in range(0,nRuns):
    a = BasicTrafficModel(nSimCars = 20)
    while not a.isDone():
      a.moveCars()
    t1[i] = a.doneCars[0]['totaltime']
    t2[i] = a.doneCars[1]['totaltime']
    print(str(i) + '/' + str(nRuns))
    
  fig = plt.figure()
  ax = fig.add_subplot(111)
  colors = ['green','red']
  plotData = np.transpose(np.vstack((t1,t2)))
  
  ax.hist(plotData,bins = 35, normed=1, histtype='bar', color=colors, 
          label = ['Global information','Local information'])
  ax.set_xlabel('time')  
  ax.legend(prop={'size': 10})
  ax.set_title('20 agent traffic simulation')
  plt.show()    
  plt.savefig('/Users/beinwaubertdepuiseau/Dropbox/Kursmaterial/Simulation of Complex Systems/Project/InitialSim4.pdf', format = 'pdf', dpi = 1000)
