from globals import GLOBAL
from prog_exemplar import ProgExemplar
from signatures import *
from prop_utils import *

from copy import deepcopy

class Condition:
    def __init__(self, eid, points):
        self.eid = eid
        self.points = points

class InputExemplars:
    def __init__(self, sender_hub, exemplars):
        self.sender = sender_hub
        self.exemplars = exemplars

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

class RootHub:
    def __init__(self, condition):
        Hub.__init__(None, None, None, None)
        self.input_exs_obj = None
        self.condition = condition

    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)

    def run(self):
        self.child = _create_hub(parent=self, SUPER_ID=GLOBAL.hub_id_gen.get_id(), condition=self.condition)
        return self.child

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



class AndHub(Hub):
    def __init__(self, signa, parent, condition, SUPER_ID):
        Hub.__init__(signa, parent, condition, SUPER_ID)
        self.child_left = None
        self.child_left_SUPER_ID =  GLOBAL.hub_id_gen.get_id()
        self.child_left_exemplars = None


        self.child_right = None
        self.child_right_SUPER_ID = GLOBAL.hub_id_gen.get_id()
        self.child_right_exemplars = None

        self.main_conditioning_child_is_left = None

        self.input_exs_obj = None


    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)


    def run(self):
        """
        Активация настроенного узла "И". Возвращается либо следующий настроенный узел
        (и тогда на него надо передать управление), либо
        None (и тогда надо перключиться в другой росток)
        :return: next_hub или None
        """
        # разные варианты прохождения активности по узлу:
        # 1) В узел заходит активирующее его условие
        if self.input_exs_obj is None:
            next_hub = self._propagate_condition()
            return next_hub
        # 2) в узел пришли экземпляры от ребенка
        next_hub = self._propagate_exemplars()
        return next_hub



    def _propagate_exemplars(self):#  В узел пришли экземпляры(положились в  self.input_exs_obj)
        # они могли придти справа или слева
        if self.input_exs_obj.sender.SUPER_ID == self.child_left_SUPER_ID:
            next_hub = self._propagate_exemplars_from_left()
            return next_hub
        assert self.input_exs_obj.sender.SUPER_ID == self.child_right.SUPER_ID, "prop err: super_id of child wrong"
        next_hub = self._propagate_exemplars_from_right()
        return next_hub

    def _propagate_exemplars_from_right(self):
        if self.input_exs_obj.sender.ID == self.child_right.ID:
        # продолжается старый росток (т.е.в И-узел снизу зашел тот же росток, что когда-то его создал, идя сверху)
            self.child_right_exemplars=deepcopy(self.input_exs_obj.exemplars)
            if self.child_left_exemplars is not None: # все есть для попытки запуска себя!
                assert self.main_conditioning_child_is_left is True, "prop err: main child must be left"
                exemplars = self.signa.run(left_pre_exemplars=self.child_left_exemplars,
                                           right_pre_exemplars=self.child_right_exemplars)
                if exemplars is None:
                    return None  # провал на узле (росток умер)
                self.parent.set_input_exemplars(self, exemplars)
                return self.parent
            else: # запуск себя невозможен ввиду отсуствия экземпляров слева
                # чтоб их (когда-нибудь) получить, создаем левого ребенка и передаем ему управление
                assert self.main_conditioning_child_is_left is False, "prop err: main child must be right"
                self.child_left = self._create_left_child_by_right_exemplars()
                del self.input_exs_obj
                self.input_exs_obj = None
                return self.child_left
        else:
        # в узел зашел какой-то новый росток, и нужно продоложить его участок по каркасу этого И-узла
            # пересоздаем И у-зел----------------------------------------------
            new_and_hub = deepcopy(self)
            new_and_hub.ID = GLOBAL.hub_id_gen.get_id()
            # настраиваем правого ребенка--------------------------------------
            new_and_hub.child_right = self.input_exs_obj.sender
            # настраиваем левого ребенка--------------------------------------
            # если  новый росток зашел из главного ребенка, то
            # ведомый ребенок должен быть в этом ростке перечсчитан:
            if self.main_conditioning_child_is_left is False:
                new_and_hub.child_left = None
                new_and_hub.child_left_exemplars = None
            return new_and_hub


    def _propagate_exemplars_from_left(self):
        if self.input_exs_obj.sender.ID == self.child_left.ID:
        # продолжается старый росток (т.е.в И-узел снизу зашел тот же росток, что когда-то его создал, идя сверху)
            self.child_left_exemplars=deepcopy(self.input_exs_obj.exemplars)
            if self.child_right_exemplars is not None: # все есть для попытки запуска себя!
                assert self.main_conditioning_child_is_left is False, "prop err: main child must be right"
                exemplars = self.signa.run(left_pre_exemplars=self.child_left_exemplars,
                                           right_pre_exemplars=self.child_right_exemplars)
                if exemplars is None:
                    return None  # провал на узле (росток умер)
                self.parent.set_input_exemplars(self, exemplars)
                return self.parent
            else: # запуск себя невозможен ввиду отсуствия экземпляров справа
                # чтоб их (когда-нибудь) получить, создаем правого ребенка и передаем ему управление
                assert self.main_conditioning_child_is_left is True, "prop err: main child must be left"
                self.child_right = self._create_right_child_by_left_exemplars()
                del self.input_exs_obj
                self.input_exs_obj = None
                return self.child_right
        else:
        # в узел зашел какой-то новый росток, и нужно продоложить его участок по каркасу этого И-узла
            # пересоздаем И у-зел----------------------------------------------
            new_and_hub = deepcopy(self)
            new_and_hub.ID = GLOBAL.hub_id_gen.get_id()
            # настраиваем левого ребенка--------------------------------------
            new_and_hub.child_left = self.input_exs_obj.sender
            # настраиваем правого ребенка--------------------------------------
            # если  новый росток зашел из главного ребенка, то
            # ведомый ребенок должен быть в этом ростке перечсчитан:
            if self.main_conditioning_child_is_left is True:
                new_and_hub.child_right = None
                new_and_hub.child_right_exemplars = None
            return new_and_hub

    def _create_left_child_by_right_exemplars(self):
        right_points = extract_cloud_from_exemplars_list_by_eid(self.signa.pre_eid_right, self.child_right_exemplars)
        left_points = self.signa.get_left_cloud_by_right_cloud(right_points)
        new_left_eid = self.signa.get_new_eid_left()
        condition = Condition(new_left_eid, list(left_points))
        child = _create_hub(parent=self, SUPER_ID=self.child_left_SUPER_ID, condition=condition)
        return child

    def _create_right_child_by_left_exemplars(self):
        left_points = extract_cloud_from_exemplars_list_by_eid(self.signa.pre_eid_left, self.child_left_exemplars)
        right_points = self.signa.get_right_cloud_by_left_cloud(left_points)
        new_right_eid = self.signa.get_new_eid_right()
        condition = Condition(new_right_eid, list(right_points))
        child = _create_hub(parent=self, SUPER_ID=self.child_right_SUPER_ID, condition=condition)
        return child

    def _propagate_condition(self):# В узел заходит активирующее его условие
        assert self.child_left is None and self.child_right is None, "prop err: child must not exist! but exists"
        # смотрим, какого ребенка надо создать, создаем его и передаем ему управление
        if self.condition.eid in self.signa.map1.keys():  # надо левого
            self.main_conditioning_child_is_left = True
            self.child_left = _create_hub(parent=self, SUPER_ID=self.child_left_SUPER_ID, condition=self.condition)
            return self.child_left
        # надо правого
        self.main_conditioning_child_is_left = False
        self.child_right = _create_hub(parent=self, SUPER_ID=self.child_right_SUPER_ID, condition=self.condition)
        return self.child_right

def _create_hub( parent, SUPER_ID, condition):
    signa = GLOBAL.ltm.get_program_signature_by_eid(eid=condition.eid)
    if type(signa) == ISignature:
        new_hub = IHub(signa,parent,condition,SUPER_ID)
    else:
        if type(signa) == AndSignature:
            new_hub = IHub(signa, parent, condition, SUPER_ID)
        else:
            if type(signa) == ORSignature:
                or_rw_hubs = _create_or_rw_hubs(signa, parent, SUPER_ID, condition)
                new_hub = or_rw_hubs.pop()
                grower.add_new_buds(or_rw_hubs) #TODO
    return new_hub

class OrRwHub(Hub):
    def __init__(self, alternative_num,  signa, parent, condition, SUPER_ID):
        Hub.__init__(signa, parent, condition, SUPER_ID)
        self.map = signa.alternatives_list[alternative_num] #  {eid1: eid1v1, eid2:eid2v1,...}
        self.child = None


        self.input_exs_obj = None

    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)

    def run(self):
        # разные варианты прохождения активности по узлу:
        # 1) В узел заходит активирующее его условие
        if self.input_exs_obj is None:
            next_hub = self._propagate_condition()
            return next_hub
        # 2) в узел пришли экземпляры от ребенка
        next_hub = self._propagate_exemplars()
        return next_hub

    def _propagate_condition(self):
        # передаем это условие ребенку
        old_eid= self.map(self.condition.eid)
        condition_for_child = Condition(old_eid, points=deepcopy(self.condition.points))
        self.child = _create_hub(parent=self, SUPER_ID=None, condition=condition_for_child)
        return self.child

    def _propagate_exemplars(self):
        if self.input_exs_obj.sender.ID == self.child.ID:
            # передаем эти эхземпляры родителю, не создавая новых ростков
            exemplars_for_parent = remap_exemplars_old_to_new(self.map,self.input_exs_obj.exemplars)
            self.parent.set_input_exemplars(sender=self, exemplars=exemplars_for_parent)
            return self.parent
        # пришло не от того, откуда ждали - прокладываем по карткасу новый кусок ростка:
        # пересоздаем себя:
        or_rw_hub = deepcopy(self)
        or_rw_hub.ID = GLOBAL.hub_id_gen.get_id()
        or_rw_hub.child = self.input_exs_obj.sender
        return or_rw_hub


def _create_or_rw_hubs(signa, parent, SUPER_ID, condition):
    or_rw_hubs = []
    for i in range(len(signa.alternatives_list)):
        new_or_rw_hub = OrRwHub(i,  signa, parent, condition, SUPER_ID)
        or_rw_hubs.append(new_or_rw_hub)
    return or_rw_hubs


class Grower:
    def __init__(self, condition):
        self.active_buds=[]
        self.root_hub = RootHub(condition)
        self.current_hub = self.root_hub


    def grow(self):
        while True:
            preffered_hub = self.current_hub.run()
            if self.root_hub.result_exemplars is not None:
                return self.root_hub.result_exemplars  # получили экземпляры на корневом узле, это успех! Выходим.
            if preffered_hub is not None:
                self.current_hub = preffered_hub
            else:
                if len(self.active_or_hubs) > 0:
                    self.current_hub = self.active_or_hubs.pop()
                else:
                    return [] # все возможности кончились, возвращаем неудачу






