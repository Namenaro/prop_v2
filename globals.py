from utils.get_pictures import get_numbers_of_type
from long_term_memory import LongTermMemory

class HubID_Generaror:
    def __init__(self):
        self.id = None

    def get_id(self):
        if self.id is None:
            self.id =0
        else:
            self.id += 1
        return self.id


class Globals:
    def __init__(self):
        self.pic = get_numbers_of_type(3)[0]
        self.ltm = LongTermMemory()
        self.hub_id_gen = HubID_Generaror()

GLOBAL = Globals()
