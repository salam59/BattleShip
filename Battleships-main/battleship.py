"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test
import random

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["board_size"] = 500
    data["cell_size"] = data["board_size"]/(data["rows"]*data["cols"])
    data["number_of_ships"] = 5
    data["user_board"] = emptyGrid(data['rows'],data['cols'])
    data["computer_board"] = emptyGrid(data['rows'],data['cols'])
    data['computer_board'] = addShips(data['computer_board'],data['number_of_ships'])
    data['temporary_ship'] = [] #empty ship
    data['no_of_user_ships'] = 0
    data['winner'] = None
    data['max_no_of_turns'] = 50
    data['no_of_turns'] = 0

'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data['user_board'],showShips=True)
    drawGrid(data,compCanvas,data['computer_board'],showShips=False)
    drawShip(data,userCanvas,data['temporary_ship'])
    if data['winner'] != None:
        drawGameOver(data,userCanvas)

'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return":
        makeModel(data)


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data['winner'] != None:  return
    value = getClickedCell(data,event)
    print(value)
    if value!=None:
        row,col = tuple(value)
        if board == "user":
            clickUserBoard(data,row,col)
            # runGameTurn(data,row,col)
        else:
            if data["no_of_user_ships"] == 5:
                runGameTurn(data,row,col)
        


#### STAGE 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    l = []
    for i in range(rows):
        l.append([EMPTY_UNCLICKED]*cols)
    return l
'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row = random.randint(1,8)
    col = random.randint(1,8)
    orientation = random.randint(0,1)
    ship = None
    if orientation == 0: # vertical
        ship = [[row-1,col],[row,col],[row+1,col]]
    else: # horizontal
        ship = [[row,col-1],[row,col],[row,col+1]]
    return ship

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for cell in ship:
        if grid[cell[0]][cell[1]] != EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    
    while numShips != 0:
        ship = createShip()
        if checkShip(grid,ship):
            numShips = numShips - 1
            for cell in ship:
                grid[cell[0]][cell[1]] = SHIP_UNCLICKED
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    # grid = test.testGrid()
    
    for row in range(data['rows']):
        topSq = row * 50
        bottomSq = topSq + 50
        for col in range(data['cols']):
            left_col = col * 50
            right_col = left_col + 50
            if grid[row][col] == SHIP_UNCLICKED:
                '''Battleship is too easy if you can
                    see your opponent's ships, so if showShips is False, draw SHIP_UNCLICKED cells as blue (to
                    hide them'''
                if showShips == True:
                    canvas.create_rectangle(left_col,topSq,right_col,bottomSq,fill="yellow", outline = 'blue')
                else:
                    canvas.create_rectangle(left_col,topSq,right_col,bottomSq,fill="blue", outline = 'blue')
            if grid[row][col] == EMPTY_UNCLICKED:
                canvas.create_rectangle(left_col,topSq,right_col,bottomSq,fill="blue", outline = 'blue')
            if grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(left_col,topSq,right_col,bottomSq,fill="red", outline = 'blue')
            if grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(left_col,topSq,right_col,bottomSq,fill="white", outline = 'blue')
            
    canvas.pack()
    return


### STAGE 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    center = ship[1]
    row_before = ship[0][0]
    row_after = ship[2][0]
    if (row_before != center[0] - 1) or (row_after != center[0] + 1):
        return False
    if center[1] != ship[0][1] or center[1] != ship[2][1]:
        return False
    return True


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    center = ship[1]
    if ship[0][0] != center[0] or ship[2][0] != center[0]: #checking if rows are same
        return False
    if ship[0][1] != center[1]-1 or ship[2][1] != center[1]+1: # checking validilty of columns
        return False
    return True


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    rows = data['rows']
    cols = data['cols']
    for row in range(rows):
        top = row * 50
        bottom = top + 50
        for col in range(cols):
            left = col * 50
            right = left + 50
            # print(left,right)
            # print(top,bottom)
            if (left<event.x and right>event.x): #row check
                if (top<event.y and bottom>event.y): #col check
                    return [row,col]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    #ship will be drawn only after checking if we can accommodate the ship

# similar logic to your code for drawGrid(), except
# that you'll only draw cells that exist in the ship value.
#in case of drawgrid we draw for every cell
    user_board = data['user_board']
    for cell in ship:
        col = cell[1]
        row = cell[0]
        left = col * 50
        right = left + 50
        top = row * 50
        bottom = top + 50
        # if user_board[row][col] == SHIP_UNCLICKED:
        canvas.create_rectangle(left,top,right,bottom,fill="white",outline='blue')

    canvas.pack()
    


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) == 3 and checkShip(grid,ship) and (isVertical(ship) or isHorizontal(ship)): 
        return True
    return False

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    ship = data['temporary_ship']
    if shipIsValid(data['user_board'],ship):
        user_board = data['user_board']
        for cell in ship:
            user_board[cell[0]][cell[1]] = SHIP_UNCLICKED
        data['no_of_user_ships'] += 1
        print(data['no_of_user_ships'])
    else:
        print("Invalid Ship!!!")
        data['temporary_ship'] = []


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data['no_of_user_ships'] == 5:
        return
    ship = data['temporary_ship']
    if [row,col] in ship:
        return
    ship.append([row,col])
    if len(ship) == 3:
        placeShip(data)
        print(ship)
        ship.clear()
    if data['no_of_user_ships'] == 5:
        print("Start Playing the Game!!!")


### STAGE 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    if board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
    if isGameOver(board):
        data['winner'] = player



'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None

check whether (row, col) has already been clicked on the
computer's board (ie, if it is SHIP_CLICKED or EMPTY_CLICKED); if it has, return early so that
the user can click again.
'''
def runGameTurn(data, row, col):
    computer_board = data['computer_board']
    value = computer_board[row][col]
    if value == SHIP_CLICKED or value == EMPTY_CLICKED:
        return
    updateBoard(data,computer_board,row,col,'user')
    row,col = getComputerGuess(data['user_board'])
    value = data['user_board'][row][col]
    if value == SHIP_CLICKED or value == EMPTY_CLICKED:
        return
    updateBoard(data,data['user_board'],row,col,'comp')
    data['no_of_turns'] += 1
    if data["no_of_turns"] == data["max_no_of_turns"]:
        data['winner'] = 'draw'

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    guess = None
    while True:
        row = random.randint(0,9)
        col = random.randint(0,9)
        guess = [row,col]
        if board[row][col] != SHIP_CLICKED and board[row][col]!=EMPTY_CLICKED:
            break
    # print(guess)
    return guess


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    print(board)
    for row in board:
        if SHIP_UNCLICKED in row:
            return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    winner = data['winner']
    if winner == 'user':
        canvas.create_text(300, 100, text="Congratulations!!!", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 150, text="Press ENTER to Play again!!", fill="black", font=('Helvetica 15 bold'))
    elif winner == 'comp':
        canvas.create_text(300, 100, text="You Lose!!!", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 150, text="Press ENTER to Play again!!", fill="black", font=('Helvetica 15 bold'))
    elif winner == 'draw':
        canvas.create_text(200, 100, text="You are out of moves!!! Draw...", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 150, text="Press ENTER to Play again!!", fill="black", font=('Helvetica 15 bold'))
### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    test.stage1Tests()

    ## Uncomment these for STAGE 2 ##
    print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    test.stage2Tests()


    ## Uncomment these for STAGE 3 ##

    print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    test.stage3Tests()


    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
