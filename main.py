import numpy as np
import csv

if (__name__ == '__main__'):

	trafficData = []
	collisionData = []
	adjM = []
	nodes = []
	hospitals = []

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
		
		for row in csvreader: 
	  		hospitals.append(list(map(float, row)))

	  	hospitals = np.asarray(hospitals)

	with open('./data/2_hours/nodes.csv', 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		for row in csvreader: 
	  		nodes.append(list(map(float, row)))

	  	nodes = np.asarray(nodes)

	num_seconds, num_edges = trafficData.shape
	num_collision = collisionData.shape[0]
	num_nodes = nodes.shape[0]
	num_hospitals = hospitals.shape[0]

	collision_counter = 0
	active_collisions = [] # contains nodes for all active collision

	for t in range(num_seconds):

		while (collisionData[collision_counter, 0] == t):
			active_collisions.append(collisionData[collision_counter, 1])
			collision_counter += 1

		current_max_speeds = trafficData[t, :]

		



			
			


	