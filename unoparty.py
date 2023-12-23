import random
from tkinter import *
from constant import *
from selector import *
from deck import *
from pygame import mixer

mixer.init()
takeCardSound = mixer.Sound('src/song/takecard.wav')
playCardSound = mixer.Sound('src/song/playcard.wav')
winSound = mixer.Sound('src/song/win.wav')
failSound = mixer.Sound('src/song/fail.wav')
unoSound = mixer.Sound('src/song/uno.wav')
unoVoiceSound = mixer.Sound('src/song/unovoice.wav')
music = mixer.Sound('src/song/music.wav')

def createStack(draw) -> tuple:
    '''crée le tas et pose la première carte de la pioche'''

    temp = Deck()
    for i in range(len(draw)):
        if not (draw[i].isSpecialCard() or draw[i].isJokerCard()):
            temp.append(draw.pop(i))
            return temp, draw

def createDeck(draw) -> tuple:
    '''crée un deck de 7 cartes'''

    temp = Deck()
    temp.extend([draw.pop(0) for i in range(7)])
    return temp, draw

def createDraw(parent) -> Deck:
    '''créer les 108 cartes du UNO'''

    draw = Deck()
    validSymbol = list(Symbol)[1:13]
    validColor = list(Color)[:-1]

    symbolColorList = [
            (Symbol.n0, Color.Blue),
            (Symbol.n0, Color.Red),
            (Symbol.n0, Color.Green),
            (Symbol.n0, Color.Yellow),
        ]

    for _ in range(2):
        symbolColorList.extend(
            [
                (Symbol.joker, Color.Black),
                (Symbol.joker, Color.Black),
                (Symbol.plus4, Color.Black),
                (Symbol.plus4, Color.Black)
            ]
        )
        for symbol in validSymbol:
            for color in validColor:
                symbolColorList.append((symbol, color))

    random.shuffle(symbolColorList)
    draw.extend([UNOCard(parent, i, j) for i, j in symbolColorList])
    return draw

class UNOParty(Canvas):
    running : bool = None

#===public function============================================================#
    def __init__(self, parent) -> None:

        Canvas.__init__(
            self, parent,
            width=ScreenSize.Width.value,
            height=ScreenSize.Height.value,
            highlightthickness=0
        )

        self.checker = IntVar()
        self.MAX_CARDS_IN_ROW : int = 20
        self.AMOUNT_OF_DELAY : int = 700
        self.background_image : PhotoImage = None
        self.UNOdraw : Deck = None
        self.playerDeck : Deck = None
        self.botDeck : Deck = None
        self.stack : Deck = None
        self.uno : Canvas = None
        self.unoImg : PhotoImage = None


        self.__setBackground()
        self.drawCardImg : UNOCard = UNOCard(self, Symbol.back, Color.Black)
        self.selector = ColorSelector(self)

    def loop(self) -> str:
        '''-----
        - verifier si l'un des deux deck est vide alors on quitte la boucle
        - si le tour du joueur est valide alors rafraichir le jeu
          - attendre 700ms
          - verifier s'il reste une carte au joueur, si oui afficher UNO

        - verifier si l'un des deux deck est vide alors on quitte la boucle
        - tour du bot
          - rafraichir le jeu
          - attendre 700ms
          - verifier s'il reste une carte au bot, si oui afficher UNO'''

        while UNOParty.running:

            if not(self.playerDeck.empty() or self.botDeck.empty()):
                if not self.__playerTurn():
                    return 'exit'

                self.__refreshGame()
                self.__delay(self.AMOUNT_OF_DELAY)
                self.__UNO(self.playerDeck)
            else: break

            if not(self.playerDeck.empty() or self.botDeck.empty()):
                self.__botTurn()
                self.__refreshGame()
                self.__delay(self.AMOUNT_OF_DELAY)
                self.__UNO(self.botDeck)
            else: break

        return self.__endGame()

    def setupGame(self) -> None:
        '''créer les 108 cartes du UNO, distribue 7 cartes au bot et au joueur
        et pose la première carte de la pioche sur le tas'''

        self.pack()
        UNOParty.running = True
        self.UNOdraw = createDraw(self)
        self.playerDeck, self.UNOdraw = createDeck(self.UNOdraw)
        self.botDeck, self.UNOdraw = createDeck(self.UNOdraw)
        self.stack, self.UNOdraw = createStack(self.UNOdraw)
        self.__showDraw()
        self.__refreshGame()

    def interupt(self) -> None:
        '''interompt la fonction loop'''
        UNOParty.running = False
        self.checker.set(-2)

#===Intern Function============================================================#

    def __botTurn(self) -> None:
        '''actions du bot
        - désactiver toutes les actions du joueur
        - recherche la première carte jouable
        - s'il n'y en as pas alors piocher
        - sinon pour chaque carte effectuer l'action associée'''

        self.botDeck.validCards(self.stack.getLast())

        self.__disablePlayer()

        card = self.__getFirstValidCard(self.botDeck)

        if card is None:
            self.botDeck = self.__takeCard(self.botDeck)
            return

        self.botDeck = self.__playCard(card, self.botDeck)

        if self.stack.getLast().symbol == Symbol.plus2:
            self.playerDeck = self.__takeCard(self.playerDeck, 2)

        if self.stack.getLast().symbol == Symbol.plus4:
            self.playerDeck = self.__takeCard(self.playerDeck, 4)

        if self.stack.getLast().isSkipCard():
            self.__skipTurn(self.botDeck, self.__botTurn)

        if self.stack.getLast().isJokerCard():
            color: Color = random.choice(list(Color)[:-1])
            self.stack.getLast().color = color

    def __playerTurn(self) -> bool:
        '''actions du joueur
        - activer les actions du joueur
        - s'il clique sur la pioche alors prendre une carte
        - s'il clique sur une carte jouable alors l'action
          associée à la carte est effectuée'''

        self.playerDeck.validCards(self.stack.getLast())

        self.__enablePlayer()

        self.wait_variable(self.checker)
        if self.checker.get() == -2:
            return False

        if self.checker.get() == -1:
            self.playerDeck = self.__takeCard(self.playerDeck)
            return True

        card: UNOCard = self.playerDeck[self.checker.get()]
        self.playerDeck = self.__playCard(card, self.playerDeck)

        if card.isSkipCard():
            self.__skipTurn(self.playerDeck, self.__playerTurn, False)

        if card.symbol == Symbol.plus2:
            self.botDeck = self.__takeCard(self.botDeck, 2)

        if card.symbol == Symbol.plus4:
            self.botDeck = self.__takeCard(self.botDeck, 4)

        if card.isJokerCard():
            self.playerDeck.disable()
            self.selector.activate(True)
            self.selector.enableAll()

            self.selector.wait_variable( self.selector.getValue())
            v = list(Color)[self.selector.getValue().get()]
            self.stack.getLast().color = v
            self.__delay(500)
            self.selector.disableAll()
            self.selector.activate(False)
            self.playerDeck.validCards(self.stack.getLast())

        return True

    def __takeCard(self, deck : Deck, n : int = 1) -> Deck:
        '''prendre n cartes dans la pioche et jouer le sample takecard.mp3
        si la pioche est vide alors elle est remplie avec le tas'''

        mixer.Channel(0).play(takeCardSound)
        if not(self.UNOdraw):
            self.UNOdraw = self.stack.copy()

        for i in range(n):
            card = self.UNOdraw.pop(0)
            card.disable()
            deck.append(card)
        self.__refreshGame()
        return deck

    def __playCard(self, cardPlayer, deckPlayer: Deck) -> Deck:
        '''retire une carte du deck, l'ajoute sur le tas
        et joue le sample playcard.mp3'''

        mixer.Channel(0).play(playCardSound)
        card: UNOCard = deckPlayer.remove(cardPlayer)
        self.stack.append(card)
        self.__refreshGame()
        return deckPlayer

    def __refreshGame(self) -> None:
        '''actualise le jeu'''

        self.__showDeck(PositionY.Bottom, self.playerDeck)
        self.__showDeck(PositionY.Top, self.botDeck, True)
        self.__showStack()
        self.__showDraw()
        self.__setHoverEvent()

    def __endGame(self) -> str:
        '''retourne le vainqueur et détruit les cartes'''

        self.__disablePlayer()
        out = 'player' if self.playerDeck.empty() else 'bot'
        self.__hideCard()
        return out

    def __setBackground(self) -> None:
        '''Affiche l'image d'arrière plan dans l'applivation'''

        self.background_image = PhotoImage(file='src/background.png')
        self.create_image((500, 450), image=self.background_image)

    def __disablePlayer(self) -> None:
        '''désactive les actions du joueur'''

        self.playerDeck.disable()
        for i in self.playerDeck: i.unbind('<Button>')
        self.drawCardImg.unbind('<Button>')

    def __enablePlayer(self) -> None:
        '''active les actions du joueur'''

        for i in range(len(self.playerDeck)):
            if self.playerDeck[i].isValid():
                self.playerDeck[i].bind(
                '<Button>', lambda e, j=i: self.checker.set(j),add='+'
                )

        self.drawCardImg.bind('<Button>', lambda e : self.checker.set(-1))

    def __getFirstValidCard(self, deck : Deck) -> UNOCard:
        '''retourne la première carte jouable sinon None'''

        return next((i for i in deck if i.isValid()), None)

    def __skipTurn(self, deck : Deck, func, delay = True) -> None:
        '''passe le tour avec possibilité d'ajout d'un délai'''

        self.__refreshGame()
        if delay: self.__delay(self.AMOUNT_OF_DELAY)
        if not deck.empty(): func()

    def __UNO(self, deck : Deck) -> None:
        '''vérifie s'il reste une carte dans un deck
        alors un popup UNO apparait pendant 1,4s
        et les samples 'uno.mp3' et 'unovoice.mp3' '''

        if len(deck) != 1: return

        mixer.Channel(1).play(unoSound)
        mixer.Channel(3).play(unoVoiceSound)

        self.uno = Canvas(
            self, width=490, height=340,
            highlightthickness=0, bg='#A6CF98'
        )
        self.unoImg = PhotoImage(file='src/UNO.png')
        self.uno.create_image((245,170), image=self.unoImg)
        self.uno.place(relx=.5, rely=.5,anchor= CENTER)
        self.__delay(self.AMOUNT_OF_DELAY * 2)
        self.uno.place_forget()

    def __setHoverEvent(self) -> None:
        ''''met en avant la carte survolé par la souris'''

        yPos = PositionY.Bottom.value
        shift = CardConstant.Shift.value
        for i in self.playerDeck:
            i.bind("<Enter>", lambda e,j=i: j.place(y=yPos-5))
            i.bind("<Leave>", lambda e,j=i: j.place(y=yPos))

        if len(self.playerDeck) <= self.MAX_CARDS_IN_ROW:
            return

        for i in range(len(self.playerDeck) % self.MAX_CARDS_IN_ROW):
            k = self.playerDeck[i]
            k.bind("<Enter>", lambda e, j=k: j.place(y=yPos-shift -5))
            k.bind("<Leave>", lambda e, j=k: j.place(y=yPos-shift))

    def __delay(self, time_us : int) -> None:
        '''marque une pause de x ms'''

        checker = IntVar()
        self.after(time_us, checker.set, 1)
        self.wait_variable(checker)

    def __showDraw(self) -> None:
        '''affiche la pioche'''

        self.drawCardImg.place(
            x = (ScreenSize.Width.value - CardConstant.Width.value-240)/2,
            y = PositionY.Center.value
        )

        self.drawCardImg.configure(bg='#9AD0C2')

    def __showStack(self) -> None:
        '''affiche la derniere carte posée sur le tas
        et retire tout les callbacks qui y sont liés'''

        for i in range(len(self.stack) - 1):
            self.stack[i].place_forget()

        self.stack.getLast().unbind("<Button>")
        self.stack.getLast().unbind("<Enter>")
        self.stack.getLast().unbind("<Leave>")
        self.stack.getLast().hide(False)
        self.stack.getLast().place(
            x = (ScreenSize.Width.value - CardConstant.Width.value + 240) / 2,
            y = PositionY.Center.value
        )
        self.stack.getLast().configure(bg='#9AD0C2')

    def __showCard(self, deck : Deck, index : int,
                   position : PositionY, shiftX : int = 0,
                   shiftY : int = 0, hidden : bool = False) -> Deck:
        '''positionne une carte a un index précis selon une position en y
        qui determine si sa place est au premier ou au deuxieme rang'''

        _x = (len(deck) - 1) * CardConstant.Shift.value
        _x += CardConstant.Width.value
        _x = (ScreenSize.Width.value - _x) / 2

        if hidden:
            deck[index].itemconfigure(deck[index].disableId, state='hidden')

        deck[index].hide(hidden)
        deck[index].place(
            x = _x  + (index - shiftX) * CardConstant.Shift.value,
            y = position.value - shiftY
        )
        deck[index].configure(bg='#557C55')
        return deck

    def __showDeck(self, position : PositionY,
        deck : Deck, hide : bool = False) -> None:
        '''Affiche un deck à une position y avec
        possibilité de de masquer les cartes'''
        length: int = len(deck)

        shiftY = -CardConstant.Shift.value
        if position.value != 0: shiftY = CardConstant.Shift.value
        if length < self.MAX_CARDS_IN_ROW: shiftY = 0

        iteration: int = length % self.MAX_CARDS_IN_ROW

        for i in range(iteration):
            deck = self.__showCard(deck, i, position, 0, shiftY, hide)

        if length < self.MAX_CARDS_IN_ROW : return

        for i in range(self.MAX_CARDS_IN_ROW):
            deck = self.__showCard(deck, i + iteration, position, iteration, 0, hide)

    def __hideCard(self) -> None:
        '''masque les cartes et les détruits'''
        self.stack.destroy()
        self.UNOdraw.destroy()
        self.drawCardImg.place_forget()