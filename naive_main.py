import math
import numpy as np
import csv
import bellman_ford as bf

def distance_between_nodes(n1, n2):
	node1 = nodes_all[n1, :]
	node2 = nodes_all[n2, :]
	return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def get_path(parent_nodes, minimum_node, source_node):
	curr_node = (int)(minimum_node)
	route = []
	while(parent_nodes[curr_node]!=source_node):
		route.append((int)(parent_nodes[curr_node]))
		curr_node = (int)(parent_nodes[curr_node])
	route.append((int)(parent_nodes[curr_node]))
	return route

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
		print('traffic data', trafficData.shape)

	with open('./data/2_hours/collisionData.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		for row in csvreader: 
			collisionData.append(list(map(float, row)))

		collisionData = np.asarray(collisionData)
		print('collision data', collisionData.shape)

	with open('./data/2_hours/adjM_new.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		for row in csvreader: 
			adjM.append(list(map(float, row)))

		adjM = np.asarray(adjM)
		adjM = adjM.astype(int)
		print('adjm', adjM.shape)

	with open('./data/2_hours/hospital.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		count = 0
		for row in csvreader: 
			hospitals.append(list(map(float, row)))
			# all_nodes_dict[((float)(row[0]), (float)(row[1]))] = 100 + count
			count += 1
		hospitals = np.transpose(np.asarray(hospitals))
		print('hospitals:', hospitals.shape)
		
	with open('./data/2_hours/nodes.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		count = 0
		for row in csvreader:
			nodes_dict[count] = row
			# all_nodes_dict[((float)(row[0]), (float)(row[1]))] = count
			count += 1
			nodes.append(list(map(float, row)))
		nodes = np.transpose(np.asarray(nodes))
		print('nodes:', nodes.shape)

	with open('./data/2_hours/edges_new.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		count = 0
		for row in csvreader:
			edges_dict[(list(map(int, row))[0], list(map(int, row))[1])] = count
			count += 1
			edges.append(list(map(float, row)))
		edges = np.asarray(edges)
		print('edges', edges.shape)

	num_seconds, num_edges = trafficData.shape
	num_collision = collisionData.shape[0]
	num_nodes = nodes.shape[0]
	num_hospitals = hospitals.shape[0]
	num_ambulances = num_hospitals

	hospital_connections = np.ones((num_seconds, 27)) * 20
	updatedTrafficData = np.concatenate((trafficData, hospital_connections), axis=1)
	print('Updated traffic data', updatedTrafficData.shape)
	nodes_all = np.concatenate((nodes, hospitals), axis=0)

	collision_counter = 0
	active_collisions = [] # contains nodes for all active collision

	current_ambulance_locations = []
	simulation_data = []

	# initialising the ambulance locations
	for i in range(num_hospitals):
		current_ambulance_locations.append([hospitals[i, 0], hospitals[i, 1]])

	ambulances_occupied = np.zeros((num_hospitals))
	num_patients_hospitals = np.zeros((num_hospitals))

	hospital_ambulance_dict = {100: 0, 101: 1, 102: 2, 103: 3, 104: 4}
	ambulance_casualty_dict = {0: [], 1: [], 2: [], 3: [], 4: []}
	ambulance_availability = [0]*num_ambulances
	hospital_vacancy = [0]*num_hospitals
	hospital_allocation_timings = {100: [], 101: [], 102: [], 103: [], 104: []}

	for t in range(num_seconds):
		print('Time Step: ', t)
		print('\n')
		while (collisionData[collision_counter, 0] == t):
			active_collisions.append(collisionData[collision_counter, 1])
			collision_counter += 1
			if(collision_counter == num_collision):
				break

		current_max_speeds = updatedTrafficData[t, :] # max speed of all edges at time t
		g = bf.Graph(num_nodes + num_hospitals)
		for i1 in range(num_nodes + num_hospitals):
			for j1 in range(num_nodes + num_hospitals):
				if ((adjM[i1, j1] == 1) and (i1!=j1)):
					speed = updatedTrafficData[t, edges_dict[(i1, j1)]-1]
					distance = distance_between_nodes(i1, j1)
					time = distance / speed
					g.addEdge(i1, j1, time)

		######################################################################
		# empty ambulance as well as hospital vacancies
		for a11 in ambulance_casualty_dict.keys():
			for b11 in ambulance_casualty_dict[a11]:
				if(t>=b11[2]):
					ambulance_casualty_dict[a11].remove(b11)

		for a11 in hospital_allocation_timings.keys():
			for b11 in hospital_allocation_timings[a11]:
				if(t>=b11):
					hospital_vacancy[a11-100] -= 1
					hospital_allocation_timings[a11].remove(b11)
		# print('Hospital Vacancies: ', t, hospital_allocation_timings)
		######################################################################

		for ac in active_collisions:
			active_node = (int)(ac)
			# print('Active Node:', active_node)
			ac_distances, p = np.asarray(g.BellmanFord(active_node))
			# print('DISTANCES : ', ac_distances)
			hospital_distances_list = ac_distances[100:]
			# print('Hospital distances:', hospital_distances_list)
			nearest_hospital = 100 + np.argmin(ac_distances[100:])
			# print('Nearest hospital:', nearest_hospital)
			assigned_ambulance = hospital_ambulance_dict[nearest_hospital]
			path = get_path(p, np.argmin(ac_distances[100:]), active_node)
			# simulation_data.append([t, path, active_collisions])
			# print('assigned ambulance', assigned_ambulance)
			
			if(ambulance_availability[assigned_ambulance]==0):
				flag=1
			else:
				flag = 0
			min_dist = float('inf')
			min_dist_index = -1

			if(flag==0):
				while(ambulance_availability[assigned_ambulance]!=0):
					for aa in range(num_hospitals):
						if(hospital_distances_list[aa]<min_dist and ambulance_availability[aa]==0 and hospital_vacancy[aa]<10):
							min_dist = hospital_distances_list[aa]
							min_dist_index = aa
							assigned_ambulance = aa
							flag = 1
					break

			if(flag==1):
				ambulance_availability[assigned_ambulance] = 1
				hospital_vacancy[nearest_hospital-100] += 1
				hospital_allocation_timings[nearest_hospital].append(t+1800)
				total_time = 2*ac_distances[nearest_hospital]
				ambulance_casualty_dict[assigned_ambulance].append([active_node, t, t+total_time])
				print('Simulation data')
				print(t, path, active_collisions)
				simulation_data.append([t, path, active_collisions])
				print('Active Collisions:', active_collisions)
				print('Ambulance to casualty assignment:', ambulance_casualty_dict)
				active_collisions.remove(ac)
		if(t==200):
			break


	with open('./data/2_hours/simulation_data_2000.csv', mode='w') as employee_file:
		writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for ix in range(len(simulation_data)):
			writer.writerow([simulation_data[ix][0], simulation_data[ix][1], simulation_data[ix][2]])

