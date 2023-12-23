from unocard import *

class Deck(list):

    def destroy(self):
        '''detruit toutes les cartes du deck'''

        for i in self:
            i.place_forget()
            i.pack_forget()
        self.clear()

    def validCards(self, card : UNOCard) -> None:
        '''vérifie qu'une carte jouable est dans le
        deck par rapport a une carte donnée'''

        self.disable()

        for i in self:
            sameColor: bool = i.isSameColor(card)
            sameSymbol: bool = i.isSameSymbol(card)
            playerJokerCard: bool = i.isJokerCard()

            if sameSymbol: i.enable()
            elif sameColor: i.enable()
            elif playerJokerCard: i.enable()

    def getLast(self) -> UNOCard:
        '''renvoie le dernier element du deck'''

        return self[-1]

    def empty(self) -> bool:
        '''indique si le deck est vide'''

        return not(self)

    def getIndex(self, card : UNOCard) -> int:
        '''renvoi l'indice d'une carte si elle existe dans le deck'''

        index = 0
        for i in self:
            if i == card:
                return index
            index+=1
        return None

    def remove(self, card : UNOCard) -> UNOCard:
        '''retire une carte donnée du deck'''

        index: int = self.getIndex(card)
        if not(index == None):
            return self.pop(index)
        return None

    def disable(self) -> None:
        '''désactive toutes les cartes'''

        for i in self:
            i.disable()
