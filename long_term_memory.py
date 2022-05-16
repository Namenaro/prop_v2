from signatures import *

import torchvision.datasets as datasets
import matplotlib.pyplot as plt
import pandas as pd
import ast
import itertools

class LongTermMemory:
    def __init__(self):
        self.eid_tab = None
        self.and_prog_tab = None
        self.i_prog_tab = None
        self.or_prog_tab = None

        self.load_tables_from_file(path='./tables.xlsx')


    def load_tables_from_file(self, path='./tables.xlsx'):
        print ("loading tables from " + path)
        self.eid_tab = pd.read_excel(path, sheet_name='ids_table',  engine='openpyxl')
        self.and_prog_tab = pd.read_excel(path, sheet_name='u_progs_table',  engine='openpyxl')
        self.i_prog_tab = pd.read_excel(path, sheet_name='i_progs_table', engine='openpyxl')
        self.or_prog_tab = pd.read_excel(path, sheet_name='or_progs_table', engine='openpyxl')

    def get_program_signature_by_eid(self, eid):
        # получим имя программы-источника этого события
        eid_rows = self.eid_tab.loc[self.eid_tab['id_name'] == eid]
        if len(eid_rows) != 1:
            return None

        source_program_name = eid_rows.iloc[0]["source"]

        # загрузим сигнатуру этой программы
        if source_program_name[0]=='a':
            rows = self.and_prog_tab[self.and_prog_tab['pr_name'] == source_program_name]

            pre_eid_left = rows.iloc[0]["id_starter"]
            pre_eid_right =rows.iloc[0]["target_id"]
            u = convert_from_str(rows.iloc[0]["u"])
            dy = u[1]
            dx = u[0]
            dactions_list = convert_from_str("[" + rows.iloc[0]["area"] + "]")
            dactions = []
            for xy in dactions_list:
                dactions.append(Point(xy[0], xy[1]))

            mapper1 =convert_from_str("[" + rows.iloc[0]["map_1"] + "]")
            map1 = {}
            for old_new in mapper1:
                old = old_new[0]
                new = old_new[1]
                map1[new] = old
            mapper2 = convert_from_str("[" + rows.iloc[0]["map_2"] + "]")
            map2 = {}
            for old_new in mapper2:
                old = old_new[0]
                new = old_new[1]
                map2[new] = old
            signature = AndSignature(source_program_name, pre_eid_left, pre_eid_right, dx, dy, dactions, map1, map2)
            return signature

        if source_program_name[0] == 'i':
            rows = self.i_prog_tab[self.i_prog_tab['pr_name'] == source_program_name]
            old_eid = None
            new_eid = 1
            steps = []
            signature = ISignature(source_program_name, old_eid, new_eid, steps)
            return signature

        if source_program_name[0] == 'o':
            rows = self.or_prog_tab[self.or_prog_tab['pr_name'] == source_program_name]
            ors_list = convert_from_str(rows.iloc[0]["OR"])
            alternatives_list = []

            num_alternatives = len(ors_list[0])-1
            for i in range(num_alternatives):
                alternative = {}
                for or_node in ors_list:
                    alternative[or_node[0]] = or_node[i+1]
                alternatives_list.append(alternative)

            signature = ORSignature(source_program_name, alternatives_list)
            return signature
        assert False, "Err: bad name for the program encountered!"


def convert_from_str(cell):
    res = ast.literal_eval(cell)
    return res

if __name__ == "__main__":
    ltm = LongTermMemory()
    signa = ltm.get_program_signature_by_eid(20)
    print (signa.__dict__)