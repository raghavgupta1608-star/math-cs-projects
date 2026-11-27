# Blackjack - simple command line version
import random

SUITS = ["H", "D", "C", "S"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def make_deck():
    deck = []
    for s in SUITS:
        for r in RANKS:
            deck.append(r + s)
    random.shuffle(deck)
    return deck


def card_value(card):
    rank = card[:-1]
    if rank in ["J", "Q", "K"]:
        return 10
    if rank == "A":
        return 11
    return int(rank)


def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[:-1] == "A")
    # an ace counts as 1 if we would bust otherwise
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def show(hand):
    return " ".join(hand) + " (" + str(hand_value(hand)) + ")"


def play_round(money):
    while True:
        try:
            bet = int(input("Bet (you have $" + str(money) + "): "))
        except ValueError:
            print("Enter a number")
            continue
        if 0 < bet <= money:
            break
        print("Bad bet")

    deck = make_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print("Dealer shows:", dealer[0])
    print("You:", show(player))

    if hand_value(player) == 21:
        print("Blackjack!")
        return money + int(bet * 1.5)

    while hand_value(player) < 21:
        move = input("(h)it or (s)tand? ").lower()
        if move == "h":
            player.append(deck.pop())
            print("You:", show(player))
        elif move == "s":
            break

    if hand_value(player) > 21:
        print("Bust! You lose.")
        return money - bet

    print("Dealer:", show(dealer))
    while hand_value(dealer) < 17:
        dealer.append(deck.pop())
        print("Dealer draws:", show(dealer))

    p = hand_value(player)
    d = hand_value(dealer)
    if d > 21 or p > d:
        print("You win!")
        return money + bet
    elif p == d:
        print("Push.")
        return money
    print("Dealer wins.")
    return money - bet


def main():
    money = 100
    print("Welcome to Blackjack")
    while money > 0:
        money = play_round(money)
        if money <= 0:
            break
        if input("Play again? (y/n) ").lower() != "y":
            break
    print("You leave with $" + str(money))


if __name__ == "__main__":
    main()
