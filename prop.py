from prop_context import Context
from hub_runner import HubRunner
from hub import *

def get_exemplars_by_condition(condition):
    context = Context()
    runner = HubRunner()
    root_hub = RootHub(condition)
    current_hub = root_hub

    while True:
        preffered_hub = runner.run(current_hub, context)
        if root_hub.input_exs_obj is not None:
            return root_hub.input_exs_obj.exemplars  # получили экземпляры на корневом узле, это успех! Выходим.
        if preffered_hub is not None:
            current_hub = preffered_hub
        else:
            current_hub = context.get_next_bud()
            if current_hub is None:
                return [] # все возможности кончились, возвращаем неудачу

