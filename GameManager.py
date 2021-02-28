import os
import time
import random as random

from person import *
from bank import Bank
from question import Question
from timer import Timer
from RoundManager import RoundManager

class GameManager():
    def __init__(self):
        self.isGameOver = False
        self.autoContinue = False
        self.skipIntro = False
        self.contestants = []
        self.host = None
        self.narrator = None
        self.delay = 1 # seconds to delay execution when using time.sleep(delay)
        self.bank = Bank()
        self.rounds = []
        self.setup()

    """
    setup()
    This is the first phase of the game.
    This function sets up what game environment. i.e. how many players etc.
    """
    def setup(self):
        self.clearScreen()
        self.printASCIIArtFromFile("logo.txt")
        self.waitForPlayerToContinue()
        self.clearScreen()

        self.printHeader("Game Setup")

        playerName = input("Enter your name: ").strip()
        playerAge = input("Enter your age: ").strip()
        playerLocation = input("Enter where you are from: ").strip()
        playerOccupation = input("Enter your occupation: ").strip()

        if playerName == "":
            playerName = "Player"
        if playerAge == "":
            playerAge = str(random.randrange(18, 100))
        if playerLocation == "":
            playerLocation = random.choice(["London", "Perth", "Venice"])
        if playerOccupation == "":
            playerOccupation = random.choice(["Real Estate Agent", "Cleaner", "Business Person"])

        # Creates the host, players and NPC's
        self.host = Host("Anne")
        self.narrator = Person("Narrator")

        self.createPerson(playerName, playerAge, playerLocation, playerOccupation, False)
        self.createPerson("Sophie", "24", "Auckland", "Librarian", True)
        self.createPerson("Nathan", "21", "Auckland", "Drama Teacher", True)
        self.createPerson("Nicholas", "21", "Auckland", "Unemployed",True)
        self.createPerson("Izak", "21", "Auckland", "Security", True)
        self.createPerson("Lachlan", "20", "Auckland", "Pizza Chief", True)
        self.createPerson("Eli", "20", "Auckland", "Fast Food Worker", True)

        self.printHeader("Host")
        print(str(self.host))
        self.printHeader("Players")
        self.displayList(self.contestants)
        self.printHeader("Complete")
        self.waitForPlayerToContinue()
        self.clearScreen()

        # Start the game
        self.start()

    """
    createPerson()
    Create a new NPC or Player object
    """
    def createPerson(self, name, age, city, occupation, isNPC):
        if (isNPC):
            newPerson = NPC(name, age, city, occupation)
        else:
            newPerson = Player(name, age, city, occupation)
        self.contestants.append(newPerson)

    """
    introduction()
    The first part of the show. Where the game and contestants are introduced and the mechanics are explained.
    """
    def introduction(self):
        # Game overview
        self.narrator.say("In today's show our " + str(len(self.contestants)) + " contestants will win up to $10,000")
        self.narrator.say("The others will leave with nothing when voted off as the...")
        time.sleep(self.delay)
        self.printASCIIArtFromFile("logo.txt")
        self.waitForPlayerToContinue()
        self.clearScreen()
        self.host.say("Any of the " + str(len(self.contestants)) + " people in the studio here today could win up to $10,000.")
        self.host.say("They've only just met but to get the prize money they'll have to work together.")
        self.host.say("However, " + (str(len(self.contestants)-1)) + " will leave with nothing.")
        self.host.say("Round by round we lose the player voted the weakest link.")
        print()
        self.waitForPlayerToContinue()
        self.clearScreen()

        # Contestant introduction
        self.host.say("Let's meet the team...")
        print()
        for player in self.contestants:
            player.say("I'm " + player.name + ". " + player.age + " years old from " + player.city + ". And I'm a " + player.occupation)
            time.sleep(self.delay)
        print()
        self.waitForPlayerToContinue()
        self.clearScreen()

        # Banking Instructions
        self.host.say("Okay, just to remind you each round there's $1000 to be won.")
        self.host.say("The fastest way is to create a chain of nine correct answers.")

        demoBank = Bank()
        print()
        for i in range(8):
            demoBank.moveUp()
            if (i > 4):
                print(demoBank)
                print()
                time.sleep(self.delay / 8)
        self.host.say("Break the chain and you lose all the money in that chain.")
        print()
        print("Bank!")
        demoBank.bankCurrentAmount()
        print(demoBank)
        print()
        self.host.say("Bank before the question is asked and the money is safe.")
        # we start with the person who's name starts alphabetically
        print()
        self.waitForPlayerToContinue()

    """
    start()
    Controls main game execution
    1. introduction
    2. Rounds
        Regular Rounds
        Final round
    3. Game Over (ending)
    """
    def start(self):
        # 1. Introduction
        if not self.skipIntro:
            self.introduction()

        # 2. rounds begin
        while not self.isGameOver:
            self.clearScreen()
            # initialise the current round
            currentRound = RoundManager(len(self.rounds)+1, self)
            self.rounds.append(currentRound)
            currentRound.start()
            # once completed, check if that was the final round
            if len(self.getRemainingPlayers()) == 1:
                self.isGameOver = True
                winningPlayer = self.getRemainingPlayers()[0]

        # 3. Game over
        self.clearScreen()
        self.gameOver(winningPlayer)



    """
    gameOver()
    The ending of the show.
    """
    def gameOver(self, winningPlayer):
        self.host.say("Congrats " + str(winningPlayer) + " you are the strongest link.")
        self.host.say("You walk away with $" + str(self.bank.currentValue))
        self.waitForPlayerToContinue()
        self.clearScreen()
        self.host.say("Join us again for The Weakest Link.")
        self.host.say("Goodbye.")
        time.sleep(self.delay * 2)
        self.host.say(";)")


    """
    printASCIIArtFromFile()
    Takes a text file path as input and outputs the each line with a delay
    """
    def printASCIIArtFromFile(self, path):
        f = open(path)
        lines = f.readlines()
        for line in lines:
            print(line, end="")
            time.sleep(self.delay / 16)
        print()
        f.close()

    """
    printHeader()
    """
    def printHeader(self, headerText):
        print("====== " + headerText + " ======")

    """
    getRemainingContestants()
    Returns a list of all the contestants who have not been eliminated
    """
    def getRemainingPlayers(self):
        remainingContestants = []
        for contestant in self.contestants:
            if not contestant.isEliminated == True:
                remainingContestants.append(contestant)
        return remainingContestants
    """
    clearScreen()
    Clears the console screen of text
    """
    def clearScreen(self):
        os.system('cls' if os.name=='nt' else 'clear')

    """
    displayList(listToDisplay)
    Takes as input an array of strings to output in order given
    Outputs the list in the format:
    [1] ListItem1
    [2] ListItem2
    [3] ListItem3 etc.
    """
    def displayList(self, listToDisplay):
        for i in range(len(listToDisplay)):
            print(("[" + str(i+1) + "] " + str(listToDisplay[i])))

    """
    waitForPlayerToContinue()
    Pauses the game execution until the user pushes enter.
    """
    def waitForPlayerToContinue(self):
        continuePhrase = "Press enter to continue..."
        if not self.autoContinue:
            input(continuePhrase)
        else:
            print(continuePhrase)
            time.sleep(self.delay)
