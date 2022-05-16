import numpy as np
import matplotlib.pyplot as plt

def plot_graph(X, Y):
    fig, ax = plt.subplots()
    ax.plot(X,Y, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    return fig