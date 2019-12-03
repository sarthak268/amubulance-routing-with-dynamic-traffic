import math
import numpy as np
import csv
import shortest_path as sp

def distance_between_nodes(n1, n2):
	node1 = nodes_all[n1, :]
	node2 = nodes_all[n2, :]
	return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def generate_path(parent_nodes, minimum_node, source_node):
	curr_node = (int)(minimum_node)
	route = []
	while(parent_nodes[curr_node]!=source_node):
		route.append((int)(parent_nodes[curr_node]))
		curr_node = (int)(parent_nodes[curr_node])
	route.append((int)(parent_nodes[curr_node]))
	return route
