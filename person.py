import random as random
import time

class Person():
    def __init__(self, name, age="?", city="?", occupation="?", dialogueSpeed = 0.01):
        self.name = name
        self.isEliminated = False
        self.dialogueSpeed = dialogueSpeed
        self.age = age
        self.city = city
        self.occupation = occupation

    def say(self, line, end="."):
        #print(self.name + ": " + line + end)
        print(self.name + ": ", end="")
        for char in range(len(line)):
            print(line[char], end="")
            time.sleep(self.dialogueSpeed)
        print()
    
    def __str__(self):
        return self.name

    def eliminate(self):
        self.isEliminated = True

class Host(Person):
    def __init__(self, name):
        Person.__init__(self, name, age="9999", city="Hell", occupation="Host")
        self.name = name

class Player(Person):
    def __init__(self, name, age, city, occupation):
        Person.__init__(self, name, age, city, occupation)

    def getResponse(self, responseList):
        isValidChoice = False

        while not isValidChoice:
            try:
                responseIndex = int(input()) - 1
                responseObject = responseList[responseIndex]
            except:
                isValidChoice = False
                print("Invalid choice. Enter a number.")
                #responseObject = random.choice(responseList)
            else:
                isValidChoice = True
        return responseObject

class NPC(Person):
    def __init__(self, name, age, city, occupation):
        Person.__init__(self, name, age, city, occupation)

    #TODO
    # make individual characteristics that affect the choices made
    def getResponse(self, responseList):
        time.sleep(random.randrange(1, 2))
        return random.choice(responseList)