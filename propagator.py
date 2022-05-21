from globals import GLOBAL
from prog_exemplar import ProgExemplar
from prop_utils import *

class Condition:
    def __init__(self, eid, points):
        self.eid = eid
        self.points = points

class InputExs:
    def __init__(self, sender_id, sender_super_id, exemplars):
        self.sender_id = sender_id
        self.exemplars = exemplars
        self.sender_super_id = sender_super_id

def make_propagation(condition):
    grower = Grower(condition)
    exemplars = grower.grow()
    return exemplars

class Hub:
    def __init__(self, signa, parent, condition, SUPER_ID):
        self.ID = GLOBAL.hub_id_gen.get_id()
        self.SUPER_ID = SUPER_ID
        self.signa = signa
        self.parent = parent  # всегда один родитель
        self.condition = condition

class IHub(Hub):
    def __init__(self, signa, parent, condition, SUPER_ID):
        Hub.__init__(signa, parent, condition, SUPER_ID)

    def run(self):  # return next_hub or None if failed
        survived_points = self.signa.run(self.condition.points, GLOBAL.pic)
        if len(survived_points) == 0:
            return None
        exemplars = points_to_exemplars(self.signa.new_eid, survived_points)
        self.parent.set_exemplars_from_child(exemplars, child_id=self.ID, child_super_id=self.SUPER_ID)
        return self.parent


class Grower:
    def __init__(self, condition):
        self.active_buds=[]
        self.current_hub = None
        self.root_hub = None
        self.init_root_hub()

    def init_root_hub(self):
        pass


    def grow(self):
        while True:
            preffered_hub = self.current_hub.run()
            if self.root_hub.result_exemplars is not None:
                return self.root_hub.result_exemplars  # получили экземпляры на корневом узле, это успех! Выходим.
            if preffered_hub is not None:
                self.current_hub = preffered_hub
            else:
                if len(self.active_or_hubs) > 0:
                    self.current_hub = self.active_or_hubs[0]
                else:
                    return [] # все возможности кончились, возвращаем неудачу


class AndHub(Hub):
    def __init__(self, signa, parent, condition, SUPER_ID):
        Hub.__init__(signa, parent, condition, SUPER_ID)
        self.child_left = None
        self.child_right = None
        self.child_left_exemplars = None
        self.child_right_exemplars = None

        self.input_exs_obj = None


    def set_input_exemplars(self, exemplars, child_id, child_super_id):
        self.input_exs_obj = InputExs(child_id, child_super_id, exemplars)

    def _propagate_condition(self):# В узел заходит активирующее его условие
        assert self.child_left is None and self.child_right is None, "prop err: child must not exist! but exists"
        # смотрим, какого ребенка надо создать, создаем его и передаем ему управление
        # запоминаем, был он правый или левый
        return child

    def _propagate_exemplars(self):#  В узел пришли экземпляры от ребенка (положились в  self.input_exs_obj)
        # если они пришли от правого ребенка,
        # и при этом под правым ребенком еще нет экземпляров, то
        # просто кладем их под правого ребенка, создаем левого ребенка, передаем ему управление

        #если под правым уже есть экземпляры, делаем копию себя , очищаем



    def run(self): # разные варианты прохождения активности по узлу:
        # 1) В узел заходит активирующее его условие
        if self.input_exemplars is None:
            next_hub = self._propagate_condition()
            return next_hub
        # 2) в узел пришли экземпляры от ребенка
        next_hub = self._propagate_exemplars()
        return next_hub


class OrHub(Hub):
    def __init__(self,signa, parent, condition, SUPER_ID):
        Hub.__init__(signa, parent, condition, SUPER_ID)
        self.alternatives_list = signa.alternatives_list # [ {eid1: eid1v1, eid2:eid2v1,...}, {eid1:eid1v2, eid2:eid2v2,...},... ]
        self.active_child = None
        self.child_result_exemplars = None

        self.input_exemplars = None

    def set_input_exemplars(self, exemplars, child_id, child_super_id):
        self.input_exemplars = InputExs(child_id, child_super_id, exemplars)

    def run(self):  # return next_hub or None if failed
        return next_hub or Fail










