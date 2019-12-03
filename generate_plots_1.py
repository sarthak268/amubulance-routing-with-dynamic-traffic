import matplotlib
import numpy as np
import matplotlib.pyplot as plt

label = [5, 6, 7, 8, 9, 10]
no_movies = [64.2, 63.4, 65.1, 68.2, 71.1, 73.6]

def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(label))
    plt.bar(index, no_movies)
    plt.xlabel('Ambulances')
    plt.ylabel('% Saved')
    plt.xticks(index, label, rotation=30)
    plt.title('Effect of change in Ambulances')
    plt.savefig('ambulances.png')

plot_bar_x()
