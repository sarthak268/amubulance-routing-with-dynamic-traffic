import csv
import numpy as np

# edges = []

# with open('./data/2_hours/edges.csv', 'r') as csvfile: 
#     csvreader = csv.reader(csvfile) 
    
#     for row in csvreader:
#         edges.append(list(map(float, row)))
#     edges = np.asarray(edges)

# adjM = np.zeros((105, 105))

# for i in range(edges.shape[0]):
#     adjM[(int)(edges[i, 0]), (int)(edges[i, 1])] = 1

# for i in range(105):
#     adjM[i, i] = 1

# np.savetxt("./data/2_hours/adjM_new.csv", adjM, delimiter=",")


####
adjM = []

with open('./data/2_hours/adjM_new.csv', 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
    
    for row in csvreader: 
        adjM.append(list(map(float, row)))

    adjM = np.asarray(adjM)
    adjM = adjM.astype(int)

print (adjM)
print (adjM.shape)