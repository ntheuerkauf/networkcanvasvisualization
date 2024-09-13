# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:57:44 2024

@author: theue
"""

#importing neccesary packages
import os #needed to access the files
import networkx as nx #needed to create the graphs
import csv #needed to parse through the data
import re #neede to capture the interview names
import matplotlib.pyplot as plt #needed to save the graphs

fileDir = '\\\\iowa.uiowa.edu\\shared\\ResearchData\\rdss_ekutlu\\VOICELab\\Network\\layout and size graphs\\nolayoutlarge\\data'
exportDir = '\\\\iowa.uiowa.edu\\shared\\ResearchData\\rdss_ekutlu\\VOICELab\\Network\\layout and size graphs\\nolayoutlarge\\'

#File directory of the current data being used
os.chdir(fileDir)


#Creating lists of the files that house the node and edge data
nodeList = [file for file in os.listdir(os.getcwd()) if file[-24:] == "attributeList_Person.csv"]
edgeList = [file for file in os.listdir(os.getcwd()) if file[-17:] == "edgeList_know.csv"]

#Function that creates the graph for a single participant
def createNetwork(nodes,edges):
    #Initializing graph and the participant node
    G = nx.Graph()
    G.add_node('0', name= "particpant") #Nodes are named in order of their creation (otherwise known as their id) to prevent cases where two people have the same name
    positions = {'0': (0.5,0.5)} #Network canvas postion data ranges from 0 to 1 for both axis

    #Creating nodes
    with open (nodes, "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',') #Allows us to select specific attributes from the data file
        for row in reader:
            if row[0] == "nodeID": #Eliminates header row
                continue
            G.add_node(row[0], name = row[3]) #Creates the node and attaches the person's name
            G.add_edge("0", row[0]) #Adds an edge back to the particpiant
            positions[row[0]] = (float(row[4]), float(row[5])) #Collects position data
            
    #Creates edges
    with open (edges, "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == "edgeID": #Eliminates header row
                continue
            G.add_edge(row[1], row[2]) #Adds the edge



    labels = nx.get_node_attributes(G, 'name') #Collects the names
    nx.draw_networkx(G, pos=positions,arrows = None, labels=labels) #Creates the graphs with positions and names as labels, could be tweaked with to look prettier and include axis
    plt.show(block=False) #Prints graphs seperatly 
    plt.savefig(exportDir+ re.search('^[^_]+(?=_)', nodes).group() + ".png", format="PNG")
    #Above line saves the graph to a specified folder, its name should be the name of the interview
    #The current regular expression that captures the file name assumes that their is no underscore in the name, so it might need to be updated later
    
    
#Cycles through every line in the data  
for i in range(0, len(nodeList)):
    createNetwork(nodeList[i], edgeList[i])


