from tkinter import *
from constant import *

class ColorSelector(Canvas):

    def __init__(self, parent) -> None:

        self.bgColor : str = '#A6CF98'
        self.value = IntVar()

        self.l : list[Canvas] = [None] * 4
        self.corner : list[PhotoImage] = [None] * 4
        self.disableImg : list[PhotoImage] = [None] * 4
        self.disableId : list[int] = [None] * 4
        self.enableId : list[int] = [None] * 4

        Canvas.__init__(
            self, parent,
            height=250, width=250,
            highlightthickness=0, bg=self.bgColor
        )

        color : list[str] = ['Red', 'Green', 'Blue', 'Yellow']
        pos : list[tuple] = [(30, 33), (125, 128), (125, 33), (30, 128)]
        path : str = 'src/ColorSelection/'
        disableColor : list[str] = ['R', 'G', 'B', 'Y']

        for i in range(4):

            self.l[i] = Canvas(
                self, height=95, width=95,
                highlightthickness=0, bg=self.bgColor
            )

            self.disableImg[i] = PhotoImage(file=f'{path}disable{disableColor[i]}.png')
            self.corner[i] = PhotoImage(file=f'{path}{color[i]}.png')

            self.enableId[i] = self.l[i].create_image((47.5, 47.5), image=self.corner[i])
            self.disableId[i] = self.l[i].create_image((47.5, 47.5), image=self.disableImg[i])

            self.l[i].place(x=pos[i][0], y=pos[i][1])

        self.disableAll()

        self.place(
            x = ScreenSize.Width.value - 250,
            y = (ScreenSize.Height.value - 250) / 2
        )

    def activate(self, activate : bool):
        if activate:
            for i in range(4):
                self.l[i].bind('<Button>', lambda e, j=i: self.onClick(j))
        else:
            for i in range(4):
                self.l[i].unbind('<Button>')

    def onClick(self, index) -> None:
        '''activer la couleur cliquer et désactiver toutes les autres'''

        self.value.set(index)
        self.disableAll()
        self.enable(index)

    def getValue(self) -> int:
        '''renvoi la valeur de l'attribut value'''

        return self.value

    def disable(self, color : int, disable : bool = True) -> None:
        '''désactive une couleur'''

        a = 'normal' if disable else 'hidden'
        self.l[color].itemconfigure(self.disableId[color], state=a)

    def enable(self, color : int, enable : bool = True) -> None:
        '''active une couleur'''

        self.disable(color, not(enable))

    def disableAll(self, disable : bool = True) -> None:
        '''désactive toutes les couleurs'''

        for i in range(4):
            self.disable(i, disable)

    def enableAll(self, enable : bool = True) -> None:
        '''active toutes les couleurs'''

        self.disableAll(not(enable))
