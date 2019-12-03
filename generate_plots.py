import matplotlib
import matplotlib.pyplot as plt
import numpy as np

label = [1000, 1250, 1500, 1725, 2000, 2250, 2500]
no_movies = [64.2, 63.2, 62.8, 58.2, 56.1, 49.8, 40.8]

def plot_bar_x():
    index = np.arange(len(label))
    plt.bar(index, no_movies)
    plt.xlabel('Accidents')
    plt.ylabel('% Saved')
    plt.xticks(index, label, rotation=30)
    plt.title('Effect of change in Total Deaths')
    plt.savefig('deaths.png')

plot_bar_x()
