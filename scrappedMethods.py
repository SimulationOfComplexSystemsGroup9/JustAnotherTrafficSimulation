



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