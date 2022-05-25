from hub import *

class HubRunner:
    def __init__(self):
        self.i_hub_runner = IHubRunner()
        self.or_hub_runner = OrHubRunner()
        self.and_hub_runner = AndHubRunner()
        self.root_hub_runner = RootHubRunner()

    def run(self, hub, context):
        if type(hub)==IHub:
            return self.i_hub_runner.run(hub, context)
        if type(hub)==AndHub:
            return self.and_hub_runner.run(hub, context)
        if type(hub)==OrHub:
            return self.or_hub_runner.run(hub, context)
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



class OrHubRunner:
    def run(self, hub, context):
        pass

