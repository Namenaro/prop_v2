import networkx as nx
import pydot
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import *

G = nx.DiGraph()

# хабы, пронумерованные уникальными (в дереве) номерами
and_nodes =[1,7,8,22]
or_nodes =[4,12,15,16,27,21]
rw_nodes = [2,3,9,10,13,14,24,25]
i_nodes = [5,11,6,17,18,19,20,30,31,23,26,28,29]

# соединяем их в граф - кого к кому крепить стрелками
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 5)
G.add_edge(3, 4)
G.add_edge(4, 7)
G.add_edge(4, 6)
G.add_edge(4, 8)
G.add_edge(8, 9)
G.add_edge(8, 10)
G.add_edge(10, 11)
G.add_edge(7, 13)
G.add_edge(7, 14)
G.add_edge(13, 12)
G.add_edge(9, 15)
G.add_edge(15, 16)
G.add_edge(15, 17)
G.add_edge(16, 18)
G.add_edge(16, 19)
G.add_edge(16, 20)
G.add_edge(14, 21)
G.add_edge(12, 22)
G.add_edge(12, 23)
G.add_edge(21, 30)
G.add_edge(21, 31)
G.add_edge(22, 24)
G.add_edge(22, 25)
G.add_edge(25, 26)
G.add_edge(24, 27)
G.add_edge(27, 28)
G.add_edge(27, 29)

# ОТРИСОВКА --------------------------------------
# стилили рисования разных типов хабов
options_and = {"edgecolors": "tab:gray", "alpha": 0.9, "node_color":"tab:red", "node_shape":'o'}
options_or = {"edgecolors": "skyblue",  "alpha": 0.9, "node_color":"skyblue", "node_shape":'v'}
options_rw = {"edgecolors": "tab:gray",  "alpha": 0.9, "node_color":"white", "node_shape":'s'}
options_i = {"edgecolors": "gray",  "alpha": 0.5, "node_color":"tab:gray", "node_shape":'o', 'linewidths':6}

# рисовка ввиде именно дерева, а не абы как
pos = pydot_layout(G, prog="dot", root=1)

# рисуем вершины
nx.draw_networkx_nodes(G, pos, nodelist=and_nodes, **options_and)
nx.draw_networkx_nodes(G, pos, nodelist=or_nodes, **options_or)
nx.draw_networkx_nodes(G, pos, nodelist=rw_nodes, **options_rw)
nx.draw_networkx_nodes(G, pos, nodelist=i_nodes, **options_i)

# рисуем стрелки
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# на всех хабах нарисуем их номера в дереве(например)
labels = {}
for hub_id in and_nodes:
    labels[hub_id]=hub_id

for hub_id in or_nodes:
    labels[hub_id]=hub_id

for hub_id in rw_nodes:
    labels[hub_id]=hub_id

for hub_id in i_nodes:
    labels[hub_id]=hub_id
nx.draw_networkx_labels(G, pos, labels, font_color="black")

plt.tight_layout()
plt.axis("off")
plt.show()