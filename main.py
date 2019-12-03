import math
import numpy as np
import csv
import shortest_path as sp
from functions import *

# initialize all arrays
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
num_collisions_at_that_time = 0
patients_transferred = 0
active_collisions = [] # contains nodes for all active collision
current_ambulance_locations = []
simulation_data = []

with open('./csv_files/trafficData.csv', 'r') as csvfile:
	read = csv.reader(csvfile)
	for r in read:
		trafficData.append(list(map(float, r)))
trafficData = np.asarray(trafficData)
print('traffic data', trafficData.shape)

with open('./csv_files/collisionData.csv', 'r') as csvfile: 
	read = csv.reader(csvfile) 
	for r in read: 
		collisionData.append(list(map(float, r)))
collisionData = np.asarray(collisionData)
print('collision data', collisionData.shape)

with open('./csv_files/adjM_new.csv', 'r') as csvfile: 
	read = csv.reader(csvfile) 
	for r in read: 
		adjM.append(list(map(float, r)))
adjM = np.asarray(adjM)
adjM = adjM.astype(int)
print('adjm', adjM.shape)

with open('./csv_files/hospital.csv', 'r') as csvfile: 
	read = csv.reader(csvfile) 
	count = 0
	for r in read: 
		hospitals.append(list(map(float, r)))
		count += 1
hospitals = np.transpose(np.asarray(hospitals))

with open('./csv_files/nodes.csv', 'r') as csvfile: 
	read = csv.reader(csvfile) 
	count = 0
	for r in read:
		nodes_dict[count] = r
		count += 1
		nodes.append(list(map(float, r)))
nodes = np.transpose(np.asarray(nodes))

with open('./csv_files/edges_new.csv', 'r') as csvfile: 
	read = csv.reader(csvfile) 
	count = 0
	for r in read:
		edges_dict[(list(map(int, r))[0], list(map(int, r))[1])] = count
		count += 1
		edges.append(list(map(float, r)))
edges = np.asarray(edges)

number_of_seconds, number_of_edges = trafficData.shape
number_of_collision = collisionData.shape[0]
number_of_nodes = nodes.shape[0]
number_of_ambulances = hospitals.shape[0]
number_of_hospitals = number_of_ambulances

# this is for making adj matrix consistent with the edges file
hospital_connections = np.ones((number_of_seconds, 27)) * 20
updatedTrafficData = np.concatenate((trafficData, hospital_connections), axis=1)
nodes_all = np.concatenate((nodes, hospitals), axis=0)

# initialising the ambulance locations
for i in range(number_of_hospitals):
	current_ambulance_locations.append([hospitals[i, 0], hospitals[i, 1]])

ambulances_occupied = np.zeros((number_of_hospitals))
num_patients_hospitals = np.zeros((number_of_hospitals))

# dict for storing the number of patients currently each hospital has
hospital_ambulance_dict = {100: 0, 101: 1, 102: 2, 103: 3, 104: 4}

# how much time has passed for each patient as we have release each 
hospital_allocation_timings = {100: [], 101: [], 102: [], 103: [], 104: []}

# dict for storing all patients (nodes where accidents took place) for each hospital
ambulance_casualty_dict = {0: [], 1: [], 2: [], 3: [], 4: []}
ambulance_availability = [0]*number_of_ambulances

hospital_vacancy = [0]*number_of_hospitals

for t in range(number_of_seconds):
	while (collisionData[num_collisions_at_that_time, 0] == t):
		active_collisions.append(collisionData[num_collisions_at_that_time, 1])
		num_collisions_at_that_time += 1
	current_max_speeds = updatedTrafficData[t, :] # max speed of all edges at time t

	# constructing the graph using all the edges and nodes provided
	g = sp.Graph(number_of_nodes + number_of_hospitals)

	for i1 in range(number_of_nodes + number_of_hospitals):
		for j1 in range(number_of_nodes + number_of_hospitals):
			if ((adjM[i1, j1] == 1) and (i1!=j1)):
				speed = updatedTrafficData[t, edges_dict[(i1, j1)]-1]
				distance = distance_between_nodes(i1, j1)
				time = distance / speed
				g.addEdge(i1, j1, time)
	for some_num in ambulance_casualty_dict.keys():
		for some_num1 in ambulance_casualty_dict[some_num]:
			if(t >= some_num1[2]):
				ambulance_casualty_dict[some_num].remove(some_num1)
	for some_num in hospital_allocation_timings.keys():
		for some_num1 in hospital_allocation_timings[some_num]:
			if(t >= some_num1):
				hospital_vacancy[some_num - number_of_nodes] -= 1
				hospital_allocation_timings[some_num].remove(some_num1)

	# we iterate over all active collisions in order to assign them corresponding ambulances
	trajectory_ambulance = []
	
	for ac in active_collisions:

		# node at which the accident has occurred at
		active_node = (int)(ac)

		# using shortest path from a source algorithm
		ac_distances, p = np.asarray(g.BellmanFord(active_node))

		hospital_distances_list = ac_distances[number_of_nodes:]
		nearest_hospital = number_of_nodes + np.argmin(ac_distances[number_of_nodes:]) 
		# finding the nearest hospital from distance list
		
		assigned_ambulance = hospital_ambulance_dict[nearest_hospital]

		# this path is the set of all nodes that are traversed to reach casualty and then to hospital
		path = generate_path(p, np.argmin(ac_distances[number_of_nodes:]), active_node)

		# this temp variable depicts if the accident is currently alloted or not
		if (ambulance_availability[assigned_ambulance] == 0):
			temp = 1 
		else:
			temp = 0

		# initially filling infinity at all edges
		min_dist = float('inf') 
		min_dist_index = -1

		# if accident is unassigned
		if (temp == 0):
			while(ambulance_availability[assigned_ambulance] != 0):
				for hos in range(number_of_hospitals):
					if(hospital_distances_list[hos] < min_dist and ambulance_availability[hos] == 0 and hospital_vacancy[ho] < 10):
						min_dist = hospital_distances_list[hos]
						min_dist_index = hos
						assigned_ambulance = hos
						temp = 1
				# break if we have assigned it
				break

		# if accident is assigned 
		else:
			ambulance_availability[assigned_ambulance] = 1
			hospital_vacancy[nearest_hospital - number_of_nodes] += 1 # 
			hospital_allocation_timings[nearest_hospital].append(t + 1800) # 1800 is the time required for treating a patient
			time_required_to_drop_patient = 2 * ac_distances[nearest_hospital] # two times as the path between hospital to casualty is same as casualty to hospital
			ambulance_casualty_dict[assigned_ambulance].append([active_node, t, t+time_required_to_drop_patient])
			simulation_data.append([t, path, active_collisions])
			
			# this is removed only when we have picked up the patient 
			active_collisions.remove(ac)
			patients_transferred += 1

		# this path is for simulation - contains path that ambulance followed and all active accidents
		trajectory_ambulance.append([active_node, assigned_ambulance, path])

	if(time == 50000):
		break
