import os
import time
from bank import Bank
import random as random
from question import Question
from timer import Timer

class RoundManager():
    def __init__(self, roundNumber, gameManager):
        self.roundNumber = roundNumber
        self.gameManager = gameManager
        self.playersInRound = gameManager.getRemainingPlayers()
        self.isFinalRound = True if len(self.playersInRound) < 3 else False
        self.currentPlayerIndex = random.randrange(0, len(self.playersInRound))
        self.activePlayer = self.playersInRound[self.currentPlayerIndex]
        self.roundLength = random.randrange(len(self.playersInRound), len(self.playersInRound) * 2) # the number of questions to ask
        self.timer = Timer(self.roundLength)
        self.questions = []
        self.currentQuestion = None
        # Sets up a dictionary to record info about player actions in the round    
        self.playerRoundInfoDict = {}  
        for player in self.playersInRound:
            self.playerRoundInfoDict[player] = {
                "numCorrectAnswers": 0,
                "numIncorrectAnswers": 0,
                "numVotesAgainst": 0
            }

    """
    start()
    Begins the round, with the pre-question preamble
    """
    def start(self):

        if self.isFinalRound:
            roundTitle = "Final Round"
        else:
            roundTitle = "Round " + str(self.roundNumber)
        self.gameManager.printHeader(roundTitle)
        print()
        self.gameManager.host.say("We now begin the round")

        # Displays number of remain players
        self.gameManager.host.say(str(len(self.playersInRound)) + " players remain")
        print()
        self.gameManager.waitForPlayerToContinue()
        time.sleep(self.gameManager.delay)
        self.gameManager.clearScreen()

        # Select the type of round to play
        if self.isFinalRound:
            self.playFinalRound()
        else:
            self.playRegularRound()

    """
    playRegularRound()

    A regular round cosists of 1. questions, 2. voting, and 3. elimination
    """
    def playRegularRound(self):
        self.gameManager.host.say("Start the clock")
        # 1. Questions
        for num in range(self.roundLength):
            #self.gameManager.printHeader("Round " + str(self.roundNumber))
            print(self.timer)
            self.timer.update()
            
            print()
            self.gameManager.host.say(str(self.activePlayer) + ".")
            print()

            # Ask's the player if they would like to bank
            self.askIfBank()

            # Ask the player a question
            self.askQuestion()
            time.sleep(self.gameManager.delay)
            print()

            # Get the player's answer and check if it is correct
            answer = self.activePlayer.getResponse(self.currentQuestion.choices)
            self.activePlayer.say(answer)
            time.sleep(self.gameManager.delay * 3)
            self.checkAnswer(answer)

            print()
            self.gameManager.waitForPlayerToContinue()
            self.gameManager.clearScreen()

            # Repeat for next player in line
            self.setNextActivePlayer()

        # 2. Voting
        print()
        self.gameManager.host.say("Times up. Who do you think was the weakest link this round?")
        print()
        self.gameManager.displayList(self.playersInRound)
        print()
        self.castVotes()
        print()
        votes = self.getPlayerVotes()
        #time.sleep(self.gameManager.delay)
        self.gameManager.clearScreen()
        self.gameManager.host.say("Stop. Show me the votes.")
        self.gameManager.printHeader("Votes")
        self.displayVotes(votes)

        # 3. Elimination
        self.elimination(votes)

        # end round
        self.gameManager.waitForPlayerToContinue()

    """
    playFinalRound()
    The final round occurs when there are two players remaining. 

    The final two contestants battle it out in a head-to-head contest. 
    They are eached asked 5 questions. Whoever answers the most correct wins the game.
    """
    def playFinalRound(self):
        remainingPlayers = self.gameManager.getRemainingPlayers()
        playerA = remainingPlayers[0]
        playerB = remainingPlayers[1]

        self.gameManager.host.say("There can only be one winner.")
        self.gameManager.host.say("Now, answer 5 questions each.")
        self.gameManager.host.say("If there is a tie - we go for sudden death.")
        print()
        self.gameManager.waitForPlayerToContinue()
        self.gameManager.clearScreen()

        self.gameManager.host.say("So, {} and {} for ${}...".format(remainingPlayers[0].name, remainingPlayers[1].name, self.gameManager.bank.currentValue))
        time.sleep(self.gameManager.delay)
        self.gameManager.host.say("...let's play the weakest link!")
        print()
        self.gameManager.waitForPlayerToContinue()
        self.gameManager.clearScreen()


        for numQuestion in range(2):
            for player in self.playersInRound:
                print(player.name + " | " + str(self.playerRoundInfoDict[player]['numCorrectAnswers']) + " correct | " + str(self.playerRoundInfoDict[player]['numIncorrectAnswers']) + " incorrect |")
            print()
            self.gameManager.host.say(self.activePlayer.name)
            print()
            self.askQuestion()
            time.sleep(self.gameManager.delay)
            print()
            # Get the player's answer and check if it is correct
            answer = self.activePlayer.getResponse(self.currentQuestion.choices)
            self.activePlayer.say(answer)
            time.sleep(self.gameManager.delay * 3)
            self.checkAnswer(answer)
            print()
            self.gameManager.waitForPlayerToContinue()
            self.gameManager.clearScreen()
            self.setNextActivePlayer()

        
        if self.playerRoundInfoDict[playerA]["numCorrectAnswers"] == self.playerRoundInfoDict[playerB]["numCorrectAnswers"]:
            suddenDeath = True
            self.gameManager.host.say("Time for sudden death!")
            while (suddenDeath):
                for player in self.playersInRound:
                    print(player.name + " | " + str(self.playerRoundInfoDict[player]['numCorrectAnswers']) + " correct | " + str(self.playerRoundInfoDict[player]['numIncorrectAnswers']) + " incorrect |")
                print()
                self.gameManager.host.say(self.activePlayer.name)
                print()
                self.askQuestion()
                print()
                answer = self.activePlayer.getResponse(self.currentQuestion.choices)
                self.checkAnswer(answer)
                self.gameManager.waitForPlayerToContinue()

                if answer != self.currentQuestion.correctAnswer:
                    playerToEliminate = self.activePlayer
                    suddenDeath = False
                self.gameManager.clearScreen()
                self.setNextActivePlayer()
        else:
            if self.playerRoundInfoDict[playerA]["numCorrectAnswers"] > self.playerRoundInfoDict[playerB]["numCorrectAnswers"]:
                playerToEliminate = playerB
            else:
                playerToEliminate = playerA

        self.gameManager.host.say("Sorry " + playerToEliminate.name + ", you are the weakest link")
        self.gameManager.host.say("Goodbye.")
        self.gameManager.waitForPlayerToContinue()
        playerToEliminate.eliminate()

    """
    displayVotes()
    Displays a list of the votes cast against each player in the round in descending order
    """
    def displayVotes(self, votes):
        votes = sorted(votes, key=lambda x: x[1], reverse=True) # sort descending based on vote count
        for vote in votes:
            print(vote[0].name + ": " + str(vote[1]))
            time.sleep(self.gameManager.delay)

    """
    elimination()
    The elimination portion of the round.

    This function takes as input an array of votes. Each element is a tuple of the player object, and the number of votes they recieved
    """
    def elimination(self, votes):
        mostVotesAgainst = 0
        players = []

        # Get player or players with the most votes
        highestVoteCount = 0
        for vote in votes:
            numVotes = vote[1]
            if numVotes == highestVoteCount:
                players.append(vote[0])
            elif numVotes > highestVoteCount:
                highestVoteCount = numVotes
                players = [vote[0]]

        print()
        # If there is a tie of two or more
        if len(players) > 1:
            self.gameManager.host.say("Looks like we have a few who are staring down elimination...")
            self.gameManager.host.say("Rules dictate the strongest link decides")
            strongestLink = self.getStrongestLink()
            self.gameManager.host.say("Congrats, " + strongestLink.name + ".")
            self.gameManager.host.say("You were the strongest link this round.")
            playerToEliminate = strongestLink.getResponse(players)
            strongestLink.say(playerToEliminate.name)
        # Not tie
        else:
            playerToEliminate = players[0]

        self.gameManager.host.say("Sorry " + playerToEliminate.name + ", you are the weakest link")
        self.gameManager.host.say("Goodbye.")
        playerToEliminate.eliminate()

    """
    getStrongestLink()
    Calculates and returns the strongest link (the player with the most correct answers)
    If there are multiple we pick one at random
    """
    def getStrongestLink(self):
        mostCorrectAnswers = 0
        players = []
        for player in self.playerRoundInfoDict:
            numCorrect = self.playerRoundInfoDict[player]['numCorrectAnswers']
            if numCorrect == mostCorrectAnswers:
                players.append(player)
            elif numCorrect > mostCorrectAnswers:
                players = [player]
        
        # if there is multiple strongest links -> pick one at random
        if len(players) > 1:
            self.gameManager.host.say("As it appears that there are multiple strong links. We pick at random.")
            player = random.choice(players)
        else:
            player = players[0]

        return player

    """
    setNextActivePlayer()
    """
    def setNextActivePlayer(self):
        # last player in the list, return to start of list
        if self.currentPlayerIndex + 1 == len(self.playersInRound):
            self.currentPlayerIndex = 0
        else:
            self.currentPlayerIndex += 1
        # set the current player
        self.activePlayer = self.playersInRound[self.currentPlayerIndex]

    """
    castVotes()
    Collects the vote of every active player in the round
    """
    def castVotes(self):
        for player in self.playersInRound:
            playerVotedAgainst = player.getResponse(self.playersInRound)
            self.playerRoundInfoDict[playerVotedAgainst]["numVotesAgainst"] += 1

    """
    getPlayerVotes()
    Returns a list of all the votes cast against each player in the round
    """
    def getPlayerVotes(self):
        votes = []
        for player in self.playersInRound:
            votes.append((player, self.playerRoundInfoDict[player]["numVotesAgainst"]))
        return votes

    """
    askIfBank()
    Gives the player the option to bank
    """
    def askIfBank(self):
        print(self.gameManager.bank)
        print()
        print("Bank?")
        bankOptions = ["Yes", "No"]
        self.gameManager.displayList(bankOptions)
        print()
        response = self.activePlayer.getResponse(bankOptions)
        self.activePlayer.say(response)
        print()
        if response.lower() == "yes":
            self.gameManager.bank.bankCurrentAmount()
            print(self.gameManager.bank)
            print()

    """
    askQuestion()
    Generates a random question, and displays the choices
    """
    def askQuestion(self):
        self.currentQuestion = Question()
        self.questions.append(self.currentQuestion)
        self.gameManager.host.say(self.currentQuestion.question, "")
        self.gameManager.displayList(self.currentQuestion.choices)
    
    """
    checkAnswer()
    Checks if the player answer matches the correct answer for the question
    """
    def checkAnswer(self, playerAnswer):
        # Verify if the answer is correct/wrong
        if playerAnswer.lower().strip() == self.currentQuestion.correctAnswer.lower().strip():
            self.gameManager.host.say("Correct")
            self.gameManager.bank.moveUp()
            self.playerRoundInfoDict[self.activePlayer]["numCorrectAnswers"] += 1    
        else:
            self.gameManager.host.say("The correct answer is " + self.currentQuestion.correctAnswer)
            self.playerRoundInfoDict[self.activePlayer]["numIncorrectAnswers"] += 1
