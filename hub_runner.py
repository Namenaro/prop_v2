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
        hub.child = context.create_hub(parent=hub,
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
        pass

class OrHubRunner:
    def run(self, hub, context):
        pass

