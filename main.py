import math
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

	def set_location(self, x, y):
		self.x = x
		self.y = y

class Hospitals:
	def __init__(self, max_capacity):
		self.max_capacity = max_capacity
		self.current_capacity = max_capacity
		self.node = -1
		self.x = -1
		self.y = -1

	def set_node(self, x):
		self.node = x

	def set_location(self, x, y):
		self.x = x
		self.y = y

def distance_between_nodes(n1, n2):
	node1 = nodes_all[n1, :]
	node2 = nodes_all[n2, :]
	return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def find_cumilative_cost(assigment_dict, new_ambulance, new_accident, sum_all_ambulances):
	total_cost = 0
	assigment_dict[(str)(new_ambulance)].append(new_accident)

	for k in assigment_dict.keys():
		if (len(assigment_dict[k]) == 1):
			ambulance = (int)(k)
			all_hospitals = sum_all_ambulances[ambulance][5*new_accident:5*new_accident+5]
			min_hospital_distance, ind_min_hospital = min(all_hospitals), np.argmin(all_hospitals) 
			total_cost += min_hospital_distance
			return min_hospital_distance, ind_min_hospital
			# break
		# else:
	#return min_hospital_distance, ind_min_hospital

if (__name__ == '__main__'):

	trafficData = []
	collisionData = []
	adjM = []
	nodes = []
	edges = []
	nodes_dict = {}
	edges_dict = {}
	hospitals = []
	hospitals_nodes = []
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

	with open('./data/2_hours/adjM_new.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		for row in csvreader: 
			adjM.append(list(map(float, row)))

		adjM = np.asarray(adjM)
		adjM = adjM.astype(int)

	with open('./data/2_hours/hospital.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		count = 0
		for row in csvreader: 
			h = Hospitals(max_patient_hospital_capacity)
			h.set_location((float)(row[0]), (float)(row[1]))
			h.set_node(100+count)
			hospitals_nodes.append(h)
			hospitals.append(list(map(float, row)))
			all_nodes_dict[((float)(row[0]), (float)(row[1]))] = 100 + count
			count += 1
		hospitals = np.asarray(hospitals)
		
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
			edges_dict[(list(map(int, row))[0], list(map(int, row))[1])] = count
			count += 1
			edges.append(list(map(float, row)))
		edges = np.asarray(edges)

	num_seconds, num_edges = trafficData.shape
	num_collision = collisionData.shape[0]
	num_nodes = nodes.shape[0]
	num_hospitals = hospitals.shape[0]
	num_ambulances = num_hospitals

	hospital_connections = np.ones((num_seconds, 5)) * 20
	updatedTrafficData = np.concatenate((trafficData, hospital_connections), axis=1)

	nodes_all = np.concatenate((nodes, hospitals), axis=0)

	collision_counter = 0
	active_collisions = [] # contains nodes for all active collision

	current_ambulance_locations = []

	# initialising the ambulance locations
	for i in range(num_hospitals):
		current_ambulance_locations.append([hospitals[i, 0], hospitals[i, 1]])

	ambulances_occupied = np.zeros((num_hospitals))
	num_patients_hospitals = np.zeros((num_hospitals))

	for t in range(num_seconds):
		print('Time Step: ', t)
		while (collisionData[collision_counter, 0] == t):
			active_collisions.append(collisionData[collision_counter, 1])
			collision_counter += 1
			if(collision_counter == num_collision):
				break

		current_max_speeds = updatedTrafficData[t, :] # max speed of all edges at time t
		g = bf.Graph(num_nodes + num_hospitals)

		for i1 in range(num_nodes + num_hospitals):
			for j1 in range(num_nodes + num_hospitals):
				if (adjM[i1, j1] == 1) and (i1!=j1):
					speed = updatedTrafficData[t, edges_dict[(i1+1, j1+1)]]
					distance = distance_between_nodes(i1, j1)
					time = distance / speed
					g.addEdge(i1, j1, time)
		
		if(len(active_collisions)):
			sum_all_ambulances = []
			for a in range(len(current_ambulance_locations)):
				a_node = all_nodes_dict[(current_ambulance_locations[a][0], current_ambulance_locations[a][1])]
				a_distances = g.BellmanFord(a_node) # ambulance to casualty
				total_sum_a = []
				hospital_for_each_collision = []
				for f in range(len(a_distances)):
					if(a_distances[f]==float('inf')):
						a_distances[f] = 1000
				# check for hospital to hospital distances
				for ac in range(len(active_collisions)):
					ac_distances = g.BellmanFord(active_collisions[ac]) # casualty to hospital
					for f in range(len(ac_distances)):
						if(ac_distances[f]==float('inf')):
							ac_distances[f] = 1000
					for h in range(num_nodes, num_nodes + num_hospitals):
						total_sum_a.append(a_distances[(int)(active_collisions[ac])] + ac_distances[h])
				sum_all_ambulances.append(np.asarray(total_sum_a))
			
			# naive approach
			# collision_assigned_arr = []
			# hospital_assigned_arr = []

			# for s in sum_all_ambulances:
			# 	print('s', s, len(s), len(active_collisions))
			# 	num_active_collisions = len(active_collisions)
			# 	min_time, casualty_index = np.min(s), np.argmin(s)
			# 	list_new = []
			# 	for x1 in range(len(s)):
			# 		if((x1+1)%(casualty_index+1)==0):
			# 			list_new.append(s[x1])
			# 	print(list_new)
			# 	min_casualty_index = min(list_new)
			# 	assigned_collision = min_casualty_index
			# 	s_copy = s.copy()
			# 	if (not (casualty_index in hospital_assigned_arr)):
			# 		hospital_assigned_arr.append(casualty_index)
			# 		collision_assigned_arr.append(assigned_collision)
			# 	else:
			# 		while (casualty_index in hospital_assigned_arr):
			# 			s_copy[casualty_index] = float('inf')
			# 			min_time, casualty_index = np.min(s_copy), np.argmin(s_copy)
			# 		hospital_assigned_arr.append(casualty_index)
			# 		collision_assigned_arr.append(assigned_collision)
			# 		print(assigned_collision)

			# print (collision_assigned_arr, hospital_assigned_arr)

			# auction based method
			current_cost = 0
			assigned_accidents = {'0':[], '1':[], '2':[], '3':[], '4':[]}
			for a1 in assigned_accidents.keys():
				for a2 in range(len(assigned_accidents[a1])):
					if(assigned_accidents[a1][a2][1]==t):
						assigned_accidents[a1].pop[a2]

			for i1 in range(len(active_collisions)):
				find_min_diff_arr = []
				for j1 in range(num_ambulances):
					print(assigned_accidents, j1, i1, sum_all_ambulances)
					time, winning_ambulance = find_cumilative_cost(assigned_accidents, j1, i1, sum_all_ambulances)
					cost = (time) - current_cost
					find_min_diff_arr.append(cost)
				current_cost = min(find_min_diff_arr)
				ambulance_that_wins_bid = np.argmin(np.asarray(find_min_diff_arr))
				assigned_accidents[(str(ambulance_that_wins_bid))].append((i1, time, t))

			print(assigned_accidents)

		


