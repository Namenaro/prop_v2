from prog_exemplar import ProgExemplar

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

def points_to_exemplars(eid, points):
    exemplars = []
    for point in points:
        exemplar = ProgExemplar({eid:point})
        exemplars.append(exemplar)
    return exemplars

