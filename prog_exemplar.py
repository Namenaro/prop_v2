from utils.point import *

class ProgExemplar: # экземпляр активации программы
    def __init__(self, events_exemplars):
        assert len(events_exemplars.keys())>0, "empty prog exemplar appeared!"
        self.events_exemplars=events_exemplars # {eid->abs_coord} # какие события были обнаружены в каких абсолютных координатах


def extract_cloud_from_exemplars_list_by_eid(eid, exemplars_list):
    points_cloud = []
    for prog_exemplar in exemplars_list:
        points_cloud.append(prog_exemplar.events_exemplars[eid])
    return points_cloud

def remap_exemplar_old_to_new(map, prog_exemplar):
    new_events_exemplars = {}
    for new_eid, old_eid in map.items():
        new_events_exemplars[new_eid] = prog_exemplar.events_exemplars[old_eid]
    return ProgExemplar(new_events_exemplars)

def remap_exemplars_old_to_new(map, exemplars):
    new_exemplars = []
    for exemplar in exemplars:
        new_exemplars.append(remap_exemplar_old_to_new(map, exemplar))
    return new_exemplars