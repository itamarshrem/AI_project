import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.bipartite import color


#a function that gets several lists of data and plots them
def plot_data(data, labels, title, x_label, y_label, colors=None):
    #add x axis array, with specific values. for example i want the x values to be 0.6, 0.4, 0.2, 0, and the y values will be the corresponding values in the data lists
    x = np.arange(1, len(data[0]) + 1)
    # plt.xticks(x, [0.6, 0.4, 0.2, 0]) # to run with gammas
    #plot each list of data with the corresponding label
    for i in range(len(data)):
        #if labels[i] contains the word ibef2, plot it with strips
        # if "ibef2" in labels[i]:
        #     if colors is None:
        #         plt.plot(x, data[i], label=labels[i], linestyle='dashed')
        #     else:
        #         plt.plot(x, data[i], label=labels[i], linestyle='dashed', color=colors[i])
        # else:
        if colors is None:
            plt.plot(x, data[i], label=labels[i])
        else:
            plt.plot(x, data[i], label=labels[i], color=colors[i])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if len(labels) > 1:
        # apply legend to the right of the plot
        plt.legend()


    #and save the plot to a file
    plt.savefig(title + ".png")
    plt.show()


#graph for gammmas
def graph_for_gammmas():
    vs_offensive = [71, 81, 96, 100]
    vs_defensive = [55, 72, 92, 100]
    labels = ["offensive", "defensive"]
    data = [vs_offensive, vs_defensive]
    plot_data(data, labels, "performance against baseline players", "probability to random action",
              "percentage of wins(on 100 games)")

def graph_for_depths1():
    complex_vs_offensive = [95.1, 95.2, 99.0, 99.9, 99.9, 99.9]
    ibef2_vs_offensive = [83.1, 76.5, 97.5, 81.8, 98.5, 85.2]
    labels = ["offensive vs complex", "offensive vs ibef2"]
    data = [complex_vs_offensive, ibef2_vs_offensive]
    plot_data(data, labels, "Compare complex and ibef2 heuristics vs offensive", "depth of the search tree",
              "percentage of wins (on 1000 games)")

def graph_for_depths2():
    complex_vs_defensive = [86.3, 95.5, 95.2, 98.1, 98.4, 98.8]
    ibef2_vs_defensive = [89.9, 85.7, 98.2, 92.3, 98.7, 94.5]
    labels = ["defensive vs complex", "defensive vs ibef2"]
    data = [complex_vs_defensive, ibef2_vs_defensive]
    plot_data(data, labels, "Compare complex and ibef2 heuristics vs defensive", "depth of the search tree",
              "percentage of wins (on 1000 games)")

if __name__ == '__main__':
    graph_for_depths1()
    graph_for_depths2()

