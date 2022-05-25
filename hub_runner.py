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
        if type(hub)==RootHub:
            return self.root_hub_runner.run(hub, context)
        assert False, "prop err: unknown type of hub"

class IHubRunner:
    def run(self, hub, context):
        pass

class AndHubRunner:
    def run(self, hub, context):
        pass

class OrHubRunner:
    def run(self, hub, context):
        pass

class RootHubRunner:
    def run(self, hub, context):
        pass