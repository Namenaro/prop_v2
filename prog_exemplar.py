from utils.point import *

class ProgExemplar: # экземпляр активации программы
    def __init__(self, events_exemplars):
        assert len(events_exemplars.keys())>0, "empty prog exemplar appeared!"
        self.events_exemplars=events_exemplars # {eid->abs_coord} # какие события были обнаружены в каких абсолютных координатах


