from utils.get_pictures import get_numbers_of_type
from long_term_memory import LongTermMemory
from signatures import AndSignature, ORSignature, ISignature
from hub import *

class Context:
    def __init__(self):
        self.id = 0
        self.pic = get_numbers_of_type(3)[0]
        self.ltm = LongTermMemory()
        self.buds = []

    def add_buds(self, buds):
        self.buds = self.buds + buds

    def get_next_bud(self):
        if len(self.buds)==0:
            return None
        return self.buds.pop()

    def get_id(self):
        if self.id == 0:
            return 0
        else:
            self.id += 1
        return self.id

    def create_hub(self, parent, SUPER_ID, condition):
        signa = self.ltm.get_program_signature_by_eid(eid=condition.eid)
        ID = self.get_id()
        if type(signa) == ISignature:
            new_hub = IHub(signa, parent, condition, ID, SUPER_ID=SUPER_ID)
        else:
            if type(signa) == AndSignature:
                new_hub = IHub(signa, parent, condition, ID, SUPER_ID=SUPER_ID)
            else:
                if type(signa) == ORSignature:
                    or_rw_hubs = _create_or_rw_hubs(signa, parent, condition, SUPER_ID=SUPER_ID)
                    new_hub = or_rw_hubs.pop()
                    self.add_buds(or_rw_hubs)
        return new_hub