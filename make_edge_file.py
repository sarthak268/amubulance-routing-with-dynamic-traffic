import csv
import numpy as np

adjM = []

with open('./data/2_hours/adjM.csv', 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
    
    for row in csvreader: 
        adjM.append(list(map(float, row)))

    adjM = np.asarray(adjM)

size = adjM.shape[0]

with open('./data/2_hours/edges.csv', mode='w') as employee_file:
    writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in range(size):
        for j in range(size):
            if (adjM[i, j] == 1 and i!=j):
                writer.writerow([str(i), str(j)])
  
