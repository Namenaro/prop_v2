import numpy as np
import matplotlib.pyplot as plt

def plot_points_arrays_as_numbers(points_arrays, pic):
    fig, ax = plt.subplots()
    plt.imshow(pic, cmap='gray_r')
    for points_array in points_arrays:
        color=np.random.rand(3,)
        i=0
        for point in points_array:
            strmarker = '$' + str(i) + '$'
            plt.scatter(point.x, point.y, s=100, c=[color], marker=strmarker, alpha=0.9)
            i+=1
    return fig

def plot_points_array(ps, pic, marker=None):
    if marker is None:
        marker='P'
    fig, ax = plt.subplots()
    plt.imshow(pic, cmap='gray_r')
    for point in ps:
        ax.plot(point.x, point.y, marker=marker, markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    return fig
