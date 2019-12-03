import matplotlib
import matplotlib.pyplot as plt

x = [1000, 1250, 1500, 1725, 2000, 2250, 2500]
y = [66, 63, 61, 56, 50, 44, 37]

for i in range(len(x)):
	plt.scatter(x[i], y[i], c='k')
plt.xlabel('Total Accidents')
plt.ylabel('Save Percentage (%)')
plt.savefig('increase_deaths.png')