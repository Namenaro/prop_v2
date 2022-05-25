from utils.get_pictures import *
from utils.point import Point
from prop import get_exemplars_by_condition
import matplotlib.pyplot as plt


def show_hardcoded_examples():
    x = get_numbers_of_type(3)
    img = x[0]
    implot = plt.imshow(img, cmap='gray_r')
    plt.scatter([15, 17], [13, 12], c="red")
    plt.scatter([19, 20], [11, 9], c="blue")
    plt.scatter([14, 16, 18], [22, 20, 18], c="green")
    plt.scatter([14, 17], [21, 18], c="yellow")
    plt.show()

    reds = [img[13][15], img[12][17]]
    blues = [img[11][19], img[9][20]]

    greens = [img[22][14], img[20][16], img[18][18]]
    yellows = [img[21][14], img[18][17]]

def exp():
    #show_hardcoded_examples()
    #points = [Point(13, 15), Point(14, 15)] # for eid=2 (Simple AND)
    #points = [Point(13, 15), Point(14, 15)] # for eid=6 (2 AND conneced by AND )
    points = [Point(14, 22), Point(13, 22)]# for eid=19 (OR between 2 ANDs)
    exemplars = get_exemplars_by_condition(eid=19, points=points)
    print("Result exemplars are " + str(exemplars))

exp()


