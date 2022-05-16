from globals import GLOBAL

class Condition:
    def __init__(self, eid, points):
        self.eid = eid
        self.points


def make_propagation(condition):
    grower = Grower(condition)
    exemplars = grower.grow()
    return exemplars


class Grower:
    def __init__(self, condition):
        self.active_or_hubs=[] #список ссылок на ИЛИ-хабы, в которых есть хоть одна не рассмотренная альтернатива
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


class Hub:
    def __init__(self, signa, parent, condition):
        self.ID = GLOBAL.hub_id_gen.get_id()
        self.signa = signa
        self.parent = parent  # всегда один родитель
        self.condition = condition
        self.result_exemplars = None

class AndHub(Hub):
    def __init__(self, signa, parent, condition):
        Hub.__init__(signa, parent, condition)
        self.child_left = None
        self.child_right = None
        self.is_left_child_activated = None
        self.left_child_result_exemplars = []
        self.right_child_result_exemplars= []

    def set_exemplars_from_child(self,exemplars):
        pass

    def run(self):
        return next_hub or Fail

class IHub(Hub):
    def run(self):
        return next_hub or Fail


class OrHub(Hub):
    def __init__(self,signa, parent, condition):
        Hub.__init__(signa, parent, condition)
        self.alternatives_list = signa.alternatives_list # [ {eid1: eid1v1, eid2:eid2v1,...}, {eid1:eid1v2, eid2:eid2v2,...},... ]
        self.active_child = None

    def run(self):
        return next_hub or Fail










