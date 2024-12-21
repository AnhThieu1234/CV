import random
import pygameRogers
import pygame
from pygameRogers import Room
from pygameRogers import TextRectangle
from pygameRogers import Game
from pygameRogers import GameObject
from pygameRogers import Alarm

#Create a new game
g = Game(1000, 600)

#Colours & Font
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
ORANGE = (255,165,0)
PASTELGREEN = (140,200,140)
arialFont80 = g.makeFont("Arial", 80)
arialFont50 = g.makeFont("Arial", 50)
arialFont35 = g.makeFont("Arial", 35)
arialFont20 = g.makeFont("Arial", 20)

#Resources
gameBackground = g.makeBackground(PASTELGREEN)
rectangle = g.makeRectangle(75, 100, BLUE)
hide = g.makeRectangle(0, 0, WHITE)

#Creating sprite images for all the cards
heartPics = []
for i in range(2, 15):
        heartPics.append(g.makeSpriteImage("Cards\HEARTS" + str(i) + ".jpg"))
diamondPics = []
for i in range(2, 15):
        diamondPics.append(g.makeSpriteImage("Cards\DIAMONDS" + str(i) + ".jpg"))
clubPics = []
for i in range(2, 15):
        clubPics.append(g.makeSpriteImage("Cards\CLUBS" + str(i) + ".jpg"))
spadePics = []
for i in range(2, 15):
        spadePics.append(g.makeSpriteImage("Cards\SPADES" + str(i) + ".jpg"))

topCard = g.makeSpriteImage("Cards\TOP.jpg")

#Creating sprite images for tokens
tokenImage = g.makeSpriteImage("Other resources/Token100.png")


#Class for insertion sorting
def insertionSort(a):

        #For loop for length of give list of cards
        for i in range(1, len(a)):

                #Take a card out of list to insert in already sorted list
                insert = a[i]

                #Variable for the value of the card
                check = int(a[i].original)

                #Find the correct spot in the already sorted list
                location = i
                while location > 0 and int(a[location-1].original) < check:
                        
                        a[location] = a[location - 1]
                        
                        location = location - 1

                #Insert at new found location
                a[location] = insert

#Classes for game objects
#Class for text box
class TextBox(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

#Class for tokens in the banking system
class Tokens(GameObject):

        #Creating object using image and value
        def __init__(self, image, value):
                GameObject.__init__(self, image)

#Class for bet display amount
class BetButton(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

                #Assigning attributes
                self.betList = [] #list that holds the best amount/tokens
                self.betNum = 0 #number of bet
                self.originalBetNum = 0 #original number of bet

        #Updating object
        def update(self):

                #Updating the text of bet display
                self.betNum = len(self.betList)*100
                betDisplay.setText("Bet: " + str(self.betNum))
                betDisplay2.setText("Bet: " + str(self.betNum))

                #If there is a bet, remove button to leave game
                if len(self.betList) != 0:
                        quitGame.kill()

                #If there is no bet, add button to leave game
                elif len(self.betList) == 0:
                        r2.addObject(quitGame)

                #check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse is clicked add a token to the bet
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        playerBank.giveToken()

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for bet remove button
class DelBetButton(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating object
        def update(self):
                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse is clicked take a token away from bet
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        playerBank.takeToken()

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for button to finish bet and play game
class DoneBet(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked -> start game
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #If the bet isn't 0:
                        if len(betButton.betList) != 0:

                                betButton.originalBetNum = len(betButton.betList) #setting original bet list variable
                                minBet.kill() #remove minimum bet display
                                betDisplay.kill() #remove bet display
                                betButton.kill() #remove bet button
                                takeBet.kill() #remove del bet button
                                quitGame.kill() #remove quit game button

                                r2.addObject(d) #add deck object
                                r2.addObject(dDisplay) #add deck counter object
                                r2.addObject(discardCounter) #add discard counter object
                                r2.addObject(startRound) #add start round button
                                r2.addObject(betDisplay2) #add smaller bet display

                                self.kill() #remove done bet button

                        #Prevent multiple clicks
                        self.mouseHasPressedOnMe = False

#Class for banking system
class Bank(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

                #Assigning attributes
                self.tokens = [] #list for all player's tokens
                self.betTimes = 1 #Win multiplier

                #Giving the player $2000 to start off with
                for i in range(0, 20):
                        token = Tokens(tokenImage, 100)
                        self.tokens.append(token)

        #Updating object
        def update(self):

                #Updating bank amount text
                self.setText("Bank: " + str(len(self.tokens)*100))
                finalBank.setText("$" + str(len(self.tokens)*100))

        #Define function to give token to bet list
        def giveToken(self):
                if len(self.tokens) != 0:
                        betButton.betList.append(self.tokens[0])
                        del(self.tokens[0])

        #Define function to take token from bet list
        def takeToken(self):
                if len(betButton.betList) != 0:
                        playerBank.tokens.append(betButton.betList[0])
                        del(betButton.betList[0])

        #Define function to add token to bet list
        def winToken(self):
                token = Tokens(tokenImage, 100)
                betButton.betList.append(token)

        #Define function to remove token from bet list
        def loseToken(self):
                del(betButton.betList[0])

#Class for quit button
class Quit(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked:
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #Go to final room "End Game"
                        g.goToRoom(2)

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False
                
#Class for HIT button
class HitButton(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor, splitName):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

                #Assigning attributes
                self.splitName = splitName #variable for which deck to give card to

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked give card to specified deck
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #If hit button is for player deck:
                        if self.splitName == "none":

                                #Use PlayerDeck takeCard() function to take card
                                playerCards.takeCard()

                        #If hit button is for split deck:
                        elif self.splitName == "first":

                                #Use Splits takecard() function to take card
                                PlayerDeck.firstSplit.takeCard()
                
                        Deck.mode = 1

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for doubling down -> double the player's bet, gets card from dealer, and then stand
class DoubleDown(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor, splitName):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

                #Assigning attributes
                self.splitName = splitName

        #Updating object
        def update(self):
                
                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #Go to playing room when object is clicked
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        
                        #If there is enough money in the bank
                        if int(betButton.betNum) <= int(len(playerBank.tokens)*100):      

                                #If the doubling down button is for player's original deck
                                if self.splitName == "none":
                                        
                                        playerCards.takeCard() #take card from dealer
                                        playerCards.betTimes = playerCards.betTimes*2 #times payout by multiplier of 2
                                        StartRoundButton.stand.kill() #remove stand button
                                        StartRoundButton.hit.kill() #remove hit button

                                        #Check for ace and change value accordingly using addTotalAce() function
                                        playerCards.addTotalAce()

                                        #If the player's total is over 21 -> bust
                                        if playerCards.addTotal() > 21:
                                                WinDecider.loseList.append(playerCards) #add player to the lose list
                                                PlayerDeck.bustNum = PlayerDeck.bustNum + 1 #increase bust counter

                                        #If player doesn't bust
                                        else:
                                                WinDecider.standList.append(playerCards) #Add player to stand list to check win/lose later
                                                PlayerDeck.standNum = PlayerDeck.standNum + 1 #increase stand counter

                                        #Double bet
                                        for i in range(0, betButton.originalBetNum):
                                                playerBank.giveToken()

                                        #Update bet display text  
                                        betDisplay2.setText("Bet: " + str(len(betButton.betList)*100))

                                #If the doubling down button is for the split deck
                                elif self.splitName == "first":
                                        
                                        PlayerDeck.firstSplit.takeCard() #take card from dealer
                                        PlayerDeck.firstSplit.betTimes = PlayerDeck.firstSplit.betTimes*2 #times payout by multiple of 2
                                        SplitButton.splitStand.kill() #remove stand button
                                        SplitButton.splitHit.kill() #remove hit button

                                        #Check for ace and change value accordingly using addTotalAce() function
                                        PlayerDeck.firstSplit.addTotalAce()

                                        #If the player's split total is over 21 -> bust
                                        if PlayerDeck.firstSplit.addTotal() > 21:
                                                WinDecider.loseList.append(PlayerDeck.firstSplit) #add player split to the lose list
                                                PlayerDeck.bustNum = PlayerDeck.bustNum + 1 #increase bust counter

                                        else:
                                                WinDecider.standList.append(PlayerDeck.firstSplit) #Add player split to stand list to check win/lose later
                                                PlayerDeck.standNum = PlayerDeck.standNum + 1 #increase stand counter

                                        #Double bet
                                        for i in range(0, betButton.originalBetNum):
                                                playerBank.giveToken()

                                        #Update bet display text
                                        betDisplay2.setText("Bet: " + str(len(betButton.betList)*100))

                                #Check if all decks are done
                                if PlayerDeck.standNum + PlayerDeck.bustNum == PlayerDeck.splitNum + 1:
                                        dealerCards.timer.setAlarm(1500)
                                        Deck.mode = 3    

                        #Remove double down button
                        self.kill()

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for stand buttons                        
class StandButton(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor, splitName):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

                #Assigning attributes
                self.timer = Alarm() #creating alarm
                self.splitName = splitName #assigning owner

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked:
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #Increase stand counter
                        PlayerDeck.standNum = PlayerDeck.standNum + 1

                        #Remove split option
                        Deck.split.kill()

                        #Check if all decks are done
                        if PlayerDeck.standNum + PlayerDeck.bustNum == PlayerDeck.splitNum + 1:
                                dealerCards.timer.setAlarm(1500) #set timer for dealer to reveal card
                                StartRoundButton.hit.kill() #remove hit button
                                SplitButton.splitHit.kill() #remove split's hit button
                                Deck.mode = 3
                                PlayerDeck.standNum = 0
                                PlayerDeck.splitNum = 0

                                #Remove all players option objects
                                if self.splitName == "none":
                                        StartRoundButton.hit.kill()
                                        StartRoundButton.doubleDown.kill()
                                        WinDecider.standList.append(playerCards)

                                #Remove all split's option objects
                                elif self.splitName == "first":
                                        SplitButton.splitStand.kill()
                                        WinDecider.standList.append(PlayerDeck.firstSplit)
                                        SplitButton.splitDoubleDown.kill()

                                #remove stand button
                                self.kill()

                        #If all decks are not done
                        else:

                                #Remove all players option objects
                                if self.splitName == "none":
                                        StartRoundButton.hit.kill()
                                        StartRoundButton.doubleDown.kill()
                                        WinDecider.standList.append(playerCards)

                                #Remove all split's option objects
                                elif self.splitName == "first":
                                        SplitButton.splitHit.kill()
                                        SplitButton.splitDoubleDown.kill()
                                        WinDecider.standList.append(PlayerDeck.firstSplit)

                                #remove stand button
                                self.kill()

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for split button
class SplitButton(TextRectangle):

        #Class objects
        splitHit = HitButton("HIT", 620, 405, arialFont20, BLACK, 60, 30, GREEN, "first")
        splitStand = StandButton("STAND", 700, 405, arialFont20, BLACK, 60, 30, RED, "first")
        splitDoubleDown = DoubleDown("DOUBLE DOWN", 620, 370, arialFont20, WHITE, 140, 30, BLUE, "first")

        #Creating objects using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor, splitName):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

                #Assigning variables
                self.splitName = splitName #assigning owner

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked:
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #if button is for split deck
                        if self.splitName == "first":

                                #If there is enough money to split
                                if int(betButton.betNum) <= int(len(playerBank.tokens)*100):

                                        #Add original bet
                                        for i in range(0, betButton.originalBetNum):
                                                playerBank.giveToken()

                                        #Set bet display text
                                        betDisplay2.setText("Bet: " + str(len(betButton.betList)*100))

                                        PlayerDeck.splitNum = PlayerDeck.splitNum + 1 #increase split num
                                        Deck.mode = 4
                                        PlayerDeck.firstSplit.splitOne() #get first card for new split deck
                                        playerCards.takeCard() #get card for original deck to replace split card
                                        PlayerDeck.firstSplit.takeCard() #get second card for split deck
                                        r2.addObject(SplitButton.splitHit) #add hit button for split deck
                                        r2.addObject(SplitButton.splitStand) #add stand button for split deck

                                #If player has enough money, add double down button for split deck
                                if int(betButton.betNum) <= int(len(playerBank.tokens)*100):
                                        r2.addObject(SplitButton.splitDoubleDown)
                        #Remove split button
                        self.kill()

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for start round button
class StartRoundButton(TextRectangle):

        #Class objects
        hit = HitButton("HIT", 170, 405, arialFont20, BLACK, 60, 30, GREEN, "none")
        stand = StandButton("STAND", 250, 405, arialFont20, BLACK, 60, 30, RED, "none")
        doubleDown = DoubleDown("DOUBLE DOWN", 170, 370, arialFont20, WHITE, 140, 30, BLUE, "none")

        #Creating objects using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating objects
        def update(self):

                #Check for mouse click
                 self.checkMousePressedOnMe(event)

                 #if mouse clicked, start game
                 if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:    

                        self.start()

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

        #Defning function to start game
        def start(self):

                d.timer2.setAlarm(1500) #set deck alarm
                playerCards.takeCard() #deal card to player
                dealerCards.hideCard() #deal face down card to dealer
                startRound.kill() #remove start round button
        
                Deck.mode = Deck.mode + 1 

#Class for start button to go to playing room
class StartButton(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating object
        def update(self):
                
                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #Go to playing room when object is clicked
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        g.goToRoom(1)

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False
                

#Class for creating an object of each card
class Card(GameObject):

        #Creating object using picture, value, suit, and original card value
        def __init__(self, picture, value, suit, original):
                GameObject.__init__(self, picture)

                #Assigning attributes
                self.value = value #value of the card
                self.original = original
                self.suit = suit #suit of the card
                self.keepImage = picture #original image of the card

        #Defining str() function to print card
        def __str__(self):
                return str(self.value) + self.suit

#Class for the starting deck
class Deck(GameObject):

        #Class variables & objects
        mode = 0
        split = SplitButton("SPLIT", 210, 335, arialFont20, BLACK, 60, 30, ORANGE, "first")

        #Creating object using x-pos, y-pos
        def __init__(self, picture, xPos, yPos):
                GameObject.__init__(self, picture)

                #Assigning attributes
                self.rect.x = xPos #x-position
                self.rect.y = yPos #y-position

                self.deck = [] #list for all cards in the deck

                self.timer = Alarm() #creating alarm
                self.timer2 = Alarm() #creating second alarm

                self.counter = 0 #card counter

                #Adding 4 decks of 52 cards into the deck using Card class to create card objects
                for o in range(0, 4):

                        #For loop for all heart cards
                        for i in range(0, len(heartPics)):

                                #Values of 2-10 are face value
                                if i+2 <= 10:
                                        c = Card(heartPics[i], i+2, "H", i+2)
                                        self.deck.append(c)

                                #Face cards gave values of 10
                                elif i+2 >10 and i+2 <= 13:
                                        c = Card(heartPics[i], 10, "H", i+2)
                                        self.deck.append(c)

                                #Aces are 11 to start but can be 1
                                elif i+2 == 14:
                                        c = Card(heartPics[i], 11, "H", i+2)
                                        self.deck.append(c)

                        #For loop for all diamond cards
                        for i in range(0, len(diamondPics)):

                                #Values of 2-10 are face value
                                if i+2 <= 10:
                                        c = Card(diamondPics[i], i+2, "D", i+2)
                                        self.deck.append(c)

                                #Face cards gave values of 10
                                elif i+2 >10 and i+2 <= 13:
                                        c = Card(diamondPics[i], 10, "D", i+2)
                                        self.deck.append(c)

                                #Aces are 11 to start but can be 1
                                elif i+2 == 14:
                                        c = Card(diamondPics[i], 11, "D", i+2)
                                        self.deck.append(c)
                                        
                        #For loop for all club cards
                        for i in range(0, len(clubPics)):

                                #Values of 2-10 are face value
                                if i+2 <= 10:
                                        c = Card(clubPics[i], i+2, "C", i+2)
                                        self.deck.append(c)

                                #Face cards gave values of 10
                                elif i+2 >10 and i+2 <= 13:
                                        c = Card(clubPics[i], 10, "C", i+2)
                                        self.deck.append(c)

                                #Aces are 11 to start but can be 1
                                elif i+2 == 14:
                                        c = Card(clubPics[i], 11, "C", i+2)
                                        self.deck.append(c)

                        #For loop for all spade cards
                        for i in range(0, len(spadePics)):

                                #Values of 2-10 are face value
                                if i+2 <= 10:
                                        c = Card(spadePics[i], i+2, "S", i+2)
                                        self.deck.append(c)

                                #Face cards gave values of 10
                                elif i+2 >10 and i+2 <= 13:
                                        c = Card(spadePics[i], 10, "S", i+2)
                                        self.deck.append(c)

                                #Aces are 11 to start but can be 1
                                elif i+2 == 14:
                                        c = Card(spadePics[i], 11, "S", i+2)
                                        self.deck.append(c)

                #insertionSort(self.deck)

                #Shuffling cards in the deck
                random.shuffle(self.deck)

        #Updating object
        def update(self):

                #Updating deck card counter display text
                dDisplay.setText("Deck: " + str(len(d.deck)))

                #If deck is about to run out, get cards from discard pile
                if len(self.deck) <= 1:
                        discard.giveCards()

                #If second timer done -> round start:
                if self.timer2.finished():
                        playerCards.takeCard() #deal card to player
                        dealerCards.takeCard() #deal card to dealer
                        r2.addObject(startRound.hit) #add player hit button
                        r2.addObject(startRound.stand) #add player stand button

                        #If player has enough money -> add double down button
                        if int(betButton.betNum) <= int(len(playerBank.tokens)*100):
                                r2.addObject(startRound.doubleDown)

                        #If player has money -> add split button
                        if int(playerCards.cards[0].value) == int(playerCards.cards[1].value) and len(playerCards.cards) == 2:
                                if int(betButton.betNum) <= int(len(playerBank.tokens)*100):
                                        r2.addObject(Deck.split)

                #If player has more than 2 cards -> remove double down and split option
                if len(playerCards.cards) != 2:
                        Deck.split.kill()
                        StartRoundButton.doubleDown.kill()

                #if there isn't enough money in bank to double down -> remove double down and split option
                if int(betButton.betNum) > int(len(playerBank.tokens)*100):
                        Deck.split.kill()
                        StartRoundButton.doubleDown.kill()
                
                #if split deck has more than 2 cards -> remove split double down
                if len(PlayerDeck.firstSplit.cards) != 2:
                        SplitButton.splitDoubleDown.kill()

                #if there isn't enough money in bank to double down -> remove split double down
                if int(betButton.betNum) > int(len(playerBank.tokens)*100):
                        SplitButton.splitDoubleDown.kill()

        #Defining str() function to print the deck
        def __str__(self):
                s = ""
                for card in self.deck:
                        s = s + str(card) + " "
                s = "Deck:\n" + s + "\n"
                return s                

#Class for reset button
class Reset(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked -> reset all variables, kill playing objects, add betting objects
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #Remove all win texts
                        for i in range(0, 2):
                                WinDecider.pWinTextList[i].kill()

                        #Remove all lose texts
                        for k in range(0, 2):
                                WinDecider.dWinTextList[k].kill()

                        #Remove all tie texts
                        for l in range(0, 2):
                                WinDecider.tWinTextList[l].kill()

                        DiscardDeck.takeCards() #give all played cards to discard pile
                        BustDisplay.splitBustText.kill() #remove split bust text
                        BustDisplay.playerBustText.kill() #remove player bust text
                        BustDisplay.dealerBustText.kill() #remove dealer bust text
                        PlayerDeck.firstSplit.kill() #remove split deck
                        StartRoundButton.hit.kill() #remove player hit button
                        StartRoundButton.doubleDown.kill() #remove player double down button
                        SplitButton.splitHit.kill() #remove split hit button
                        betDisplay2.kill() #remove small bet display

                        playerCards.bust = 0
                        PlayerDeck.firstSplit.bust = 0
                        PlayerDeck.splitNum = 0 #reset split num
                        PlayerDeck.standNum = 0 #reset stand num
                        PlayerDeck.bustNum = 0 #reset bust num
                        Deck.mode = 0

                        WinDecider.standList.clear()
                        WinDecider.winList.clear()
                        WinDecider.loseList.clear()
                        WinDecider.tieList.clear()
                        
                        playerCards.betTimes = 1 #reset bet multiplier
                        PlayerDeck.firstSplit.betTimes = 1 #reset bet multiplier

                        r2.addObject(minBet) #add minimum bet info to playing room
                        r2.addObject(doneBet) #add done bet button to playing room
                        r2.addObject(takeBet) #add more bet button to playing room
                        r2.addObject(betDisplay) #add bet display to playing room
                        r2.addObject(betButton) #add bet button to playing room
                        r2.addObject(quitGame) #add quit game option to playing room
                        
                        self.kill() #remove reset button

                        #Prevent multiple clicks
                        self.mouseHasPressedOnMe = False

#Class for dealer draw button when dealer's cards are less than 16
class DealerDraw(TextRectangle):

        #Creating object using TextRectangle
        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)

        #Updating object
        def update(self):

                #Check for mouse click
                self.checkMousePressedOnMe(event)

                #If mouse clicked -> give dealer card
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        dealerCards.takeCard() #give dealer card
                        self.kill() #remove draw button
                        DealerDeck.lessInfo.kill() #remove draw info button

                        #Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

#Class for dealer deck
class DealerDeck(GameObject):

        #Class variables
        lessInfo = TextBox("Dealer has values of 16 or less, dealer draws.", 75, 250, arialFont20, BLACK, 360, 50, WHITE)
        dealerDrawButton = DealerDraw("CLICK", 175, 325, arialFont35, BLACK, 125, 50, GREEN)
        resetButton = Reset("Click for next round", 100, 300, arialFont35, BLACK, 270, 40, GREEN)

        #Creating object using x-pos and y-pos
        def __init__(self, xPos, yPos):
                GameObject.__init__(self)

                #Assigning attributes
                self.rect.x = xPos #x-position
                self.rect.y = yPos #y-position
                self.timer = Alarm() #create alarm
                self.cards = [] #list for dealer's all cards

        #Updating objects
        def update(self):

                #If timer finished -> reveal faced down card
                if self.timer.finished() and Deck.mode == 3:
                        self.cards[0].image = self.cards[0].keepImage
                                 
                if Deck.mode == 3:

                        #If image is faced up
                        if self.cards[0].image != topCard:

                                #Check for ace and decide value accordingly
                                self.addTotalAce()

                                #check value of dealer's total
                                check = int(dealerCards.addTotal())

                                #If dealer's total is less than or equal to 16 and not all players busted, pick up card
                                if check <= 16 and PlayerDeck.bustNum != PlayerDeck.splitNum + 1:
                                        r2.addObject(DealerDeck.lessInfo)
                                        r2.addObject(DealerDeck.dealerDrawButton)

                                #If dealer's total is less than or equal to 16 and all players busted -> dealer wins and don't need cards
                                elif check <= 16 and PlayerDeck.bustNum == PlayerDeck.splitNum + 1:
                                        
                                        r2.addObject(DealerDeck.resetButton) #add reset button
                                        WinDecider.dealerWin() #go through all loses
                                        WinDecider.checkWins() #check wins
                                        WinDecider.playerWin() #go through wins
                                        WinDecider.dealerWin() #go through loses again
                                        WinDecider.tie() #check ties

                                        #Give all gained or loss tokens from bet list back to player's bank
                                        for u in range(0, len(betButton.betList)):
                                                playerBank.takeToken()

                                        #Update bet display
                                        betDisplay2.setText("Bet: " + str(int(len(betButton.betList)*100)))

                                #If dealer's total is bigger or equal to 17 and smaller or equal to 21 -> check wins and losses
                                elif check >= 17 and check <= 21:
                                        
                                        WinDecider.checkWins() #check all standing players win and losses
                                        WinDecider.playerWin() #give tokens to winners
                                        WinDecider.dealerWin() #take tokens from losers
                                        WinDecider.tie() #check ties

                                        #Add reset button
                                        r2.addObject(DealerDeck.resetButton)

                                        #Give all gained or loss tokens from bet list back to player's bank
                                        for u in range(0, len(betButton.betList)):
                                                playerBank.takeToken()

                                        #Update bet display
                                        betDisplay2.setText("Bet: " + str(int(len(betButton.betList)*100)))
                                        Deck.mode = 1

                                #If dealer's total is bigger than 21 -> dealer busts
                                elif check >= 22:

                                        BustDisplay.dealerBust() #display dealer bust text box
                                        WinDecider.dealerBust() #use class WinDecider.dealerBust() function to add all standing decks to winning list
                                        WinDecider.playerWin() #give tokens to winners
                                        WinDecider.dealerWin() #take tokens from losers
                                        WinDecider.tie() #check ties

                                        #Give all gained or loss tokens from bet list back to player's list
                                        for u in range(0, len(betButton.betList)):
                                                playerBank.takeToken()

                                        #Update bet display
                                        betDisplay2.setText("Bet: " + str(int(len(betButton.betList)*100)))
                                        Deck.mode = 0

                                        #Add reset button
                                        r2.addObject(DealerDeck.resetButton)
                                        
        #Defining function to get sum of value in deck
        def addTotal(self):
                
                total = 0

                #For loop to go through all the cards in deck and add value to total variable
                for i in range(0, len(self.cards)):
                        total = total + int(self.cards[i].value)

                #Return deck value total
                return total

        #Defining function to check for aces and change their value corresponding to what is best for the deck
        def addTotalAce(self):
                
                countAce = 0

                #For loop to go through all the cards in the deck and checking for number of aces in the deck
                for a in range(0, len(self.cards)):
                        if int(self.cards[a].original) == 14:
                                countAce = countAce + 1

                #If there is one or more aces in the deck -> insert sort the deck
                if countAce >= 1:

                        #Use inserSort() function to sort the deck and get all the aces to the front of the list
                        insertionSort(self.cards)

                        #For loop to check the value that is best suited for the deck -> either 1 or 11
                        for i in range(0, countAce):

                                #If the total of the deck is over 21 -> change the ace value to 1 so deck does not bust
                                if self.addTotal() > 21:
                                        self.cards[i].value = 1

                        #If the total of the deck without the ace value is less than or equal to 10 -> change ace value to 11 for the highest value possible
                        if int(self.addTotal()) <= 10:
                                self.cards[0].value = 11

        #Defining function to take and place a faced up card from playing deck to dealer's deck
        def takeCard(self):
                
                self.cards.append(d.deck[0]) #getting a card from the playing deck
                self.cards[len(self.cards)-1].rect.x = self.rect.x + 35 * len(self.cards) #setting new x-pos for card
                self.cards[len(self.cards)-1].rect.y = self.rect.y #setting new y-pos for card
                r2.addObject(self.cards[len(self.cards)-1]) #place card 
                del(d.deck[0]) #delete card from playing deck

        #Defining function to take and place a faced down card from playing deck to dealer's deck
        def hideCard(self):
                
                self.cards.append(d.deck[0]) #getting a card from the playing deck
                self.cards[len(self.cards)-1].rect.x = self.rect.x + 35 * len(self.cards) #setting new x-pos for card
                self.cards[len(self.cards)-1].rect.y = self.rect.y #setting new y-pos for card
                self.cards[len(self.cards)-1].image = topCard #place card 
                r2.addObject(self.cards[len(self.cards)-1])
                del(d.deck[0]) #delete card from playing deck

#Class for split deck
class Splits(GameObject):

        #Creating object x-pos, y-pos, and owner
        def __init__(self, xPos, yPos, splitName):
                GameObject.__init__(self)

                #Assigning variables
                self.rect.x = xPos #x-position
                self.rect.y = yPos #y-position
                self.cards = [] #list for all the cards in split deck
                self.splitName = splitName #owner of deck
                self.betTimes = 1 #bet multiplier of split deck
                self.bust = 0

        #Update objects
        def update(self):

                if Deck.mode >= 1 and Deck.mode != 3:

                        #Check for aces and choose best value for deck
                        self.addTotalAce()

                        #Add total of deck
                        check = PlayerDeck.firstSplit.addTotal()

                        #if deck's total is more than 21 -> deck busted
                        if check > 21 and self.bust == 0:
                                        
                               if self.splitName == "first":

                                        BustDisplay.splitBust() #add deck bust display textbox
                                        WinDecider.loseList.append(PlayerDeck.firstSplit) #add busted deck to lost list
                                        SplitButton.splitHit.kill() #remove split's hit button
                                        SplitButton.splitStand.kill() #remove split's stand button
                                        PlayerDeck.bustNum = PlayerDeck.bustNum + 1 #Increase bust counter
                                        self.bust = self.bust + 1

                                        #If the stand num + bust num equals the decks in the game
                                        if PlayerDeck.standNum + PlayerDeck.bustNum == PlayerDeck.splitNum + 1:
                                                dealerCards.timer.setAlarm(1500) #set dealer's deck alarm to reveal cards
                                                Deck.mode = 3

                                        else:
                                                Deck.mode = 0

                               #If the stand num + bust num equals the decks in the game
                               if PlayerDeck.standNum + PlayerDeck.bustNum == PlayerDeck.splitNum + 1:
                                        dealerCards.timer.setAlarm(1500) #set dealer's deck alarm to reveal cards
                                        Deck.mode = 3

                        self.total = 0
                

        #Defining function to get cards in split deck
        def splitOne(self):
                
                    self.cards.append(playerCards.cards[1]) #get card from player deck
                    self.cards[len(self.cards)-1].rect.x = self.rect.x + 35 * len(self.cards) #set new x-pos
                    self.cards[len(self.cards)-1].rect.y = self.rect.y #set new y-pos
                    playerCards.cards[1].kill() #remove the card object from the game
                    r2.addObject(self.cards[0]) #add card object to new position in the game
                    del(playerCards.cards[1]) #delete card from player's deck

        #Defining function to get sum of total in deck
        def addTotal(self):
                
                total = 0

                #For loop to go through all the cards in deck and add each value
                for i in range(0, len(self.cards)):
                        total = total + int(self.cards[i].value)

                #Returning total
                return total

        #Defining function to 
        def addTotalAce(self):
                
                countAce = 0
                #Defining function to check for aces and change their value corresponding to what is best for the deck
                for a in range(0, len(self.cards)):
                        if int(self.cards[a].original) == 14:
                                countAce = countAce + 1

                #If there is one or more aces in the deck -> insert sort the deck
                if countAce >= 1:

                        #Use insertSort() function to sort the deck and get all aces to the front of the list
                        insertionSort(self.cards)

                        #For loop to check the value that is best suited for the deck -> either 1 or 11
                        for i in range(0, countAce):

                                #If the total of the deck is over 21 -> change the ace value to 1 so deck does not bust
                                if self.addTotal() > 21:
                                        self.cards[i].value = 1

                        #If the total of the deck without the ace value is less than or equal to 10 -> change ace value to 11 for the highest value possible
                        if int(self.addTotal()) <= 10:
                                self.cards[0].value = 11
                                
        #Defining function to take and place a faced up card from playing deck to dealer's deck
        def takeCard(self):
                self.cards.append(d.deck[0]) #getting a card from the playing deck
                self.cards[len(self.cards)-1].rect.x = self.rect.x + 35 * len(self.cards) #setting new x-pos for card
                self.cards[len(self.cards)-1].rect.y = self.rect.y #setting new y-pos for card
                r2.addObject(self.cards[len(self.cards)-1]) #place card
                del(d.deck[0]) #delete card from playing deck

        #Defining function to remove all playing options for deck if bust
        def bust():
                SplitButton.splitHit.kill() #remove split hit
                SplitButton.splitStand.kill() #remove split stand
                SplitButton.splitDoubleDown.kill() #remove split double down

#Class for player's deck
class PlayerDeck(GameObject):

        #Class variables
        splitNum = 0
        standNum = 0
        bustNum = 0
        firstSplit = Splits(600, 450, "first")

        #Creating object using x-pos and y-pos
        def __init__(self, xPos, yPos):
                GameObject.__init__(self)

                #Assigning attributes
                self.rect.x = xPos #x-pos
                self.rect.y = yPos #y-pos
                self.cards = [] #list for all the cards
                self.timer = Alarm() #create alarm
                self.betTimes = 1 #bet multiplier
                self.bust = 0

        #Updating object
        def update(self):
                        
                if Deck.mode >= 1 and Deck.mode != 3:

                        #Check for aces
                        self.addTotalAce()

                        #Check player totals
                        playerCheck = playerCards.addTotal()

                        #If player's values is over 21 -> player bust
                        if playerCheck > 21 and self.bust == 0:

                                PlayerDeck.bust()
                                BustDisplay.playerBust() #add player bust display text box
                                WinDecider.loseList.append(playerCards) #add player deck to lost list
                                PlayerDeck.bustNum = PlayerDeck.bustNum + 1 #increase bust num counter
                                self.bust = self.bust + 1

                                #If standnum + bust num is equal to number of decks
                                if PlayerDeck.standNum + PlayerDeck.bustNum == PlayerDeck.splitNum + 1:
                                        dealerCards.timer.setAlarm(1500) #reveal dealer cards
                                        Deck.mode = 3

                                else:
                                        Deck.mode = 0
                                        
                        self.total = 0

                if Deck.mode == 4:

                        #if number of split is clicked -> add split deck
                        if PlayerDeck.splitNum == 1:
                                r2.addObject(PlayerDeck.firstSplit)
                                Deck.mode = 0

        #Defining function to add value of deck
        def addTotal(self):
                
                total = 0

                #For loop for length of of cards in deck
                for i in range(0, len(self.cards)):
                        total = total + int(self.cards[i].value)

                #Return total
                return total

        #Defining function to check for ace and change value to best suit deck
        def addTotalAce(self):

                countAce = 0

                #For loop for length of cards in deck
                for a in range(0, len(self.cards)):
                        if int(self.cards[a].original) == 14:
                                countAce = countAce + 1

                #If there is one or more aces in deck -> use insertSort function()
                if countAce >= 1:

                        #InsertSort() function to move all aces to the front of the deck
                        insertionSort(self.cards)

                        #For loop for how many aces there are in the deck
                        for i in range(0, countAce):

                                #If the total of the deck is more than 21 -> value of ace = 1
                                if self.addTotal() > 21:
                                        self.cards[i].value = 1

                        #If the total of the deck without ace is less or equal to 10 -> value of ace = 11
                        if int(self.addTotal()) <= 10:
                                self.cards[0].value = 11

        #Defining function to take card from playing deck
        def takeCard(self):
                
                self.cards.append(d.deck[0]) #get card from playing deck
                self.cards[len(self.cards)-1].rect.x = self.rect.x + 35 * len(self.cards) #set new x-pos for card
                self.cards[len(self.cards)-1].rect.y = self.rect.y #set new y-pos for card
                r2.addObject(self.cards[len(self.cards)-1]) #add card object to room
                del(d.deck[0]) #delete card from playing deck

        #Defining function to remove all playing options if player busts
        def bust():
                
                StartRoundButton.hit.kill() #remove hit button
                StartRoundButton.stand.kill() #remove stand button
                StartRoundButton.doubleDown.kill() #remove double down button

#Class to check and decide winners
class WinDecider():

        #Class variables
        pWinText1 = TextBox("WIN", 440, 250, arialFont20, BLACK, 60, 30, GREEN) #text object for player win
        pWinText2 = TextBox("WIN", 440, 250, arialFont20, BLACK, 60, 30, GREEN) #text object for split win
        pWinTextList = [pWinText1, pWinText2] #win object list
        
        dWinText1 = TextBox("LOSE", 440, 250, arialFont20, WHITE, 60, 30, RED) #text object for player lose
        dWinText2 = TextBox("LOSE", 440, 250, arialFont20, WHITE, 60, 30, RED) #text object for split lose
        dWinTextList = [dWinText1, dWinText2] #lose object list
        
        tWinText1 = TextBox("TIE", 440, 250, arialFont20, BLACK, 60, 30, WHITE) #text object for player tie
        tWinText2 = TextBox("TIE", 440, 250, arialFont20, BLACK, 60, 30, WHITE) #text object for split tie
        tWinTextList = [tWinText1, tWinText2] #tie object list

        p = 0 #win counter
        d = 0 #lose counter
        t = 0 #tie counter
        
        standList = [] #list for all stand decks
        loseList = [] #list for all lose decks
        winList = [] #list for all win decks
        tieList = [] #list for all tie decks

        #Defining function if dealers busts
        def dealerBust():

                #For loop to length of stand list
                for i in range(0, len(WinDecider.standList)):

                        #Add all standing decks to win list
                        WinDecider.winList.append(WinDecider.standList[0])
                        del(WinDecider.standList[0])

        #Defining function to check for wins, losses, and ties
        def checkWins():

                #For loop to length of stand list
                for i in range(0, len(WinDecider.standList)):

                        #Check for aces in any of the lists
                        (WinDecider.standList[0]).addTotalAce()

                        #If player's deck total is bigger than dealer's deck total then add to win list
                        if int((WinDecider.standList[0]).addTotal()) > int(dealerCards.addTotal()):
                                WinDecider.winList.append(WinDecider.standList[0])
                                del(WinDecider.standList[0])

                        #If player's deck total is smaller than dealer's deck total then add to lose list
                        elif int((WinDecider.standList[0]).addTotal()) < int(dealerCards.addTotal()):
                                WinDecider.loseList.append(WinDecider.standList[0])
                                del(WinDecider.standList[0])

                        #If player's deck total is equal to dealer's deck total then add to lose list
                        elif int((WinDecider.standList[0]).addTotal()) == int(dealerCards.addTotal()):
                                WinDecider.tieList.append(WinDecider.standList[0])
                                del(WinDecider.standList[0])

        #Defining function to add win textbox to each winner and distribute bet win
        def playerWin():

                #For loop for all winners
                for i in range(0, len(WinDecider.winList)):
                   
                        check21 = (WinDecider.winList[0]).addTotal()
                        checkDealer = dealerCards.addTotal()

                        #If player won with a 21 then double the bet winnings
                        if int(check21) == 21 and int(checkDealer) != 21:
                                WinDecider.winList[0].betTimes =  WinDecider.winList[0].betTimes*2

                        #For all the winners, give the winnings
                        for o in range(0, WinDecider.winList[0].betTimes*betButton.originalBetNum):
                                playerBank.winToken()

                        #Adding win textbox under winner's deck
                        WinDecider.pWinTextList[WinDecider.p].rect.x = (WinDecider.winList[0]).rect.x + 70 #set new x-pos 70 pixels right of deck
                        WinDecider.pWinTextList[WinDecider.p].rect.y = (WinDecider.winList[0]).rect.y + 110 #set new y-pos 110 pixels down of deck
                        r2.addObject(WinDecider.pWinTextList[WinDecider.p]) #add text box to room
                        WinDecider.p = WinDecider.p + 1 #increase winner text box counter
                        del(WinDecider.winList[0]) #delete winner from list

                #Reset winner text box counter
                WinDecider.p = 0

        #Defining function to add win textbox to each loser and distribute bet loss
        def dealerWin():

                #For loop for all losers
                for i in range(0, len(WinDecider.loseList)):

                        #For all the losers, take bet
                        for o in range(0, WinDecider.loseList[0].betTimes*betButton.originalBetNum):
                                playerBank.loseToken()

                        #Adding lose textbox under losers' deck
                        WinDecider.dWinTextList[WinDecider.d].rect.x = (WinDecider.loseList[0]).rect.x + 70 #set new x-pos 70 pixels right of deck
                        WinDecider.dWinTextList[WinDecider.d].rect.y = (WinDecider.loseList[0]).rect.y + 110 #set new y-pos 110 pixels down of deck
                        r2.addObject(WinDecider.dWinTextList[WinDecider.d]) #add text box to room
                        WinDecider.d = WinDecider.d + 1 #increase loser text box counter
                        del(WinDecider.loseList[0]) #delete loser from list
                        
                #Reset loser text box counter
                WinDecider.d = 0

        ##Defining function to add tie textbox
        def tie():

                #For loop for all ties
                for i in range(0, len(WinDecider.tieList)):

                        #Adding lose textbox under losers' deck
                        WinDecider.tWinTextList[WinDecider.t].rect.x = (WinDecider.tieList[0]).rect.x + 70 #set new x-pos 70 pixels right of deck
                        WinDecider.tWinTextList[WinDecider.t].rect.y = (WinDecider.tieList[0]).rect.y + 110 #set new y-pos 110 pixels down of deck
                        r2.addObject(WinDecider.tWinTextList[WinDecider.t]) #add text box to room
                        WinDecider.t = WinDecider.t + 1 #increase loser text box counter
                        del(WinDecider.tieList[0]) #delete loser from list

                #Reset tie text box counter
                WinDecider.t = 0

#Class for bust displays
class BustDisplay():

        #Class objects
        playerBustText = TextBox("Player bust", 210, 400, arialFont20, WHITE, 100, 30, BLUE)
        splitBustText = TextBox("Player bust", 660, 400, arialFont20, WHITE, 100, 30, BLUE)
        dealerBustText = TextBox("Dealer bust", 210, 170, arialFont20, WHITE, 100, 30, BLUE)

        #defining function to add player bust display
        def playerBust():
                r2.addObject(BustDisplay.playerBustText)

        #defining function to add split bust display
        def splitBust():
                r2.addObject(BustDisplay.splitBustText)

        #defining function to add dealer bust display
        def dealerBust():
                r2.addObject(BustDisplay.dealerBustText)

#Class for discard deck object
class DiscardDeck(GameObject):

        #Class variables
        hide = g.makeRectangle(0, 0, WHITE)

        #Creating object using x-pos and y-pos
        def __init__(self, xPos, yPos):
                GameObject.__init__(self)

                #Assigning attributes
                self.rect.x = xPos #x-position
                self.rect.y = yPos #y-position
                self.cards = [] #list for all the cards in the discard pile
                self.counter = 0 #counter for cards in pile

        #Updating object
        def update(self):

                #Updating discard deck counter
                self.counter = len(self.cards)
                discardCounter.setText("Discard: " + str(discard.counter))

                #If there are no cards in the discard deck, make the deck invisible
                if len(self.cards) == 0:
                        self.image = hide

        #Defining function that discards all the played cards
        def takeCards():

                #Take all cards from player's deck
                for k in range(0, len(playerCards.cards)):
                        discard.cards.append(playerCards.cards[0])
                        playerCards.cards[0].kill()
                        del(playerCards.cards[0])

                #Take all cards from split deck
                for m in range(0, len(PlayerDeck.firstSplit.cards)):
                        discard.cards.append(PlayerDeck.firstSplit.cards[0])
                        PlayerDeck.firstSplit.cards[0].kill()
                        del(PlayerDeck.firstSplit.cards[0])

                #Take all cards from dealer's deck
                for l in range(0, len(dealerCards.cards)):
                        discard.cards.append(dealerCards.cards[0])
                        dealerCards.cards[0].kill()
                        del(dealerCards.cards[0])

                #Set image of discard pile to topCard
                discard.image = topCard

        #Defining function to give all cards in discard pile to the playing pile
        def giveCards(self):

                #Give all cards to playing pile
                for i in range(0, len(self.cards)):
                        d.deck.append(self.cards[0])
                        del(self.cards[0])

                #Shuffling playing pile
                random.shuffle(d.deck)
        
#Create the Rooms and add them to the game
r1 = Room("Start Screen", gameBackground)
g.addRoom(r1)

r2 = Room("Blackjack Card Game", gameBackground)
g.addRoom(r2)

r3 = Room("End Game", gameBackground)
g.addRoom(r3)

#Initializing objects and adding them to room
d = Deck(topCard, 900, 50)

dDisplay = TextBox("Deck" + str(len(d.deck)), 890, 10, arialFont20, BLACK, 90, 35, WHITE)

startingText = TextBox("Blackjack Card Game", 150, 170, arialFont80, BLACK, 700, 100, PASTELGREEN)
r1.addObject(startingText)

start = StartButton("START", 410, 350, arialFont50, BLACK, 175, 75, GREEN)
r1.addObject(start)

discard = DiscardDeck(50, 50)
r2.addObject(discard)

discardCounter = TextBox("", 40, 10, arialFont20, BLACK, 90, 35, WHITE)

#Dealer's objects
dealerCards = DealerDeck(150, 50)
r2.addObject(dealerCards)

#Player's objects
playerCards = PlayerDeck(150, 450)
r2.addObject(playerCards)

#Bet and bet display objects
playerBank = Bank("Bank: 0", 45, 515, arialFont20, BLACK, 100, 35, WHITE)
r2.addObject(playerBank)

betButton = BetButton("+$100 Bet", 570, 375, arialFont35, BLACK, 200, 75, GREEN)
r2.addObject(betButton)

takeBet = DelBetButton("-$100 Bet", 230, 375, arialFont35, BLACK, 200, 75, RED)
r2.addObject(takeBet)

doneBet = DoneBet("Click to play with bet amount", 300, 500, arialFont35, WHITE, 400, 50, BLUE)
r2.addObject(doneBet)

betDisplay = TextBox("Bet: " + str(betButton.betNum), 350, 220, arialFont35, BLACK, 300, 75, WHITE)
r2.addObject(betDisplay)

betDisplay2 = TextBox("Bet: " + str(betButton.betNum), 45, 450, arialFont20, BLACK, 100, 35, WHITE)

startRound = StartRoundButton("START ROUND", 385, 280, arialFont35, BLACK, 220, 75, WHITE)

minBet = TextBox("MIN BET IS $100!", 365, 50, arialFont35, ORANGE, 275, 75, BLACK)
r2.addObject(minBet)

quitGame = Quit("QUIT", 850, 250, arialFont50, WHITE, 120, 70, RED)
r2.addObject(quitGame)

#Objects in "End Room" (r3)
finalMessage = TextBox("You left with: ", 310, 150, arialFont80, BLACK, 400, 100, PASTELGREEN)
r3.addObject(finalMessage)

finalBank = TextBox("0", 350, 325, arialFont50, BLACK, 300, 100, GREEN)
r3.addObject(finalBank)

#Start Game 
g.start()

while g.running:
        dt = g.clock.tick(60)
        
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        clickedObj = g.currentRoom().whatGotClicked()
                        if clickedObj != None:
                                clickedObj.clicked = True

                elif event.type == pygame.QUIT:
                        g.stop()
                        
        g.currentRoom().updateObjects()

        g.currentRoom().renderBackground(g)

        g.currentRoom().renderObjects(g)

        pygame.display.flip()

pygame.quit()
