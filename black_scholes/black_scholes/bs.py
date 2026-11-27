# Black-Scholes call price, checked with a Monte Carlo simulation
import math
import random


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs_call(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)


def mc_call(S, K, T, r, sigma, n=200000):
    total = 0
    for _ in range(n):
        z = random.gauss(0, 1)
        ST = S * math.exp((r - sigma ** 2 / 2) * T + sigma * math.sqrt(T) * z)
        total += max(ST - K, 0)
    return math.exp(-r * T) * total / n


if __name__ == "__main__":
    S, K, T, r, sigma = 100, 105, 1, 0.05, 0.2
    print("Black-Scholes:", round(bs_call(S, K, T, r, sigma), 4))
    print("Monte Carlo:  ", round(mc_call(S, K, T, r, sigma), 4))
    # TODO: compare with real option prices
