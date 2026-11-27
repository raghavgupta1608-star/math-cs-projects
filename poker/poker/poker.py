# Five card draw poker vs the computer (very basic)
import random
from collections import Counter

SUITS = ["H", "D", "C", "S"]
RANKS = "23456789TJQKA"
NAMES = ["High card", "Pair", "Two pair", "Three of a kind", "Straight",
         "Flush", "Full house", "Four of a kind", "Straight flush"]


def make_deck():
    deck = [r + s for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck


def score(hand):
    """Returns (category number, tiebreak list). Bigger is better."""
    vals = sorted([RANKS.index(c[0]) for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    counts = Counter(vals)
    # sort by count then value so pairs come first
    groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    shape = [g[1] for g in groups]
    order = [g[0] for g in groups]

    flush = len(set(suits)) == 1
    straight = len(counts) == 5 and vals[0] - vals[4] == 4
    # wheel: A 2 3 4 5
    if vals == [12, 3, 2, 1, 0]:
        straight = True
        order = [3, 2, 1, 0, -1]

    if straight and flush:
        return 8, order
    if shape == [4, 1]:
        return 7, order
    if shape == [3, 2]:
        return 6, order
    if flush:
        return 5, order
    if straight:
        return 4, order
    if shape == [3, 1, 1]:
        return 3, order
    if shape == [2, 2, 1]:
        return 2, order
    if shape == [2, 1, 1, 1]:
        return 1, order
    return 0, order


def computer_discard(hand):
    # keep any card that is part of a pair or better, otherwise keep the top 2
    counts = Counter(c[0] for c in hand)
    keep = [c for c in hand if counts[c[0]] > 1]
    if not keep:
        keep = sorted(hand, key=lambda c: RANKS.index(c[0]), reverse=True)[:2]
    return [c for c in hand if c not in keep]


def main():
    deck = make_deck()
    you = [deck.pop() for _ in range(5)]
    cpu = [deck.pop() for _ in range(5)]

    print("Your hand:")
    for i, c in enumerate(you):
        print(" ", i + 1, c)
    ans = input("Which cards to throw away? (like 1 3 5, or enter for none) ")
    for n in ans.split():
        if n.isdigit() and 1 <= int(n) <= 5:
            you[int(n) - 1] = None
    you = [c for c in you if c is not None]
    while len(you) < 5:
        you.append(deck.pop())

    for c in computer_discard(cpu):
        cpu.remove(c)
        cpu.append(deck.pop())

    print("Your final hand:", " ".join(you), "-", NAMES[score(you)[0]])
    print("Computer hand:  ", " ".join(cpu), "-", NAMES[score(cpu)[0]])

    a = score(you)
    b = score(cpu)
    if a > b:
        print("You win!")
    elif a < b:
        print("Computer wins.")
    else:
        print("Tie.")


if __name__ == "__main__":
    main()
