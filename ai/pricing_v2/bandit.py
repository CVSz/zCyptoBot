import random


class Thompson:
    def __init__(self):
        self.alpha = [1, 1, 1]
        self.beta = [1, 1, 1]

    def select(self):
        samples = [random.betavariate(a, b) for a, b in zip(self.alpha, self.beta)]
        return samples.index(max(samples))

    def update(self, i, reward):
        if reward > 0:
            self.alpha[i] += 1
        else:
            self.beta[i] += 1
