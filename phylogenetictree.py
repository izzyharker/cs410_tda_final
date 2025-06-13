from itertools import count
from typing import Any
import os
import ete3
from ete3 import Tree, TreeStyle, faces


metrics = ["Name", "Price", "Chips", "Plus Mult", "Times Mult", "Money", "Retrigger", "In Hand", "Scored", "Scales", "Perishes", "Tarot", "Spectral", "Planet", "Creates", "Destroys", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "Hands", "Discards", "First Hand", "Last Hand", "Played Hand", "Hand Size", "Chance", "Copy Joker", "Spades", "Hearts", "Clubs", "Diamonds", "Boss Blind", "Glass", "Steel", "Stone", "Lucky", "Gold", "BB compatible", "Jokers", "Deck", "Blind", "Shop", "On Sell"]


class Node:
    def __init__(self, name, parent, branch_length = 1):
        self.name = name
        self.children = []
        self.parent = parent
        self.branch_length = branch_length
        self.weight = 0
    
    def add_child(self, newchild):
        self.children.append(newchild)
    
    def get_children(self):
        return self.children
    
    def get_leaves(self):
        leaves = []
        for c in self.children:
            if c.name is None:
                leaves += c.get_leaves()
            else:
                leaves.append(c.name)
        return leaves
    
    def set_parent(self, newparent):
        self.parent = newparent

    def is_leaf(self):
        return len(self.children) == 0
    
    def compute_weights(self):
        self.weight = 0
        if self.is_leaf():
            self.weight = 1
        if not self.is_leaf():
            for node in self.children:
                node.compute_weights()
                self.weight += node.weight

    def __str__(self):
        rep = f""
        if self.is_leaf():
            rep += str(self.name)
        if not self.is_leaf():
            rep += "("
            my_list = self.children
            my_list.sort(key = lambda x: x.branch_length)
            for i in range(len(self.children) - 1):
                # rep += str(self.children[i]) + ","
                rep += str(my_list[i]) + ","
            rep += str(my_list[-1]) + ")"
            # rep += str(self.children[-1]) + ")"
        if self.parent is not None:
            rep += ":" + str(float(self.branch_length))
        return rep

# distance metric - hamming distance
def hamming_distance(a: list, b: list) -> int:
    if len(a) != len(b):
        print("Error: vectors must be equal length")
        return 0
    distance = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            distance += 1
    return distance

def vector_distance(a: list, b: list) -> float:
    if len(a) != len(b):
        print("Error: vectors must be equal length")
        return 0
    a_total = max(sum(a), 1)
    b_total = max(sum(b), 1)
    dist = 0
    for i in range(len(a)):
        dist += (a[i]/a_total-b[i]/b_total)**2
    return dist ** 0.5

def load_jokers(filename) -> dict:
    jokers = {}

    with open(filename, "r") as jk:
        lines = jk.readlines()

        # print(lines[0])

        for line in lines[1:]:
            # print(line)
            line = line.split(",")

            name = line[0]
            traits = [int(n) if n != '' else 0 for n in line[2:]]

            jokers[name] = traits

    return jokers

def create_edges(jokers: dict):
    num_traits = len(metrics) - 1
    node_order = []

    for k in jokers:
        node_order.append(k)

    num_jokers = len(node_order)
    # edge_matrix = [[0 for _ in range(num_jokers)] for _ in range(num_jokers)]

    edge_dict = {0: []}

    for i in range(num_jokers):
        for j in range(i+1, num_jokers):
            # distance = hamming_distance(jokers[node_order[i]], jokers[node_order[j]])  
            distance = vector_distance(jokers[node_order[i]], jokers[node_order[j]])  
            if distance in edge_dict.keys():
                edge_dict[distance].append((node_order[i], node_order[j]))
            else:
                edge_dict[distance] = [(node_order[i], node_order[j])]

    return edge_dict, node_order

def create_tree(edges: dict, jokerlist: list):
    nodes = {name: None for name in jokerlist}
    root = None

    dists = sorted(list(edges.keys()))

    for idx, el in enumerate(dists):
        for joker_pair in edges[el]:
            set = False
            n = Node(None, None, dists[idx])
            # n = Node(None, None)
            # print(f"{el}: {joker_pair}")
            j0 = joker_pair[0]
            j1 = joker_pair[1]
            if nodes[j0] is not None and nodes[j0] == nodes[j1]:
                set = False
            else:
                if nodes[j0] is not None:
                    n.add_child(nodes[j0])
                    for c in nodes[j0].get_leaves():
                        nodes[c].set_parent(n)
                        nodes[c] = n
                else:
                    n.add_child(Node(j0, n))
                nodes[j0] = n

                if nodes[j1] is not None:
                    n.add_child(nodes[j1])
                    for c in nodes[j0].get_leaves():
                        nodes[c].set_parent(n)
                        nodes[c] = n
                else:
                    n.add_child(Node(j1, n))
                nodes[j1] = n
                # print(nodes)

                set = True

            if set:
                root = n

    # print(root.name, [c for c in root.children])
    # print(root)
    return root


# jokers = {"Blueprint": [0, 1], "Gros Michel": [0, 1], "8 Ball": [1, 1]}

jokers = load_jokers("jokers.csv")

edge_dict, joker_order = create_edges(jokers)  

# with open("test.csv", "w") as f:
#     for k, v in edge_dict.items():
#         print(f"{k}: {v}", file=f)
# f.close()

root = create_tree(edge_dict, list(jokers.keys()))

# string_rep = str(root) + " root;"
root.compute_weights()
string_rep = str(root) + ";"

# t = Tree(string_rep, format=1)
print(string_rep)
t = Tree(string_rep, format=1)
ts = TreeStyle()
ts.show_leaf_name = True

for leaf in t.iter_leaves():
    IMAGE_PATH = "./images/"
    # myface = faces.TextFace(leaf.name)
    # leaf.img_style["size"]=12
    # print("'" + leaf.name + "'")

    # leaf.add_face(myface, 0, "aligned")
    if not os.path.isfile(IMAGE_PATH + leaf.name + '.png'):
        print(f"ERROR, {leaf.name} is not found")
    else:
        imgface = faces.ImgFace(IMAGE_PATH + leaf.name + '.png', height=95)
        leaf.add_face(imgface, 1)
# ts.mode = "c"
# ts.arc_start = -180 # 0 degrees = 3 o'clock
# ts.arc_span = 360
# ts.orientation = 1
ts.rotation=90
ts.scale = 30
t.show(tree_style=ts)


class Simplex:
    _ids = count(0)
    def __init__(self, nodes: tuple[int, ...] = ()):
        if nodes == ():
            self.nodes = (next(self._ids),)
        else:
            self.nodes = nodes
        self.dim = len(nodes) - 1
        # self.nodes = next(self._ids)
        # if id == -1:
        #     self.id = next(self._ids)
        # self.dim = len(nodes) - 1
        # if self.dim > 0:
        #     self.nodes = nodes
        # else:
        #     self.dim = 0
        #     self.nodes = [self.id]
    def __eq__(self, sim: object) -> bool:
        if isinstance(sim, Simplex):
            return set(self.nodes) == set(sim.nodes)
        else:
            return False
    def __ne__(self, sim: object) -> bool:
        return not (self == sim)
    def __hash__(self) -> int:
        # Two hashes is to prevent simple hash equality with the early numbers
        return hash(self.nodes)
    # def boundary(self) -> Complex:
    #     return Complex({tuple(list(self.nodes[0:i] + self.nodes[i:self.dim+1] for i in range(self.dim+1)})


class Filtration:
    def __init__(self):
        self.table = []
    def len(self) -> int:
        return len(self.table)
    

class Complex:
    def __init__(self, simplices: set[Simplex]):
        self.simplices = simplices

    def __add__(self, c2: Any):
        if c2.isinstance(Filtration):
            return Complex(self.simplices^c2.simplices)
        else:
            raise ValueError("Adding together two things which aren't the same!")


def boundary(self: Simplex) -> Complex:

    for i in range(self.dim+1):
        front = list(self.nodes)[0:i]
        back = list(self.nodes)[i+1:self.dim+1]

    return Complex({Simplex(tuple(list(self.nodes)[0:i] + list(self.nodes)[i:self.dim+1])) for i in range(self.dim+1)})
setattr(Simplex, 'boundary', boundary)



def persistence_measure(filt: Filtration):
    pairs = [-1] * filt.len()