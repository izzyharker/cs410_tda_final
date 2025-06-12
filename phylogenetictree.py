import ete3
from ete3 import Tree, TreeStyle

metrics = ["Name", "Price", "Chips", "Plus Mult", "Times Mult", "Money", "Retrigger", "In Hand", "Scored", "Scales", "Perishes", "Tarot", "Spectral", "Planet", "Creates", "Destroys", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "Hands", "Discards", "First Hand", "Last Hand", "Played Hand", "Hand Size", "Chance", "Copy Joker", "Spades", "Hearts", "Clubs", "Diamonds", "Boss Blind", "Glass", "Steel", "Stone", "Lucky", "Gold", "BB compatible", "Jokers", "Deck", "Blind", "Shop", "On Sell"]


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.children = []
        self.parent = parent
    
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

    def __str__(self):
        rep = f""
        if self.is_leaf():
            rep += str(self.name)
        if not self.is_leaf():
            rep += "("
            for i in range(len(self.children) - 1):
                rep += str(self.children[i]) + ","
            rep += str(self.children[-1]) + ")"
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
            distance = hamming_distance(jokers[node_order[i]], jokers[node_order[j]])  
            if distance in edge_dict.keys():
                edge_dict[distance].append((node_order[i], node_order[j]))
            else:
                edge_dict[distance] = [(node_order[i], node_order[j])]

    return edge_dict, node_order

def create_tree(edges: dict, jokerlist: list):
    nodes = {name: None for name in jokerlist}
    root = None

    for el in sorted(list(edges.keys())):
        for joker_pair in edges[el]:
            set = False
            n = Node(None, None)
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

string_rep = str(root) + "root;"

t = Tree(string_rep, format=1)
ts = TreeStyle()
ts.show_leaf_name = True
# ts.mode = "c"
# ts.arc_start = -180 # 0 degrees = 3 o'clock
# ts.arc_span = 180
t.show(tree_style=ts)