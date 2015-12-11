# Imports
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import gistfile as osm
#%%
manhattan = [-74.0097,40.7430,-73.9612,40.7631]
highway_cat = 'motorway|trunk|primary|secondary|tertiary|road|residential|service|motorway_link|trunk_link|primary_link|secondary_link|teriary_link'
G = osm.read_osm(osm.download_osm(-74.0097,40.7430,-73.9612,40.7631,'motorway|trunk|primary|secondary|motorway_link|trunk_link|primary_link|secondary_link'))
#%%
pos = nx.get_node_attributes(G,'lon')
lat = nx.get_node_attributes(G,'lat')
for key in pos.keys():
    pos[key] = [pos[key], lat[key]]
    
nx.draw_networkx_edges(G ,pos, width = 3, arrows = False)