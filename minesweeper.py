import tkinter, tkinter.ttk, random, os, tkinter.messagebox, tkinter.simpledialog, tkinter.font as font
from operator import add, sub

root = tkinter.Tk()
root.resizable(width=False, height=False)
root.title("Minesweeper")


# Global variables initialization
rows = 9
columns = 9
mines = 10
field = []
buttons = []
isGameOver = False

# Cell colors
colors = ['#FFFFFF', '#0000FF', '#1688FF', '#FF0000', '#000084', '#F60237', '#FFC600', '#FF0085', '#5C0500', "#8AC3FF", '#000000', '#6D6D6D']
        #activategdbg,   1,         2,          3,        4,        5,          6,          7,        8,      closedbg,    mine,      flag
# Font
myFont = font.Font(family='Arial', weight="bold")
# Path
saveDir = os.path.dirname(os.path.abspath(__file__)) + r'\Saves\\'
if not os.path.exists(saveDir): os.makedirs(saveDir)

root.protocol("WM_DELETE_WINDOW", lambda: saveAndQuit())

def saveAndQuit():
    if not isGameOver:
        File.saveGameField(File)
    root.destroy()

def setColors(theme):
    global colors
    if theme == 'darkpink':
        colors = ['#30102D', '#00F1F2', '#007BFC', '#E4266C', '#B15EDE', '#6E3A7C', '#D862C1', '#003399', '#003399', '#16090F', '#CF4EAB', '#FF005D']
    elif theme == 'darklava':
        colors = ['#FF8A00', '#330000', '#A60000', '#1A0000', '#16090F', '#911710', '#3B003B', '#FFFFFF', '#FFD900', '#1A0000', '#E2A35C', '#FF4900']
    elif theme == 'lightlime':
        colors = ['#FFFFFF', '#31A100', '#4B7000', '#FF0000', '#000084', '#0E499F', '#0B2F4A', '#0B4A35', '#0672E3', "#BDDE48", '#000000', '#005E70']
    else:
        colors = ['#FFFFFF', '#0000FF', '#1688FF', '#FF0000', '#000084', '#F60237', '#FFC600', '#FF0085', '#5C0500', "#8AC3FF", '#000000', '#6D6D6D']
    for x in range(rows):
        for y in range(columns):
            if buttons[x][y]["state"] == "normal" or buttons[x][y]["text"] == "⚑" or buttons[x][y]["text"] == "?":
                buttons[x][y].config(bg=colors[9])
                buttons[x][y].config(disabledforeground=colors[11])
            elif buttons[x][y]["text"] == "✱":
                buttons[x][y].config(disabledforeground=colors[10])
                buttons[x][y].config(bg=colors[0])
            else:
                buttons[x][y].config(bg=colors[0])
                buttons[x][y].config(disabledforeground=colors[field[x][y]])

def createMenu():
    """This creates context menus"""

    menuField = tkinter.Menu(root, tearoff=0)
    menuField.add_command(label="Easy: 9х9, 10 мин", command=lambda: setSize(9, 9, 10))
    menuField.add_command(label="Normal: 16х16, 40 мин", command=lambda: setSize(16, 16, 40))
    menuField.add_command(label="Hard: 16х30, 99 мин", command=lambda: setSize(16, 30, 99))

    menuTheme = tkinter.Menu(root, tearoff=0)
    menuTheme.add_command(label="Light", command=lambda: setColors('light'))
    menuTheme.add_command(label="Light Lime", command=lambda: setColors('lightlime'))
    menuTheme.add_command(label="Dark Pink&Blue", command=lambda: setColors('darkpink'))
    menuTheme.add_command(label="Dark Lava", command=lambda: setColors('darklava'))

    menuBar = tkinter.Menu(root)
    menuBar.add_cascade(label="Field", menu=menuField)
    menuBar.add_command(label="Rating", command=lambda: showRating())
    menuBar.add_cascade(label="Theme", menu=menuTheme)
    menuBar.add_command(label="Quit", command=lambda: saveAndQuit())
    root.config(menu=menuBar)


def composeRating(lineNumber):
    """This creates a player rating"""

    textFiles = [f for f in os.listdir(saveDir) if f.endswith('_save.txt')]
    ratingArr = []
    for file in textFiles:
        with open(saveDir + str(file), "r") as playerSave:
            playerSave.seek(0)
            lines = playerSave.readlines()
            try: ratingArr.append(lines[lineNumber].replace('[', '').replace(']', '').replace('\n', '').split(' '))
            except IndexError: pass
    return ratingArr

def showRating():
    """This calls a new window with a player rating"""

    ratingWindow = tkinter.Toplevel(root)
    ratingWindow.resizable(width=False, height=False)
    ratingWindow.title("Player Rating")
    tabs = tkinter.ttk.Notebook(ratingWindow)
    beginner = tkinter.ttk.Frame(tabs)
    intermediate = tkinter.ttk.Frame(tabs)
    expert = tkinter.ttk.Frame(tabs)
    tabs.add(beginner, text="Easy")
    tabs.add(intermediate, text="Normal")
    tabs.add(expert, text="Hard")

    tkinter.Label(beginner, text=recordRating(composeRating(2), beginner, 5)).grid(column=2, row=0)
    tkinter.Label(intermediate, text=recordRating(composeRating(3), intermediate, 6)).grid(column=2, row=0)
    tkinter.Label(expert, text=recordRating(composeRating(4), expert, 7)).grid(column=2, row=0)
    tabs.pack(expand=1, fill="both")

def recordRating(resultsArr, tab, lastResLineNumber):
    """This generates the rating"""

    namesArr = []
    lastResArr = []
    rating = []

    textFiles = [f for f in os.listdir(saveDir) if f.endswith('_save.txt')]
    for file in textFiles:
        with open(saveDir + str(file), "r") as playerSave:
            playerSave.seek(0)
            lines = playerSave.readlines()
            name = lines[0].replace("Name: ", '').replace("\n", '')
            try: lastResArr.append(float(lines[lastResLineNumber].replace("\n", '')))
            except IndexError: lastResArr.append(0.0)
            namesArr.append(name)

    for i, result in enumerate(resultsArr):
        resultPercentage = File.calculateRating(File, result, lastResArr[i])
        rating.append(namesArr[i] + " : " + str(resultPercentage) + "%")
    for n, row in enumerate(rating):
        tkinter.Button(tab, text=row.split(':', 1)[0], command=lambda row=row:specifyRating(row)).grid(column=0, row=n, ipadx=30, sticky="ew")
        tkinter.Label(tab, text=row.split(':', 1)[1]).grid(column=1, row=n, sticky='ew')

def specifyRating(name):
    """This generates a rating for a specific player"""

    userName = name.split(' :', 1)[0]
    userRating = tkinter.Toplevel(root)
    userRating.resizable(width=False, height=False)
    userRating.title(userName)

    with open((saveDir + userName + "_save.txt"), "r+") as playerSave:
        lines = playerSave.readlines()
        try: bLastResult = lines[5].replace('\n', '')
        except IndexError: bLastResult = 0.0
        try: iLastResult = lines[6].replace('\n', '')
        except IndexError: iLastResult = 0.0
        try: eLastResult = lines[7].replace('\n', '')
        except IndexError: eLastResult = 0.0
    try:
        bResults = lines[2].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
    except IndexError:
        bResults = []
    try:
        iResults = lines[3].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
    except IndexError:
        iResults = []
    try:
        eResults = lines[4].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
    except IndexError:
        eResults = []

    tkinter.Label(userRating, text='Player results ' + userName + ': ').grid(column=0, row=0, ipadx=50)
    tkinter.Label(userRating, text='Easy: ' + str(File.calculateRating(File, bResults, float(bLastResult)))+'%').grid(column=0, row=1, ipadx=50)
    tkinter.Label(userRating, text='Normal: ' + str(File.calculateRating(File, iResults, float(iLastResult)))+'%').grid(column=0, row=2, ipadx=50)
    tkinter.Label(userRating, text='Hard: ' + str(File.calculateRating(File, eResults, float(eLastResult)))+'%').grid(column=0, row=3, ipadx=50)


def setSize(r, c, m):
    """This reloads the game field with new parameters"""

    global rows, columns, mines
    rows = r
    columns = c
    mines = m
    restartGame()

def prepareGame():
    """This generates a game field"""

    global rows, columns, mines, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, columns):
            field[x].append(0)
    for _ in range(0, mines):
        x = random.randint(0, rows - 1)
        y = random.randint(0, columns - 1)
        while field[x][y] == 9:
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)
        field[x][y] = 9
        valueGeneration(x, y, add)

def valueGeneration(x, y, op):
    """This generates mines"""

    if x != 0:
        if y != 0:
            if field[x - 1][y - 1] != 9:
                field[x - 1][y - 1] = op(int(field[x - 1][y - 1]), 1)
        if field[x - 1][y] != 9:
            field[x - 1][y] = op(int(field[x - 1][y]), 1)
        if y != columns - 1:
            if field[x - 1][y + 1] != 9:
                field[x - 1][y + 1] = op(int(field[x - 1][y + 1]), 1)
    if y != 0:
        if field[x][y - 1] != 9:
            field[x][y - 1] = op(int(field[x][y - 1]), 1)
    if y != columns - 1:
        if field[x][y + 1] != 9:
            field[x][y + 1] = op(int(field[x][y + 1]), 1)
    if x != rows - 1:
        if y != 0:
            if field[x + 1][y - 1] != 9:
                field[x + 1][y - 1] = op(int(field[x + 1][y - 1]), 1)
        if field[x + 1][y] != 9:
            field[x + 1][y] = op(int(field[x + 1][y]), 1)
        if y != columns - 1:
            if field[x + 1][y + 1] != 9:
                field[x + 1][y + 1] = op(int(field[x + 1][y + 1]), 1)

def prepareWindow():
    """This fills the field with buttons"""

    global rows, columns, buttons
    buttons = []
    firstClickHappened = False
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, columns):
            b = tkinter.Button(root, text=" ", bg=colors[9], pady=0, padx=0, width=2, font=myFont, borderwidth=0, command=lambda x=x, y=y: Cell.clickOn(Cell, x, y)) #clickOn(x, y)
            b.bind("<Button-3>", lambda e, x=x, y=y: Cell.onRightClick(Cell, x, y))
            b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            buttons[x].append(b)


def restartGame():
    """This reloads the game"""

    global isGameOver
    isGameOver = False
    for x in root.winfo_children():
        if type(x) != tkinter.Menu and x != Player.p:
            x.destroy()
    Player.p.config(text=Player.faces[0])
    Player.p.grid(row=0, column=0, columnspan=columns, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
    Cell.firstClickHappened = False
    prepareWindow()
    prepareGame()


def checkWin():
    """This checks if all mine buttons are closed"""

    global buttons, field, rows, columns, isGameOver
    win = True
    for x in range(0, rows):
        for y in range(0, columns):
            if field[x][y] != 9 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        File.saveResults(File, True)
        isGameOver = True
        os.remove(saveDir + File.playerName + "_game.bin")
        os.remove(saveDir + File.playerName + "_cells.bin")
        Player.p.config(text=Player.faces[2])
        tkinter.messagebox.showinfo("Victory!", "Good job!!")


# CLASSES:

class File:
    playerName = ''     # Player name
    playerPass = ''     # Player password
    resultCount = 0     # Game count
    bResults = []       # 10 last Easy results
    iResults = []       # 10 last Normal results
    eResults = []       # 10 last Hard results
    bLastRating = 0     # Rating based on 10 last Easy results
    iLastRating = 0     # Rating based on 10 last Normal results
    eLastRating = 0     # Rating based on 10 last Hard results
    mode = 'Easy'    # Current difficulty mode
    authWindow = tkinter.Toplevel(root, pady=20, padx=20)

    def deterMode(self):
        """This resets the difficulty level"""

        if mines == 99: self.mode = 'Hard'
        elif mines == 40: self.mode = 'Normal'
        else: self.mode = 'Easy'
        return self.mode

    def playerAuth(self):
        """This is for login and auth"""

        authWindow = self.authWindow
        authWindow.grab_set()
        authWindow.lift(root)
        authWindow.resizable(width=False, height=False)
        authWindow.title("Authorization")
        authWindow.protocol("WM_DELETE_WINDOW", lambda: "pass")

        tkinter.Label(authWindow, text="Welcome! \n Enter your name and password!").pack()
        tkinter.Label(authWindow, text="Name: ").pack()
        playerName = tkinter.Entry(authWindow)
        playerName.pack()
        tkinter.Label(authWindow, text="Password: ").pack()
        playerPass = tkinter.Entry(authWindow)
        playerPass.pack()
        a = tkinter.Button(authWindow, text="Let's go!", command=lambda: File.closeAuth(self, playerName, playerPass))
        b = tkinter.Button(authWindow, text="Quit", command=lambda: root.destroy())
        a.pack(side="left", pady=10, padx=27)
        b.pack(side="left", pady=10, padx=1)

    def closeAuth(self, playerName, playerPass):
        """This checks if player file exists and if not - creates a file"""

        name = str(playerName.get())
        passw = str(playerPass.get())
        self.playerPass = passw
        self.playerName = name

        if os.path.exists(saveDir + name + "_save.txt"):
            with open((saveDir + name + "_save.txt"), "r+") as playerSave:
                playerSave.seek(0)
                lines = playerSave.readlines()
                try:
                    self.bResults = lines[2].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
                except IndexError:
                    self.bResults = []
                try:
                    self.iResults = lines[3].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
                except IndexError:
                    self.iResults = []
                try:
                    self.eResults = lines[4].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
                except IndexError:
                    self.eResults = []

                try: self.bLastRating = lines[5].replace('\n', '')
                except IndexError: self.bLastRating = 0.0
                try: self.iLastRating = lines[6].replace('\n', '')
                except IndexError: self.iLastRating = 0.0
                try:self.eLastRating = lines[7].replace('\n', '')
                except IndexError: self.eLastRating = 0.0
        else:
            self.bResults = []
            self.iResults = []
            self.eResults = []

        if os.path.exists(saveDir + name + "_save.txt"):
            with open((saveDir + name + "_save.txt"), "r+") as playerSave:
                content = playerSave.readlines()
                password = content[1]
                if passw in password:
                    File.loadGameField(File)
                    self.authWindow.destroy()
                else: tkinter.messagebox.showinfo("Oops!", "Wrong password")
        else:
            with open((saveDir + name + "_save.txt"), "w+") as playerSave:
                playerSave.write("Name: " + name + '\n')
                playerSave.write("Password: " + passw + '\n')
                self.authWindow.destroy()

    def saveResults(self, didPlayerWin):
        """This controls how many game results are saved
        (no more than 10 can exist at the same time)"""

        self.mode = File.deterMode(self)
        if self.mode == "Easy": resultsArr = self.bResults
        elif self.mode == "Normal": resultsArr = self.iResults
        else: resultsArr = self.eResults

        if didPlayerWin: resultsArr.append("1")
        else: resultsArr.append("0")
        if len(resultsArr) >= 10:
            self.shiftLeft(self, resultsArr)
        with open((saveDir + self.playerName + "_save.txt"), "w+") as playerSave:
            playerSave.write("Name: " + self.playerName + '\n')
            playerSave.write("Password: " + self.playerPass + '\n')
            playerSave.write(str(self.bResults) + '\n')
            playerSave.write(str(self.iResults) + '\n')
            playerSave.write(str(self.eResults) + '\n')
            playerSave.write(str(self.bLastRating) + '\n')
            playerSave.write(str(self.iLastRating) + '\n')
            playerSave.write(str(self.eLastRating) + '\n')

    def shiftLeft(self, lst):
        res = self.calculateRating(File, lst, 0.0)
        if self.mode == 'Easy': self.bLastRating = res
        elif self.mode == 'Normal': self.iLastRating = res
        else: self.eLastRating = res
        lst.clear()

    @staticmethod
    def calculateRating(self, resultsArr, lastResult):
        """This calculates the rating"""

        quantity = len(resultsArr)
        totalWins = resultsArr.count("'1',") + resultsArr.count("'1'") + resultsArr.count('1')
        if lastResult == 0.0:
            if quantity != 0: calcResult = (totalWins * 100) / quantity
            else: calcResult = 0
        else:
            if quantity != 0: calcResult = (lastResult+((totalWins * 100) / quantity))/2
            else: calcResult = lastResult
        return round(calcResult, 2)

    def saveGameField(self):
        """This saves the game field arrays (binary data)"""

        if not isGameOver:
            global field, buttons
            openedCells = []

            for buttonRow in buttons:
                for b in buttonRow:
                    if b['state'] == 'disabled':
                        if b['text'] == "⚑": openedCells.append(2)
                        elif b['text'] == "?": openedCells.append(3)
                        else: openedCells.append(0)
                    else:
                        if b['text'] == " ": openedCells.append(1)

            with open((saveDir + self.playerName + "_cells.bin"), "w+b") as cellSheet:
                binCells = bytearray(openedCells)
                cellSheet.write(binCells)

            with open((saveDir + self.playerName + "_game.bin"), "w+b") as binaryField:
                for cellRow in field:
                    binField = bytearray(cellRow)
                    binaryField.write(binField)

    def loadGameField(self):
        """This restores data from game arrays we saved"""

        if os.path.exists(saveDir + self.playerName + "_game.bin"):
            global field, buttons
            response = tkinter.messagebox.askyesno("Load game",
                                                   message='You have an unfinished game. \n'
                                                           'Load it?')
            if response:
                intCellsRow = []
                Cells = []

                with open((saveDir + self.playerName + "_cells.bin"), "r+b") as cellSheet:
                    cells = cellSheet.readlines()
                    for row in cells:
                        for c in row: Cells.append(int(c))

                if len(Cells) == 81: cellColumns = 9
                elif len(Cells) == 256: cellColumns = 16
                else: cellColumns = 30

                if cellColumns == 9: setSize(9, 9, 10)
                elif cellColumns == 16: setSize(16, 16, 40)
                else: setSize(16, 30, 99)

                openedCells = [Cells[i:i + cellColumns] for i in range(0, len(Cells), cellColumns)]

                if os.path.exists(saveDir + self.playerName + "_game.bin"):
                    with open((saveDir + self.playerName + "_game.bin"), "r+b") as binaryField:
                        binData = binaryField.readlines()
                        for cellRow in binData:
                            for c in cellRow:
                                intCellsRow.append(int(c))
                intCells = [intCellsRow[i:i + columns] for i in range(0, len(intCellsRow), columns)]

                field = intCells

                for n, row in enumerate(openedCells):
                    for nn, c in enumerate(row):
                        if c == 1:
                            buttons[n][nn]['state'] = 'normal'
                            buttons[n][nn]['relief'] = 'raised'
                        elif c == 2:
                            buttons[n][nn]["text"] = "⚑"
                            buttons[n][nn]["state"] = "disabled"
                        elif c == 3:
                            buttons[n][nn]["text"] = "?"
                            buttons[n][nn]["state"] = "disabled"
                        else:
                            Cell.clickOn(Cell, n, nn)

class Cell:
    firstClickHappened = False

    def clickOn(self, x, y):
        """This is for left click events"""

        global field, buttons, colors, isGameOver, rows, columns
        if not self.firstClickHappened:
            if field[x][y] == 9:
                field[x][y] = 0
                valueGeneration(x, y, sub)

                xx = random.randint(0, rows - 1)
                yy = random.randint(0, columns - 1)
                if buttons[xx][yy]['state'] != 'disabled':
                    field[xx][yy] = 9
                    valueGeneration(xx, yy, add)
                else:
                    xx = random.randint(0, rows - 1)
                    yy = random.randint(0, columns - 1)
                    valueGeneration(x, y, sub)
                    valueGeneration(xx, yy, add)
            self.firstClickHappened = True

        if isGameOver: return
        buttons[x][y]["text"] = str(field[x][y])

        if field[x][y] == 9:
            buttons[x][y]["text"] = "✱"
            buttons[x][y].config(bg='red', disabledforeground='red')
            isGameOver = True
            Player.frown(Player)
            File.saveResults(File, False)
            os.remove(saveDir + File.playerName + "_game.bin")
            os.remove(saveDir + File.playerName + "_cells.bin")

            for _x in range(0, rows):
                for _y in range(columns):
                    if field[_x][_y] == 9:
                        buttons[_x][_y]["text"] = "✱"
                        buttons[_x][_y]["fg"] = colors[10]
        else:
            buttons[x][y].config(disabledforeground=colors[field[x][y]])
        if field[x][y] == 0:
            buttons[x][y]["text"] = " "
            self.autoClickOn(self, x, y)
        buttons[x][y]['state'] = 'disabled'
        buttons[x][y].config(bg=colors[0])
        buttons[x][y].config(relief=tkinter.GROOVE)
        File.saveGameField(File)
        checkWin()

    def autoClickOn(self, x, y):
        global field, buttons, colors, rows, columns

        if field[x][y] != 9:

            if buttons[x][y]["state"] == "disabled":
                return
            if field[x][y] != 0:
                buttons[x][y]["text"] = str(field[x][y])
            else:
                buttons[x][y]["text"] = " "
            buttons[x][y].config(disabledforeground=colors[field[x][y]])
            buttons[x][y].config(relief=tkinter.GROOVE)
            buttons[x][y]['state'] = 'disabled'
            buttons[x][y].config(bg=colors[0])
            if field[x][y] == 0:
                if x != 0 and y != 0:
                    self.autoClickOn(self, x - 1, y - 1)
                if x != 0:
                    self.autoClickOn(self, x - 1, y)
                if x != 0 and y != columns - 1:
                    self.autoClickOn(self, x - 1, y + 1)
                if y != 0:
                    self.autoClickOn(self, x, y - 1)
                if y != columns - 1:
                    self.autoClickOn(self, x, y + 1)
                if x != rows - 1 and y != 0:
                    self.autoClickOn(self, x + 1, y - 1)
                if x != rows - 1:
                    self.autoClickOn(self, x + 1, y)
                if x != rows - 1 and y != columns - 1:
                    self.autoClickOn(self, x + 1, y + 1)

    def onRightClick(self, x, y):
        global buttons
        if isGameOver: return
        if buttons[x][y]["relief"] != tkinter.GROOVE:
            if buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
                buttons[x][y]["text"] = "⚑"
                buttons[x][y].config(disabledforeground=colors[11])
                buttons[x][y]["state"] = "disabled"
                File.saveGameField(File)

            elif buttons[x][y]["text"] == "⚑":
                buttons[x][y]["text"] = "?"
                buttons[x][y].config(disabledforeground=colors[11])
                File.saveGameField(File)

            else:
                buttons[x][y]["text"] = " "
                buttons[x][y]["state"] = "normal"
                buttons[x][y].config(disabledforeground=colors[field[x][y]])
                File.saveGameField(File)

class Player:
    faces = ["🙂", "😟", "😄"]
    p = tkinter.Button(root, text=faces[0], font=('Helvetica', '30'), command=restartGame)

    def __init__(self, f=faces, p=p):
        self.f = f

    def frown(self):
        self.p.config(text=self.faces[1])
        pass

    def smile(self):
        self.p.config(text=self.faces[2])
        pass


File.playerAuth(File)
Player.p.grid(row=0, column=0, columnspan=columns, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
createMenu()
prepareWindow()
prepareGame()
root.mainloop()
