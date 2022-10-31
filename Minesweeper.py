import tkinter as TKI
import random as RNG
import time

DEBUG = True

class Minesweeper:
    def __init__(self):
        self.W = 264
        self.H = 275

        self.Colors = [
            "#FFFFFF",
            "#0000FF",
            "#00CC00",
            "#FF0000",
            "#DD00DD",
            "#CCCC00",
            "#00BBBB",
            "#000000",
            "#FBFBFB"
            ]

        self.TK = TKI.Tk()
        self.TK.title("TKI Minesweeper")
        self.TK.geometry(f"{self.W}x{self.H}")
        self.TK.resizable(0, 0)
        self.CreateGUIElements()
        self.PlaceGUIElements()
        self.ConfigureGUIElements()

        self.Gewonnen   = False
        self.Verloren   = False
        self.Running    = False
        self.Bomben     = 0

        self.Feld       = False
        self.Grid       = []

        self.SliderX    = 0
        self.SliderY    = 0
        self.SliderS    = 0

        self.FeldW      = 0
        self.FeldH      = 0

        self.YX         = []
        self.Recursiv   = []

    def CreateGUIElements(self):
        self.MinesweeperLabel   = TKI.Label(self.TK, text = "TKI Minesweeper", font = ("Helvetica", 24), justify = "center")
        self.XAchseLabel        = TKI.Label(self.TK, text = "X - Achse:", font = ("Helvetica", 16), justify = "center")
        self.XAchse             = TKI.Scale(self.TK, orient = "horizontal", from_ = 1, to = 1, sliderlength = 24, length = 1)
        self.YAchseLabel        = TKI.Label(self.TK, text = "Y - Achse:", font = ("Helvetica", 16), justify = "center")
        self.YAchse             = TKI.Scale(self.TK, orient = "horizontal", from_ = 1, to = 1, sliderlength = 24, length = 1)
        self.SchwierigkeitLabel = TKI.Label(self.TK, text = "Schwierigkeit:", font = ("Helvetica", 16), justify = "center")
        self.Schwierigkeit      = TKI.Scale(self.TK, orient = "horizontal", from_ = 1, to = 1, sliderlength = 24, length = 1, resolution = 0.1)
        self.Start              = TKI.Button(self.TK, text = "Start", font = ("Helvetica", 16, "bold"))
        self.Clear              = TKI.Button(self.TK, text = "Reset", font = ("Helvetica", 16, "bold"), fg = "#DD0000", state = "disabled")

    def PlaceGUIElements(self):
        self.MinesweeperLabel.place(x = 6, y = 6)
        self.XAchseLabel.place(x = 10, y = 60)
        self.XAchse.place(x = 116, y = 45)
        self.YAchseLabel.place(x = 10, y = 100)
        self.YAchse.place(x = 116, y = 85)
        self.SchwierigkeitLabel.place(x = 10, y = 140)
        self.Schwierigkeit.place(x = 151, y = 125)
        self.Start.place(x = 92, y = 180, width = 80)
        self.Clear.place(x = 92, y = 227, width = 80)

        self.XAchse.configure(length = 133)
        self.YAchse.configure(length = 133)
        self.Schwierigkeit.configure(length = 98)

    def ConfigureGUIElements(self):
        if DEBUG:
            self.XAchse.configure(from_ = 1)
            self.XAchse.configure(to = 80)
            self.YAchse.configure(from_ = 1)
            self.YAchse.configure(to = 45)
            self.Schwierigkeit.configure(from_ = 0)
            self.Schwierigkeit.configure(to = 5)
        else:
            self.XAchse.configure(from_ = 3)
            self.XAchse.configure(to = 32)
            self.YAchse.configure(from_ = 3)
            self.YAchse.configure(to = 32)
            self.Schwierigkeit.configure(from_ = 0.5)
            self.Schwierigkeit.configure(to = 2)

        self.XAchse.set(12)
        self.YAchse.set(12)
        self.Schwierigkeit.set(1)

        self.Start.configure(command = self.StartCallback)
        self.Clear.configure(command = self.ClearCallback)

    def CreateGrid(self):
        for c in range(self.SliderX):
            self.Feld.create_line(((c * 26) + 3), 0, ((c * 26) + 3), ((26 * self.SliderY) + 3))
        for c in range(self.SliderY):
            self.Feld.create_line(0, ((c * 26) + 3), ((26 * self.SliderX) + 3), ((c * 26) + 3))
        for iY in range(self.SliderY):
            for iX in range(self.SliderX):
                self.Grid[iY][iX] = self.Feld.create_rectangle(((iX * 26) + 7), ((iY * 26) + 7), ((iX * 26) + 25), ((iY * 26) + 25), fill = "#b0b0b0", outline = "#b0b0b0")

    def StartCallback(self):
        self.XAchse.config(state = "disabled", sliderlength = 0)
        self.XAchseLabel.config(state = "disabled")
        self.YAchse.config(state = "disabled", sliderlength = 0)
        self.YAchseLabel.config(state = "disabled")
        self.Schwierigkeit.config(state = "disabled", sliderlength = 0)
        self.SchwierigkeitLabel.config(state = "disabled")
        self.Start.config(state = "disabled")
        self.Clear.config(state = "normal")

        self.SliderX    = int(self.XAchse.get())
        self.SliderY    = int(self.YAchse.get())
        self.SliderS    = float(self.Schwierigkeit.get())

        self.FeldW = (261 + (26 * self.SliderX) + 6)
        if (26 * self.SliderY) > self.H:
            self.FeldH = (26 * self.SliderY + 7)
        else:
            self.FeldH = self.H
        self.TK.geometry(f"{self.FeldW}x{self.FeldH}")

        self.Grid   = [[0 for dummyX in range(self.SliderX)] for dummyY in range(self.SliderY)] 

        self.Feld = TKI.Canvas(self.TK, bd = 2, bg = "#e0e0e0", width = ((26 * self.SliderX) - 1), height = (26 * self.SliderY), relief = "ridge")
        self.Feld.place(x = 261, y = 0)
        self.Feld.bind("<Button-1>", self.MausLinks)
        self.Feld.bind("<Button-2>", self.MausMitte)
        self.Feld.bind("<Button-3>", self.MausRechts)

        self.CreateGrid()

    def EventChecker(self, event):
        if event.x >= ((self.SliderX * 26) + 3):
            X = ((self.SliderX * 26) + 2)
        elif event.x <= 3:
            X = 3
        else:
            X = event.x

        if event.y >= ((self.SliderY * 26) + 3):
            Y = ((self.SliderY * 26) + 2)
        elif event.y <= 3:
            Y = 3
        else:
            Y = event.y

        return [((Y - 3) // 26), ((X - 3) // 26)]

    def MausLinks(self, event):
        Y, X = self.EventChecker(event)
        if not self.Bomben:
            self.BombenLegen(Y, X)
            self.SpielfeldBewerten()
            self.Running = True
        if self.YX[Y][X] <= 9 and self.Running:
            self.YX[Y][X] += 10
            self.Feld.delete(self.Grid[Y][X])
            if self.YX[Y][X] == 19:
                self.Verloren   = True
                self.Running    = False
                self.Grid[Y][X] = self.Feld.create_oval(((X * 26) + 7), ((Y * 26) + 7), ((X * 26) + 25), ((Y * 26) + 25), fill = "#000000", outline = "#000000")
            elif self.YX[Y][X] == 10:
                self.Aufdecken(Y, X)
            else:
                self.Grid[Y][X] = self.Feld.create_text(((X * 26) + 16), ((Y * 26) + 16), text = str(self.YX[Y][X] - 10), fill = self.Colors[self.YX[Y][X] - 10], font = ("Helvetica", 20))

    def MausMitte(self, event):
        Y, X = self.EventChecker(event)
        if self.Running and (self.YX[Y][X] // 10) in [0, 2]:
            self.Feld.delete(self.Grid[Y][X])
            if self.YX[Y][X] <= 9:
                self.YX[Y][X] += 20
                self.Grid[Y][X] = self.Feld.create_text(((X * 26) + 16), ((Y * 26) + 16), text = "?", fill = "#00CC00", font = ("Helvetica", 20))
            else:
                self.YX[Y][X] -= 20
                self.Grid[Y][X] = self.Feld.create_rectangle(((X * 26) + 7), ((Y * 26) + 7), ((X * 26) + 25), ((Y * 26) + 25), fill = "#b0b0b0", outline = "#b0b0b0")

    def MausRechts(self, event):
        Y, X = self.EventChecker(event)
        if self.Running and (self.YX[Y][X] // 10) in [0, 3]:
            self.Feld.delete(self.Grid[Y][X])
            if self.YX[Y][X] <= 9:
                self.YX[Y][X] += 30
                self.Grid[Y][X] = self.Feld.create_polygon(((X * 26) + 16), ((Y * 26) + 3), ((X * 26) + 10), ((Y * 26) + 16), ((X * 26) + 16), ((Y * 26) + 29), ((X * 26) + 22), ((Y * 26) + 16), fill = "#FF0000", outline = "#FF0000")
            else:
                self.YX[Y][X] -= 30
                self.Grid[Y][X] = self.Feld.create_rectangle(((X * 26) + 7), ((Y * 26) + 7), ((X * 26) + 25), ((Y * 26) + 25), fill = "#b0b0b0", outline = "#b0b0b0")

    def Aufdecken(self, Y, X):
        self.Recursiv.append([Y, X])
        while self.Recursiv:
            Y, X = self.Recursiv[-1]
            JumpOut = False
            for cX in [-1, 0, 1]:
                if JumpOut:
                    break
                for cY in [-1, 0, 1]:
                    if JumpOut:
                        break
                    if (X + cX) >= 0 and (X + cX) < self.SliderX and (Y + cY) >= 0 and (Y + cY) < self.SliderY and self.YX[(Y + cY)][(X + cX)] <= 8:
                        if cY == 0 and cX == 0:
                            pass
                        else:
                            self.YX[(Y + cY)][(X + cX)] += 10
                            self.Feld.delete(self.Grid[(Y + cY)][(X + cX)])
                            if self.YX[(Y + cY)][(X + cX)] == 10:
                                self.Recursiv.append([(Y + cY), (X + cX)])
                                JumpOut = True
                                break
                            else:
                                self.Grid[(Y + cY)][(X + cX)] = self.Feld.create_text((((X + cX) * 26) + 16), (((Y + cY) * 26) + 16), text = str(self.YX[(Y + cY)][(X + cX)] - 10), fill = self.Colors[self.YX[(Y + cY)][(X + cX)] - 10], font = ("Helvetica", 20))
            if not JumpOut:
                self.Recursiv.pop()

    def SpielfeldBewerten(self):
        for iX in range(self.SliderX):
            for iY in range(self.SliderY):
                if self.YX[iY][iX] == 0:
                    BombenNebenan = 0
                    for cX in [-1, 0, 1]:
                        for cY in [-1, 0, 1]:
                            if (iX + cX) >= 0 and (iX + cX) < self.SliderX and (iY + cY) >= 0 and (iY + cY) < self.SliderY:
                                if self.YX[(iY + cY)][(iX + cX)] == 9:
                                    BombenNebenan += 1
                    self.YX[iY][iX] = BombenNebenan

    def BombenLegen(self, Y, X):
        VerteilungErfolgreich = False
        BombenZiel = min((self.SliderX * self.SliderY * 0.15625 * self.SliderS), (self.SliderX * self.SliderY - 1))
        while not VerteilungErfolgreich:
            self.YX = [[0 for dummyX in range(self.SliderX)] for dummyY in range(self.SliderY)] 
            self.Bomben = 0
            while self.Bomben < BombenZiel:
                YC = RNG.randint(0, (self.SliderY - 1))
                XC = RNG.randint(0, (self.SliderX - 1))
                if self.YX[YC][XC] == 0:
                    self.YX[YC][XC] = 9
                    self.Bomben += 1
            if self.YX[Y][X] == 0:
                VerteilungErfolgreich = True

    def ClearCallback(self):
        if self.Feld:
            self.Feld.destroy()
        self.Grid = []

        self.XAchse.config(state = "normal", sliderlength = 24)
        self.XAchseLabel.config(state = "normal")
        self.YAchse.config(state = "normal", sliderlength = 24)
        self.YAchseLabel.config(state = "normal")
        self.Schwierigkeit.config(state = "normal", sliderlength = 24)
        self.SchwierigkeitLabel.config(state = "normal")
        self.Start.config(state = "normal")
        self.Clear.config(state = "disabled")
        self.TK.geometry(f"{self.W}x{self.H}")

        self.Gewonnen       = False
        self.Verloren       = False
        self.Running        = False
        self.Bomben         = 0

if __name__ == "__main__":
    MS = Minesweeper()
    MS.TK.mainloop()