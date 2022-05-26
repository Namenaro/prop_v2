from utils.point import Point
from utils.logger import HtmlLogger
from prog_exemplar import ProgExemplar

import numpy as np
import matplotlib.pyplot as plt
import math


def draw_exemplar_to_ax(exemplar, ax):
    eids_list = list(exemplar.events_exemplars.keys())

    prev_eid = eids_list[0]
    prev_point = exemplar.events_exemplars[prev_eid]

    color = np.random.rand(3, )
    strmarker = '$' + str(prev_eid) + '$'
    ax.scatter(prev_point.x, prev_point.y, s=100, c=[color], marker=strmarker, alpha=0.9)
    for i in range(1, len(eids_list)):
        next_eid = eids_list[i]
        next_point = exemplar.events_exemplars[next_eid]
        strmarker = '$' + str(next_eid) + '$'
        ax.scatter(next_point.x, next_point.y, s=100, c=[color], marker=strmarker, alpha=0.9)
        x_values = [prev_point.x, next_point.x]
        y_values = [prev_point.y, next_point.y]
        ax.plot(x_values, y_values, linestyle="--")


def draw_exeplars_to_html(pic, exemplars, name, one_ax=False):
    logger = HtmlLogger(name)
    if one_ax:
        fig, ax = plt.subplots()
        plt.imshow(pic, cmap='gray_r')
        for exemplar in exemplars:
            draw_exemplar_to_ax(exemplar, ax)
    else:
        num_axs = len(exemplars)
        num_cols = 3
        num_rows = math.ceil(num_axs/num_cols)
        fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, sharex=True, sharey=True)
        i=0
        for row in axs:
            for col in row:
                if i< num_axs:
                    col.imshow(pic, cmap='gray_r')
                    exemplar = exemplars[i]
                    draw_exemplar_to_ax(exemplar, col)
                    i+=1
                else:
                    break

    logger.add_fig(fig)
    logger.close()
