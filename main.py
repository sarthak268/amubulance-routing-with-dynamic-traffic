import numpy as np
import csv
import bellman_ford as bf

class Patient:
	def __init__(self):
		self.total_time_to_elapse = patient_time_to_elapse
		self.casualty_begin_time = -1

class Ambulance:
	def __init__(self):
		self.x = -1
		self.y = -1

	def set_location(x, y):
		self.x = x
		self.y = y

class Hospitals:
	def __init__(self, max_capacity):
		self.max_capacity = max_capacity
		self.current_capacity = max_capacity
		self.node = -1
		self.x = -1
		self.y = -1

	def set_node(x):
		self.node = x

	def set_location(x, y):
		self.x = x
		self.y = y

def distance_between_nodes(node1, node2):
	return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

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
	patient_time_to_elapse = 2400 #seconds

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
	  		h = Hospitals(max_patient_hospital_capacity)
	  		h.set_location((float)(row[0]), (float)(row[1]))
	  		h.set_node(100+count)
	  		hospitals.append(h)
	  		count += 1
	  	
	with open('./data/2_hours/nodes.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		count = 0
		for row in csvreader:
			nodes_dict[count] = row
			all_nodes_dict[((float)(row[0]), (float)(row[1]))] = count
			count += 1
	  		nodes.append(list(map(float, row)))
	  	nodes = np.asarray(nodes)

	with open('./data/2_hours/edges.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		count = 0
		for row in csvreader:
			edges_dict[((float)(row[0]), (float)(row[1]))] = count
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
		print('Time Step: ', t)
		while (collisionData[collision_counter, 0] == t):
			active_collisions.append(collisionData[collision_counter, 1])
			collision_counter += 1
			if(collision_counter == num_collision):
				break

		current_max_speeds = trafficData[t, :] # max speed of all edges at time t
		g = bf.Graph(num_nodes + num_hospitals)
		for i1 in range(num_nodes + num_hospitals):
			for j1 in range(num_nodes + num_hospitals):
				if(adjM[i1, j1] == 1) and i1!=j1:
					if([i1, j1] in edges_dict.keys()): ##### check for this condition
						speed = trafficData[t, edges_dict[i1, j1]]
						distance = distance_between_nodes(i1, j1)
						time = distance / speed
						g.addEdge(i1, j1, time)

		sum_all_ambulances = []
		for a in range(len(current_ambulance_locations)):
			a_node = all_nodes_dict[(current_ambulance_locations[a][0], current_ambulance_locations[a][1])]
			a_distances = g.BellmanFord(a_node) # ambulance to casualty
			total_sum_a = []
			hospital_for_each_collision = []
			for ac in range(len(active_collisions)):
				ac_distances = g.BellmanFord(active_collisions[ac]) # casualty to hospital
				for h in range(num_nodes, num_nodes + num_hospitals):
					total_sum_a.append(a_distances[(int)(active_collisions[ac])] + ac_distances[h])
					# calculate the sum of the distances here
			sum_all_ambulances.append(np.asarray(total_sum_a))

		# naive approach
		assigned_accidents = []
		for s in sum_all_ambulances:
			min_time, casualty_index = np.min(s), np.argmin(s)
 			if (not (casualty_index in assigned_accidents)):
 				assigned_accidents.append(casualty_index)
 			else:
 				s_copy = s.copy()
 				while (casualty_index in assigned_accidents):
 					s_copy.pop(casualty_index)
 					min_time, casualty_index = np.min(s_copy), np.argmin(s_copy)
 				assigned_accidents.append(casualty_index)


