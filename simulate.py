from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

nodes = np.array([[0, 0], [1, 0], [2, 0], [1, 0], [0, 2], [1, 1], [2, 2], [1, 2], [2, 1]])
accidents = np.array([[1, 1], [2, 2], [2, 1]])
path1 = [[0, 0], [1, 1], [3, 3], [2, 2]]
path2 = [[0, 0], [2, 1], [3, 3]]

counter1 = 0
counter2 = 0

plt.scatter(x=nodes[:, 0], y=nodes[:, 1], c='b')

def init():
    ax.set_ylim(-1, 3)
    ax.set_xlim(-1, 3)
    return point1, point2

fig, ax = plt.subplots()
point1, = ax.plot([0], [0], 'go')
point1.set_data(0, 0)
point2, = ax.plot([0], [0], 'go')
point2.set_data(0, 0)
ax.grid()

active_accidents = accidents.copy()
 
def run(ambulance):
    plt.scatter(x=active_accidents[:, 0], y=active_accidents[:, 1])
    
    x1, y1 = path1[counter1, 0], path1[counter1, 1]
    counter1 += 1
    x2, y2 = path2[counter2, 0], path2[counter2, 1]
    counter2 += 1

    point1.set_data(x1, y1)
    point2.set_data(x2, y2)
    return point1, point2
 
ani = animation.FuncAnimation(fig, run, init_func=init, interval=1000)
plt.show()