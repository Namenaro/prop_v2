from hub import *

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
                                                    ID=context.get_id(),
                                                    SUPER_ID=context.get_id(),
                                                    condition=hub.condition)
        return hub.child

class IHubRunner:
    def run(self, hub, context):
        survived_points = hub.signa.run(hub.condition.points, context.pic)
        if len(survived_points) == 0:
            return None
        exemplars = points_to_exemplars(hub.signa.new_eid, survived_points)
        hub.parent.set_input_exemplars(exemplars=exemplars, sender=hub)
        return hub.parent


class AndHubRunner:
    def run(self, hub, context):
        # 1) В узел заходит условие
        if self.input_exs_obj is None:
            next_hub = self._propagate_condition(hub, context)
            return next_hub
        # 2) в узел пришли экземпляры от ребенка
        next_hub = self._propagate_exemplars(hub, context)
        return next_hub

    def _propagate_condition(self, hub, context):
        assert hub.child_left is None and hub.child_right is None, "prop err: child of and-hub must not exist! but exists"
        # смотрим, какого ребенка надо создать, создаем его и передаем ему управление
        if hub.condition.eid in hub.signa.map1.keys():  # надо левого
            hub.main_conditioning_child_is_left = True
            hub.child_left = context.create_hub_by_condition(parent=hub,
                                                             SUPER_ID=hub.child_left_SUPER_ID,
                                                             condition=hub.condition)
            return self.child_left
        # надо правого
        hub.main_conditioning_child_is_left = False
        hub.child_right = context.create_hub_by_condition(parent=hub,
                                                           SUPER_ID=hub.child_right_SUPER_ID,
                                                           condition=hub.condition)
        return hub.child_right

    def _propagate_exemplars(self, hub, context):
        #  В узел пришли экземпляры (положились в  self.input_exs_obj).
        #  Они могли придти справа или слева.
        if hub.input_exs_obj.sender.SUPER_ID == hub.child_left_SUPER_ID:
            next_hub = hub._propagate_exemplars_from_left(hub, context)
            return next_hub
        assert hub.input_exs_obj.sender.SUPER_ID == self.child_right.SUPER_ID, "prop err: super_id of child wrong"
        next_hub = hub._propagate_exemplars_from_right(hub, context)
        return next_hub

    def _propagate_exemplars_from_right(self, hub, context):
        #  1) продолжается старый росток (т.е.в И-узел снизу зашел тот же росток,
        #  что когда-то его создал, идя сверху)
        if hub.input_exs_obj.sender.ID == hub.child_right.ID:
            hub.child_right_exemplars = deepcopy(hub.input_exs_obj.exemplars)
            if hub.child_left_exemplars is not None:  # все есть для попытки запуска себя!
                assert hub.main_conditioning_child_is_left is True, "prop err: main child must be left"
                exemplars = hub.signa.run(left_pre_exemplars=hub.child_left_exemplars,
                                           right_pre_exemplars=hub.child_right_exemplars)
                if exemplars is None:
                    return None  # провал на узле (росток умер)
                hub.parent.set_input_exemplars(exemplars, sender=hub)
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
        new_left_eid = hub.signa.get_new_eid_left()
        condition = Condition(new_left_eid, list(left_points))
        child = context.create_hub(parent=hub,
                                   SUPER_ID=hub.child_left_SUPER_ID,
                                   condition=condition)
        return child

    def _create_right_child_by_left_exemplars(self, hub, context):
        left_points = extract_cloud_from_exemplars_list_by_eid(hub.signa.pre_eid_left, hub.child_left_exemplars)
        right_points = hub.signa.get_right_cloud_by_left_cloud(left_points)
        new_right_eid = hub.signa.get_new_eid_right()
        condition = Condition(new_right_eid, list(right_points))
        child = context.create_hub(parent=hub,
                                   SUPER_ID=hub.child_right_SUPER_ID,
                                   condition=condition)
        return child




class OrRwHubRunner:
    def run(self, hub, context):
        pass

