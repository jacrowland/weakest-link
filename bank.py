class Bank():
    def __init__(self):
        self.currentValue = 0
        self.chain = [20, 50, 100, 200, 300, 450, 600, 800, 1000]
        self.chainIndex = 0

    def moveUp(self):
        if self.chainIndex < len(self.chain) - 1:
            self.chainIndex += 1

    def resetChain(self):
        self.chainIndex = 0

    def bankCurrentAmount(self):
        self.currentValue += self.chain[self.chainIndex]
        self.resetChain()

    def __str__(self):
        returnStr = "| $ " + str(self.currentValue) + " |"
        for i in range(len(self.chain)):
            if i == self.chainIndex:
                returnStr += " [" + str(self.chain[i]) + "]"
            else:
                returnStr+= " " + str(self.chain[i])
        returnStr += " | "
        return returnStr