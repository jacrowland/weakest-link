class Timer():
    def __init__(self, numRounds, incrementBy = 1):
        self.max = numRounds
        self.current = 1
        self.symbol = "█ "
        self.empty = "  "
        self.incrementBy = incrementBy

    def update(self):
        if self.current < self.max:
            self.current += self.incrementBy

    def reset(self):
        self.current = 0

    def __str__(self):
        return '\n| ' + (self.symbol * self.current) + ((self.max - self.current) * self.empty) +  '|'

