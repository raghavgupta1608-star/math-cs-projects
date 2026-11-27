# Simulate how often each poker hand shows up in 5 cards
import random
from collections import Counter
from poker import make_deck, score, NAMES

N = 100000
results = Counter()
for _ in range(N):
    deck = make_deck()
    hand = deck[:5]
    results[score(hand)[0]] += 1

for cat in range(8, -1, -1):
    print(NAMES[cat].ljust(16), round(100 * results[cat] / N, 3), "%")
