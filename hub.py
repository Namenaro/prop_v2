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

class Hub:
    def __init__(self, signa, parent, condition, ID, SUPER_ID):
        self.ID = ID
        self.SUPER_ID = SUPER_ID
        self.signa = signa
        self.parent = parent  # всегда один родитель
        self.condition = condition

class RootHub:
    def __init__(self, condition):
        Hub.__init__(None, None, None, None, None)
        self.input_exs_obj = None
        self.condition = condition

    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)

