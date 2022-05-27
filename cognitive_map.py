from utils.logger import HtmlLogger
from prog_exemplar import ProgExemplar
import numpy as np
import matplotlib.pyplot as plt
import math

class EidsInPoint:
    def __init__(self):
        self.eids=[]

    def add_eid(self, eid):
        self.eids.append(eid)

    def contains_eid(self, eid):
        return eid in self.eids


class CognitiveMap:
    def __init__(self):
        # ключ - Point
        # значение - EidsInPoint
        self.points_to_eids_dict = {}
        self.uniq_eids_in_situation = set()

    def add_event(self, point, eid):
        self.uniq_eids_in_situation.add(eid)
        if point not in self.points_to_eids_dict.keys():
            self.points_to_eids_dict[point]=EidsInPoint()
        self.points_to_eids_dict[point].add_eid(eid)

    def add_prog_exemplar(self,exemplar):
        for eid, point in exemplar.events_exemplars.items():
            self.add_event(point, eid)

    def add_prog_exemplars(self, exemplars):
        for exemplar in exemplars:
            self.add_prog_exemplar(exemplar)

    def get_points_for_eid(self, eid):
        points = []
        for point, eids_in_point in self.points_to_eids_dict.items():
            if eids_in_point.contains_eid(eid):
                points.append(point)
        return points

    def draw(self, pic, name="cm_result"):
        logger = HtmlLogger(name)
        MAX = 20
        num_axs = len(self.uniq_eids_in_situation)
        if num_axs==0:
            return
        logger.add_text("number of UNIQUE eid in situation = " + str(num_axs))
        num_cols = 3
        num_rows = min( math.ceil(num_axs / num_cols), math.ceil(MAX / num_cols))
        if num_rows == 1:
            num_rows = 2
        fig, axs = plt.subplots(figsize=(5 * num_cols, 5 * num_rows), nrows=num_rows, ncols=num_cols, sharex=True,
                                sharey=True)
        i = 0
        eids_list = list(self.uniq_eids_in_situation)
        for row in axs:
            for col in row:
                if i < num_axs:
                    col.imshow(pic, cmap='gray_r')
                    col.title.set_text("eid="+str(eids_list[i]))
                    points_list = self.get_points_for_eid(eids_list[i])
                    color = np.random.rand(3,)
                    for point in points_list:

                        col.scatter(point.x, point.y, s=100, c=[color], alpha=0.9)
                    i += 1
                else:
                    break
        logger.add_fig(fig)
        logger.close()





