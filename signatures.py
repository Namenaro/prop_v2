from utils.get_pixels import sense
from utils.point import Point
from prog_exemplar import *

class ORSignature:
    def __init__(self, name, alternatives_list):
        self.name = name
        self.alternatives_list = alternatives_list # [ {eid1: eid1v1, eid2:eid2v1,...}, {eid1:eid1v2, eid2:eid2v2,...},... ]


class ISignature:
    def __init__(self, name, old_eid,new_eid, steps):
        self.name=name
        self.old_eid=old_eid
        self.new_eid=new_eid
        self.steps=steps

    def run(self, points, pic):
        survived_points = []
        for point in points:
            if sense(picture=pic, point=point) == 1:
               survived_points.append(point)
        return survived_points


class AndSignature: # коннектор 2 программ действием dx, dy с неопределенностьью dactions
    def __init__(self, name, pre_eid_left, pre_eid_right, dx, dy, dactions, map1, map2):
        self.name=name
        self.pre_eid_left = pre_eid_left
        self.pre_eid_right = pre_eid_right
        self.dx=dx
        self.dy=dy
        self.dactions=dactions # список точк в локальной с.к. т.е. [Point(0,0), Point(0,1),...]
        self.map1=map1#{some_new_eid1:some_old1, some_new_eid2:some_old2...}
        self.map2=map2 #{...}


    def actions_set_to_abs_coords(self,  abs_center):
        abs_actions_set = []
        for daction in self.dactions:
            absx = daction.x + abs_center.x
            absy = daction.y + abs_center.y
            abs_actions_set.append(Point(x=absx, y=absy))
        return abs_actions_set

    def run_one_ex(self, pre_left_exemplar, pre_right_exemplar):
        print(self.__dict__)
        print ("pre_left=" + str(pre_left_exemplar.__dict__))
        print("pre_right=" + str(pre_right_exemplar.__dict__))
        left_coord = pre_left_exemplar.events_exemplars[self.pre_eid_left]
        right_coord = pre_right_exemplar.events_exemplars[self.pre_eid_right]
        abs_center_of_right_compact = Point(x=left_coord.x + self.dx, y=left_coord.y+self.dy )
        possible_varians_of_right = self.actions_set_to_abs_coords(abs_center_of_right_compact)


        if right_coord in possible_varians_of_right:
            events_exemplars = {}
            # переименование точек левого контекста
            for new_eid, old_eid in self.map1.items():
                events_exemplars[new_eid]=pre_left_exemplar.events_exemplars[old_eid]

            # переименование точек правого контекста
            for new_eid, old_eid in self.map2.items():
                events_exemplars[new_eid]=pre_right_exemplar.events_exemplars[old_eid]
            result_exemplar = ProgExemplar(events_exemplars)
            return result_exemplar
        return None

    def get_right_cloud_by_left_cloud(self, left_abs_points):
        result = set()
        # теоретико-множественное ИЛИ между всеми правыми облаками для данного множества левых точек
        for left_abs_point in left_abs_points:
            right_abs_point = Point(x=left_abs_point.x+self.dx, y=left_abs_point.y+self.dy)
            right_abs_set = self.actions_set_to_abs_coords( right_abs_point)
            for p in right_abs_set:
                result.add(p)
        return result

    def get_left_cloud_by_right_cloud(self, right_abs_points):
        result = set()
        # теоретико-множественное ИЛИ между всеми левыми облаками для данного множества правых точек
        for right_abs_point in right_abs_points:
            left_abs_set = self.get_left_cloud_for_right_point(right_abs_point)
            for p in left_abs_set:
                result.add(p)
        return result

    def get_left_cloud_for_right_point(self, right_abs_point):
        result = []
        for daction in self.dactions:
            left_x = right_abs_point.x - daction.x - self.dx
            left_y = right_abs_point.y - daction.y - self.dy
            result.append(Point(x=left_x, y=left_y))
        return result

    def get_new_eid_left(self):
        for new_eid, old_eid in self.map1.items():
            if old_eid == self.pre_eid_left:
                return new_eid
        assert "Err: no left eid found in and_signa"

    def get_new_eid_right(self):
        for new_eid, old_eid in self.map2.items():
            if old_eid == self.pre_eid_right:
                return new_eid
        assert "Err: no right eid found in and_signa"

    def run(self, left_pre_exemplars, right_pre_exemplars):
        new_exemplars = []
        for pre_left in left_pre_exemplars:
            for pre_right in right_pre_exemplars:
                new_exemplar = self.run_one_ex(pre_left, pre_right)
                if new_exemplar is not None:
                    new_exemplars.append(new_exemplar)
        if len(new_exemplars)==0:
            return None
        return new_exemplars