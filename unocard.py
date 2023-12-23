from constant import *
from tkinter import *

class UNOCard(Canvas):

    def __init__(self, parent, symbol: Symbol, color: Color) -> None:

        Canvas.__init__(
            self, parent,
            height=CardConstant.Height.value,
            width=CardConstant.Width.value,
            highlightthickness=0,
            bg = '#557C55'
        )

        self.symbol: Symbol = symbol
        self.color: Color = color
        self.disableState : bool = None

        bgPath : str = 'src/background/'
        smblPath : str = 'src/symbol/'

        self.background = PhotoImage(file=f'{bgPath}{self.color.value}')
        self.symbolCard = PhotoImage(file=f'{smblPath}{self.symbol.value}')
        self.backCard = PhotoImage(file=f'{smblPath}{Symbol.back.value}')
        self.disableFilter = PhotoImage(file=f'{bgPath}{Symbol.disable.value}')

        w : int = CardConstant.HalfWidth.value
        h : int = CardConstant.HalfHeight.value

        self.backwardId: int = self.create_image((w, h), image=self.background)
        self.forwardId: int = self.create_image((w, h), image=self.symbolCard)
        self.backId: int = self.create_image((w, h), image=self.backCard)
        self.disableId: int = self.create_image((w, h), image=self.disableFilter)

        self.disable(False)

    def __eq__(self, card) -> bool:
        '''verifie que deux cartes sont identiques'''

        return self.isSameColor(card) and self.isSameSymbol(card)

    def isValid(self) -> bool:
        '''renvoi l'état de l'attribut disableState'''

        return self.disableState

    def isSpecialCard(self) -> bool:
        '''indique si la carte est un +2, inv ou skip'''

        return self.symbol in [Symbol.plus2, Symbol.inv , Symbol.skip]

    def isJokerCard(self) -> bool:
        '''indique si la carte est un +4 ou un joker'''

        return self.symbol in [Symbol.joker, Symbol.plus4]

    def isSkipCard(self) -> bool:
        '''indique si la carte est skip ou inv'''

        return self.symbol in [Symbol.skip, Symbol.inv]

    def hide(self, hidden : bool = True) -> None:
        '''affiche le dos de la carte'''

        a, b = ('hidden', 'normal') if hidden else ('normal', 'hidden')

        self.itemconfigure(self.forwardId, state=a)
        self.itemconfigure(self.backId, state=b)

    def disable(self, disable = True) -> None:
        '''rend la carte non jouable'''

        a = 'normal' if disable else 'hidden'
        self.itemconfigure(self.disableId, state=a)
        self.disableState = not(disable)

    def enable(self, enable = True) -> None:
        '''rend la carte jouable'''

        self.disable(not enable)

    def isDisable(self) -> bool:
        return self.cget('state') == 'normal'

    def isSameColor(self, card) -> bool:
        return self.color == card.color

    def isSameSymbol(self, card) -> bool:
        return self.symbol == card.symbol
