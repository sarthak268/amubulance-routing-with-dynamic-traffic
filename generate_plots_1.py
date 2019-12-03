import matplotlib
import matplotlib.pyplot as plt

x = [5, 6, 7, 8, 9, 10]
y = [66, 65, 68, 70, 73, 74]

for i in range(len(x)):
	plt.scatter(x[i], y[i], c='k')
plt.xlabel('Total Ambulances')
plt.ylabel('Save Percentage (%)')
plt.savefig('increase_ambulances.png')