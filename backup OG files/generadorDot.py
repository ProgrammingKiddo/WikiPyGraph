import pydot
import os
import sys

file=open(str(sys.argv[1])+".txt","r")
g=pydot.Dot(graph_type='graph')
nodos=[]
edges=[]
i=-1
for line in file:
    origen=line.split(":")[0]
    nodo_origen=pydot.Node(origen, style='filled', fillcolor='#598de0')
    if nodo_origen not in nodos:
        nodos.append(nodo_origen)
        i=i+1
    for val in line.split(":")[1].split("/"):
        nodo=pydot.Node(val, style='filled', fillcolor='#598de0')
        if nodo not in nodos:
            nodos.append(nodo)
            i=i+1
            edge=pydot.Edge(nodos[nodos.index(nodo_origen)],nodos[i])
            edges.append(edge)
for nodo in nodos:
    g.add_node(nodo) 
for edge in edges:
    g.add_edge(edge)
g.write_png(str(sys.argv[1])+'.png')
file.close()