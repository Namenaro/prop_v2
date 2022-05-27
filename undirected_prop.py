# Распознавание запускается из выборанной точки на картинке.
# Цель - распознать как можно более редкое событие, которое тут есть.
# Его резульататами являются события, обнаруженные в ходе распознавания.
# Они регистрируются в объект "когнитивная карта"


# Перед запуском считем, что набор pre_eids (которые зависимы от изображения), определен.
# Дальше надо будет поиграть с инициализацией IProgs, делая  так:
# try starter_id = pre_eid1
# .... test...
# try starter_id = pre_eid2 ...
# .... test...

from prog_exemplar import ProgExemplar
from prop import get_exemplars_by_condition

class Possibility:
    def __init__(self, point_cloud_of_eid, eid, prognames_to_start):
        self.point_cloud_of_eid=point_cloud_of_eid
        self.eid=eid
        self.prognames_to_start=prognames_to_start

    def is_fully_done(self):
        if len(self.prognames_to_start)==0:
            return True
        return False

def _exemplars_to_possibilities(exemplars):
    return possibilities

def _try_run_possibility(possibility):
    return exemplars

def _init_possibilities(point):
    return possibilities


def undirected_prop_from_point(point, context):
    # запускаем для этой точки все IProgs
    # если ни одна не вернула успех, то возвращаем неудачу
    # если хоть одна вернула успех, то работаем дальше с ней, (1)
    # но запоминаем, какие IProgs остались непротестены

    # (1)пусть IProg вернула успех. Она создала экземпляр своего события в этой точке.
    # Смотрим, какие программы она стартует (их несколько). Перебираем эти
    # программы в цикле:
    # ----Если встрречается программа ИЛИ, то применяем ее
    # и продолжаем работу с ней, а остальные запоминаем как нерассмотренные возможности.
    # -----Если встречается программа И, то для
    # ее запуска не хватает срабатывания второй ветки. Запускаем вторую
    # ветку  по условию, получаемому из положений опорной точки в экземплярах, уже имеющихся.
    # Если И смогла вернуть свои экземпляры, то продолжнам работу с ней, а
    # остальные запоминаем как нерассмотренные возможности. Цикл змкнулся.

    # Если очережная программа не срабатывает, то переключаемся на следующую возможность.
    # Если возможностей больше нет, алгоритм завершен!
    possibilities = _init_possibilities(point)
    if possibilities is None:
        return

    while True:
        if len(possibilities)==0:
            break
        possibility = possibilities[0]
        exemplars = _try_run_possibility(possibility)
        if exemplars is None:
            possibilities.pop()
        else:
            new_possibilities = _exemplars_to_possibilities(exemplars)
            if new_possibilities is not None:
                possibilities = possibilities + new_possibilities
                if possibility.is_fully_done():
                    possibilities.pop()




