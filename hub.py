from prog_exemplar import ProgExemplar
from signatures import *
from prop_utils import *


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
        Hub.__init__(self, signa=None, parent=None, condition=None, ID=None, SUPER_ID=None)
        self.input_exs_obj = None
        self.condition = condition

    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)


class IHub(Hub):
    def __init__(self, signa, parent, condition, ID, SUPER_ID):
        Hub.__init__(self, signa, parent, condition, ID, SUPER_ID)


class AndHub(Hub):
    def __init__(self, signa, parent, condition, ID, SUPER_ID, LEFT_SUPER_ID, RIGHT_SUPER_ID):
        Hub.__init__(self, signa, parent, condition, ID, SUPER_ID)
        self.child_left = None
        self.child_left_SUPER_ID =  LEFT_SUPER_ID
        self.child_left_exemplars = None


        self.child_right = None
        self.child_right_SUPER_ID = RIGHT_SUPER_ID
        self.child_right_exemplars = None

        self.main_conditioning_child_is_left = None

        self.input_exs_obj = None


    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)


class OrRwHub(Hub):
    def __init__(self, alternative_num,  signa, parent, condition, ID, SUPER_ID):
        Hub.__init__(self, signa, parent, condition, ID, SUPER_ID)
        self.map = signa.alternatives_list[alternative_num] #  {eid1: eid1v1, eid2:eid2v1,...}
        self.child = None

        self.input_exs_obj = None

    def set_input_exemplars(self, sender, exemplars):
        self.input_exs_obj = InputExemplars(sender, exemplars)