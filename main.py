import numpy as np
import csv
import bellman_ford as bf

if (__name__ == '__main__'):

	trafficData = []
	collisionData = []
	adjM = []
	nodes = []
	edges = []
	nodes_dict = {}
	edges_dict = {}
	hospitals = []
	all_nodes_dict = {}

	treatment_time = 1800 # seconds
	max_patient_hospital_capacity = 10

	with open('./data/2_hours/trafficData.csv', 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		
		for row in csvreader:
	  		trafficData.append(list(map(float, row)))

	  	trafficData = np.asarray(trafficData)

	with open('./data/2_hours/collisionData.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		for row in csvreader: 
	  		collisionData.append(list(map(float, row)))

	  	collisionData = np.asarray(collisionData)

	with open('./data/2_hours/adjM.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		for row in csvreader: 
	  		adjM.append(list(map(float, row)))

	  	adjM = np.asarray(adjM)

	with open('./data/2_hours/hospital.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		count = 0
		for row in csvreader: 
	  		hospitals.append(list(map(float, row)))
	  		all_nodes_dict[(row[0], row[1])] = 100 + count
	  		count += 1

	  	hospitals = np.asarray(hospitals)

	with open('./data/2_hours/nodes.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		count = 0
		for row in csvreader:
			nodes_dict[count] = row
			all_nodes_dict[(row[0], row[1])] = count
			count += 1
	  		nodes.append(list(map(float, row)))
	  	nodes = np.asarray(nodes)

	with open('./data/2_hours/edges.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		count = 0
		for row in csvreader:
			edges_dict[(row[0], row[1])] = count
			count += 1
	  		edges.append(list(map(float, row)))
	  	edges = np.asarray(edges)

	num_seconds, num_edges = trafficData.shape
	num_collision = collisionData.shape[0]
	num_nodes = nodes.shape[0]
	num_hospitals = hospitals.shape[0]

	collision_counter = 0
	active_collisions = [] # contains nodes for all active collision

	current_ambulance_locations = []

	# initialising the ambulance locations
	for i in range(num_hospitals):
		current_ambulance_locations.append([hospitals[i, 0], hospitals[i, 1]])
	
	for t in range(num_seconds):
		while (collisionData[collision_counter, 0] == t):
			active_collisions.append(collisionData[collision_counter, 1])
			collision_counter += 1

		current_max_speeds = trafficData[t, :] # max speed of all edges at time t
		g = bf.Graph(num_nodes + num_hospitals)
		for i1 in range(num_nodes + num_hospitals):
			for j1 in range(num_nodes + num_hospitals):
				if(adjM[i1, j1] == 1):
					weight = trafficData[t, edges_dict[i1, j1]]
					g.addEdge(i1, j1, weight)

		for a in range(len(current_ambulance_locations)):
			a_node = all_nodes_dict[current_ambulance_locations[a]]
			a_distances = g.BellmanFord(a_node) # ambulance to casualty
			print(len(a_distances))
			for ac in range(len(active_collisions)):
				ac_distances = g.BellmanFord(active_collisions[ac]) # casualty to hospital
 				print(len(ac_distances))

		for c in range(len(active_collision)):
			casualty = active_collisions[c] # node of collision
			# d = distance_from_list(casualty)