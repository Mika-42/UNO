from enum import *

#@verify(UNIQUE) # uncomment only if python > python 3.7
class ScreenSize(Enum):
    '''Dimensions de la fenetre de l'app'''

    Width = 1000
    Height = 900

#@verify(UNIQUE) # uncomment only if python > python 3.7
class CardConstant(Enum):
    '''dimensions usuelles des cartes'''

    Width = 140
    Height = 230
    HalfWidth = Width / 2
    HalfHeight = Height / 2
    Shift = 40

#@verify(UNIQUE) # uncomment only if python > python 3.7
class Color(Enum):
    Red = 'red_bg_card.png'
    Green = 'green_bg_card.png'
    Blue = 'blue_bg_card.png'
    Yellow = 'yellow_bg_card.png'
    Black = 'black_bg_card.png'

#@verify(UNIQUE) # uncomment only if python > python 3.7
class Symbol(Enum):
    n0 = '0.png'
    n1 = '1.png'
    n2 = '2.png'
    n3 = '3.png'
    n4 = '4.png'
    n5 = '5.png'
    n6 = '6.png'
    n7 = '7.png'
    n8 = '8.png'
    n9 = '9.png'
    plus2 = 'plus2.png'
    inv = 'inv.png'
    skip = 'skip.png'
    joker = 'joker.png'
    plus4 = 'plus4.png'
    back = 'back.png'
    disable = 'disable.png'

#@verify(UNIQUE) # uncomment only if python > python 3.7
class PositionY(Enum):
    '''positionnement usuel en Y'''
    
    Top = 0
    Bottom = ScreenSize.Height.value - CardConstant.Height.value
    Center = Bottom / 2
