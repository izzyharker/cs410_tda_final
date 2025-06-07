metrics = ["Name", "Price", "Chips", "Plus Mult", "Times Mult", "Money", "Retrigger", "In Hand", "Scored", "Scales", "Perishes", "Tarot", "Spectral", "Planet", "Creates", "Destroys", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "Hands", "Discards", "First Hand", "Last Hand", "Played Hand", "Hand Size", "Chance", "Copy Joker", "Spades", "Hearts", "Clubs", "Diamonds", "Boss Blind", "Glass", "Steel", "Stone", "Lucky", "Gold", "BB compatible", "Jokers", "Deck", "Blind", "Shop", "On Sell"]

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

jokers = load_jokers("jokers.csv")

def create_edge_matrix(jokers: dict):
    num_traits = len(metrics) - 1
    node_order = []

    for k in jokers:
        node_order.append(k)

    num_jokers = len(node_order)
    edge_matrix = [[0 for _ in range(num_jokers)] for _ in range(num_jokers)]

    edge_dict = {0: []}

    for i in range(num_jokers):
        for j in range(i+1, num_jokers):
            distance = hamming_distance(jokers[node_order[i]], jokers[node_order[j]])  
            if distance in edge_dict.keys():
                edge_dict[distance].append((node_order[i], node_order[j]))
            else:
                edge_dict[distance] = [(node_order[i], node_order[j])]

    return edge_dict, node_order

# jokers = {"Blueprint": [0, 1], "Gros Michel": [0, 1], "8Ball": [1, 1]}

edge_dict, joker_order = create_edge_matrix(jokers)  

with open("test.csv", "w") as f:
    for k, v in edge_dict.items():
        print(f"{k}: {v}", file=f)
f.close()