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

        print(lines[0])

        for line in lines[1:]:
            # print(line)
            line = line.split(",")

            name = line[0]
            traits = [int(n) if n != '' else 0 for n in line[2:]]

            jokers[name] = traits

    return jokers

jokers = load_jokers("jokers.csv")
print(jokers["Blueprint"])

def create_edges(jokers: dict):
    for k, v in jokers.items():
        # do something
        pass