from tkinter import *
from unoparty import *

class ScoreBoard(Canvas):
    def __init__(self, parent) -> None:
        Canvas.__init__(
            self, parent,
            width=120,
            height=190,
            highlightthickness=0,
            bg='#FA7070'
        )

        self.score = StringVar(value='0')

        self.pack_propagate(0)
        self.scoreLabel = Label(
            self,
            height=190,
            font=('Cabin', 50),
            bg='#FA7070',
            fg='white',
            textvariable=self.score
        )
        self.scoreLabel.pack()

    def plus1(self) -> None:
        '''incremente le score de 1'''
        self.score.set(int(self.score.get()) + 1)

class mainWindow(Tk):
    def __init__(self) -> None:
        Tk.__init__(self)
        self.title('UNO')
        self.geometry(f'{ScreenSize.Width.value}x{ScreenSize.Height.value}')
        self.resizable(width=0, height=0)

        self.uno = UNOParty(self)
        self.uno.pack()

        self.playBtn = Canvas(
            self, width=300, height=153,
            highlightthickness=0, bg ='#A6CF98'
        )
        self.playImg = PhotoImage(file='src/play.png')
        self.playBtn.create_image((150, 76), image = self.playImg)
        self.playBtn.place(
            x=(ScreenSize.Width.value - 300) / 2,
            y = (ScreenSize.Height.value - 153) / 2
        )

        self.botScore = ScoreBoard(self.uno)
        self.botScore.place(x=0, y=400)

        self.playerScore = ScoreBoard(self.uno)
        self.playerScore.place(x=140, y=400)

        mixer.Channel(4).play(music, loops=-1)

        self.playBtn.bind('<Button>', lambda e: self.launchGame())

        #ATTENTION CODE NON PORTABLE#
        #fonctionne UNIQUEMENT sous Windows
        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self) -> None:
        '''ferme l'application'''

        self.uno.interupt()
        music.stop()
        self.quit()
        self.destroy()

    def launchGame(self) -> None:
        '''lance le jeu quand le bouton play est cliqué'''

        mixer.Channel(0).play(playCardSound)
        self.playBtn.place_forget()
        self.uno.setupGame()
        winner: str = self.uno.loop()

        if winner == 'exit': return
        elif winner == 'player':
            mixer.Channel(2).play(winSound)
            self.playerScore.plus1()
        else:
            mixer.Channel(2).play(failSound)
            self.botScore.plus1()

        self.playBtn.place(
            x=(ScreenSize.Width.value - 300) / 2,
            y = (ScreenSize.Height.value - 153) / 2
        )

uno = mainWindow()
uno.mainloop()
