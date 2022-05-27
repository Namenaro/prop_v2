from utils.get_pictures import *
from utils.point import Point
from prop import get_exemplars_by_condition
from draw import draw_exeplars_to_html
from prop_context import Context
from long_term_memory import LongTermMemory
from cognitive_map import CognitiveMap
from undirected_prop import undirected_prop_from_point
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

def exp1(): # test directed prop
    #show_hardcoded_examples()
    pic = get_numbers_of_type(3)[0]
    ltm = LongTermMemory()
    cog_map = CognitiveMap()
    context = Context(cog_map, ltm, pic)
    #points = [Point(13, 15)] # for eid=2 (Simple AND)
    points = [Point(13, 15), Point(14, 15)] # for eid=6 (2 AND conneced by AND )
    #points = [Point(14, 22), Point(12, 22)]# for eid=19 (OR between 2 ANDs)
    #points = [Point(0, 0), Point(1, 0)]# for eid=19 (fail)
    exemplars = get_exemplars_by_condition(eid=6, points=points, context=context)
    print("Result exemplars are " + str(exemplars))
    draw_exeplars_to_html(pic=pic, exemplars=exemplars, name="result",one_ax=False)
    cog_map.draw(pic)

def exp2():# test undirected prop
    pic = get_numbers_of_type(3)[0]
    ltm = LongTermMemory()
    cog_map = CognitiveMap()
    context = Context(cog_map, ltm, pic)
    point = Point(13, 15)
    undirected_prop_from_point(point, context)
    cog_map.draw(pic)

#exp1()
exp2()


