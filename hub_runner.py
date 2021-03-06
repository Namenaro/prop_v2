from hub import *

from copy import  deepcopy
from cognitive_map import CognitiveMap

class HubRunner:
    def __init__(self):
        self.i_hub_runner = IHubRunner()
        self.or_rw_hub_runner = OrRwHubRunner()
        self.and_hub_runner = AndHubRunner()
        self.root_hub_runner = RootHubRunner()

    def run(self, hub, context):
        if type(hub)==IHub:
            return self.i_hub_runner.run(hub, context)
        if type(hub)==AndHub:
            return self.and_hub_runner.run(hub, context)
        if type(hub)==OrRwHub:
            return self.or_rw_hub_runner.run(hub, context)
        if type(hub) == RootHub:
            return self.root_hub_runner.run(hub, context)
        assert False, "prop err: unknown type of hub"

class RootHubRunner:
    def run(self, hub, context):
        hub.child = context.create_hub_by_condition(parent=hub,
                                                    SUPER_ID=context.get_id(),
                                                    condition=hub.condition)
        return hub.child

class IHubRunner:
    def run(self, hub, context):
        survived_points = hub.signa.run(hub.condition.points, context.pic)
        if len(survived_points) == 0:
            return None
        exemplars = points_to_exemplars(hub.signa.new_eid, survived_points)
        hub.print()
        print("i-hub returns exemplars:" + str(len(exemplars)))
        hub.parent.set_input_exemplars(exemplars=exemplars, sender=hub)
        context.cog_map.add_prog_exemplars(exemplars)
        return hub.parent


class AndHubRunner:
    def run(self, hub, context):
        hub.print()
        # 1) В узел заходит условие
        if hub.input_exs_obj is None:
            next_hub = self._propagate_condition(hub, context)
            return next_hub
        # 2) в узел пришли экземпляры от ребенка
        assert hub.child_right is not None or hub.child_left is not None, "prop err: unexpected exemplars"
        next_hub = self._propagate_exemplars(hub, context)
        return next_hub

    def _propagate_condition(self, hub, context):
        assert hub.child_left is None and hub.child_right is None, "prop err: child of and-hub must not exist! but exists"
        # смотрим, какого ребенка надо создать, создаем его и передаем ему управление
        if hub.condition.eid in hub.signa.map1.keys():  # надо левого
            print ("and-hub creates left, left is main child")
            hub.main_conditioning_child_is_left = True
            condition_for_child = Condition(eid=hub.signa.map1[hub.condition.eid],
                                            points=deepcopy(hub.condition.points))

            hub.child_left = context.create_hub_by_condition(parent=hub,
                                                             SUPER_ID=hub.child_left_SUPER_ID,
                                                             condition=condition_for_child)

            return hub.child_left
        # надо правого

        print("and-hub creates right, right is main child")
        hub.main_conditioning_child_is_left = False
        condition_for_child = Condition(eid=hub.signa.map2[hub.condition.eid],
                                        points=deepcopy(hub.condition.points))
        hub.child_right = context.create_hub_by_condition(parent=hub,
                                                           SUPER_ID=hub.child_right_SUPER_ID,
                                                           condition=condition_for_child)
        return hub.child_right

    def _propagate_exemplars(self, hub, context):
        #  В узел пришли экземпляры (положились в  self.input_exs_obj).
        #  Они могли придти справа или слева.
        if hub.input_exs_obj.sender.SUPER_ID == hub.child_left_SUPER_ID:
            next_hub = self._propagate_exemplars_from_left(hub, context)
            return next_hub
        assert hub.input_exs_obj.sender.SUPER_ID == hub.child_right.SUPER_ID, "prop err: super_id of child wrong"
        next_hub = self._propagate_exemplars_from_right(hub, context)
        return next_hub

    def _propagate_exemplars_from_right(self, hub, context):
        print("exemplars to and-hub from right..")
        #  1) продолжается старый росток (т.е.в И-узел снизу зашел тот же росток,
        #  что когда-то его создал, идя сверху)
        if hub.input_exs_obj.sender.ID == hub.child_right.ID:
            hub.child_right_exemplars = deepcopy(hub.input_exs_obj.exemplars)
            if hub.child_left_exemplars is not None:  # все есть для попытки запуска себя!
                print ("TRY RUN and-hub")
                assert hub.main_conditioning_child_is_left is True, "prop err: main child must be left"
                exemplars = hub.signa.run(left_pre_exemplars=hub.child_left_exemplars,
                                           right_pre_exemplars=hub.child_right_exemplars)
                if exemplars is None:
                    return None  # провал на узле (росток умер)
                hub.parent.set_input_exemplars(exemplars=exemplars, sender=hub)
                context.cog_map.add_prog_exemplars(exemplars)
                return hub.parent
            else: # запуск себя невозможен ввиду отсуствия экземпляров слева
                # чтоб их (когда-нибудь) получить, создаем левого ребенка и передаем ему управление
                assert hub.main_conditioning_child_is_left is False, "prop err: main child must be right"
                hub.child_left = self._create_left_child_by_right_exemplars(hub, context)
                del hub.input_exs_obj
                hub.input_exs_obj = None
                return hub.child_left
        else:
        # 2 ) в узел зашел какой-то новый росток, и нужно продоложить
        # его участок по каркасу этого И-узла
            # пересоздаем И у-зел----------------------------------------------
            new_and_hub = deepcopy(hub)
            new_and_hub.ID = context.get_id()
            # настраиваем правого ребенка--------------------------------------
            new_and_hub.child_right = hub.input_exs_obj.sender
            # настраиваем левого ребенка--------------------------------------
            # если  новый росток зашел из главного ребенка, то
            # ведомый ребенок должен быть в этом ростке перечсчитан:
            if hub.main_conditioning_child_is_left is False:
                new_and_hub.child_left = None
                new_and_hub.child_left_exemplars = None
            return new_and_hub

    def _propagate_exemplars_from_left(self, hub, context):
        print("exemplars to and-hub from left..")
        # 1) продолжается старый росток (т.е.в И-узел снизу зашел
        # тот же росток, что когда-то его создал, идя сверху)
        if hub.input_exs_obj.sender.ID == hub.child_left.ID:
            hub.child_left_exemplars=deepcopy(hub.input_exs_obj.exemplars)
            if hub.child_right_exemplars is not None: # все есть для попытки запуска себя!
                assert hub.main_conditioning_child_is_left is False, "prop err: main child must be right"
                exemplars = hub.signa.run(left_pre_exemplars=hub.child_left_exemplars,
                                           right_pre_exemplars=hub.child_right_exemplars)
                if exemplars is None:
                    return None  # провал на узле (росток умер)
                hub.parent.set_input_exemplars(exemplars=exemplars, sender=hub)
                context.cog_map.add_prog_exemplars(exemplars)
                return hub.parent
            else: # запуск себя невозможен ввиду отсуствия экземпляров справа
                # чтоб их (когда-нибудь) получить, создаем правого ребенка и передаем ему управление
                assert hub.main_conditioning_child_is_left is True, "prop err: main child must be left"
                hub.child_right = self._create_right_child_by_left_exemplars(hub, context)
                del hub.input_exs_obj
                hub.input_exs_obj = None
                return hub.child_right
        else:
        # 2) в узел зашел какой-то новый росток, и нужно продоложить
        # его участок по каркасу этого И-узла
            # пересоздаем И у-зел----------------------------------------------
            new_and_hub = deepcopy(hub)
            new_and_hub.ID = context.get_id()
            # настраиваем левого ребенка--------------------------------------
            new_and_hub.child_left = hub.input_exs_obj.sender
            # настраиваем правого ребенка--------------------------------------
            # если  новый росток зашел из главного ребенка, то
            # ведомый ребенок должен быть в этом ростке перечсчитан:
            if hub.main_conditioning_child_is_left is True:
                new_and_hub.child_right = None
                new_and_hub.child_right_exemplars = None
            return new_and_hub

    def _create_left_child_by_right_exemplars(self, hub, context):
        right_points = extract_cloud_from_exemplars_list_by_eid(hub.signa.pre_eid_right, hub.child_right_exemplars)
        left_points = hub.signa.get_left_cloud_by_right_cloud(right_points)
        condition = Condition(hub.signa.pre_eid_left, list(left_points))
        child = context.create_hub_by_condition(parent=hub,
                                   SUPER_ID=hub.child_left_SUPER_ID,
                                   condition=condition)
        return child

    def _create_right_child_by_left_exemplars(self, hub, context):
        left_points = extract_cloud_from_exemplars_list_by_eid(hub.signa.pre_eid_left, hub.child_left_exemplars)
        right_points = hub.signa.get_right_cloud_by_left_cloud(left_points)
        condition = Condition(hub.signa.pre_eid_right, list(right_points))
        child = context.create_hub_by_condition(parent=hub,
                                   SUPER_ID=hub.child_right_SUPER_ID,
                                   condition=condition)
        return child


class OrRwHubRunner:
    def run(self, hub, context):
        hub.print()
        # разные варианты прохождения активности по узлу:
        # 1) В узел заходит активирующее его условие
        if hub.input_exs_obj is None:
            next_hub = self._propagate_condition(hub, context)
            return next_hub
        # 2) в узел пришли экземпляры от ребенка
        next_hub = self._propagate_exemplars(hub, context)
        return next_hub

    def _propagate_condition(self, hub, context):
        # передаем это условие ребенку
        old_eid = hub.map[hub.condition.eid]
        condition_for_child = Condition(old_eid, points=deepcopy(hub.condition.points))
        hub.child = context.create_hub_by_condition(parent=hub, SUPER_ID=context.get_id(),
                                        condition=condition_for_child)
        return hub.child

    def _propagate_exemplars(self, hub, context):
        if hub.input_exs_obj.sender.ID == hub.child.ID:
            # передаем эти эхземпляры родителю, не создавая новых ростков
            exemplars_for_parent = remap_exemplars_old_to_new(hub.map, hub.input_exs_obj.exemplars)
            hub.parent.set_input_exemplars(sender=hub, exemplars=exemplars_for_parent)
            context.cog_map.add_prog_exemplars(exemplars_for_parent)
            return hub.parent
        # пришло не от того, откуда ждали - прокладываем по каркасу новый кусок ростка:
        or_rw_hub = deepcopy(hub)
        or_rw_hub.ID = context.get_id()
        or_rw_hub.child = hub.input_exs_obj.sender
        return or_rw_hub

