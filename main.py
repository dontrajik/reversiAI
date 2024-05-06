import re
import random

class Board:
    def __init__(self):
        self.width, self.height = 8, 8

        self.black, self.white = 0,0

        self.board = [ [0]*self.width for i in range(self.height)]

        self.board[3][3] = self.board[4][4] = "+"
        self.board[3][4] = self.board[4][3] = "-"

        self.onTurn = True #true if White (+), false if Black (-)
        self.validDirections = []

    def __repr__(self) -> str:
        ret = ""
        for i in range(self.width):
            for j in range(self.height):
                ret  += str(self.board[i][j])+"  "
            ret += "\n"
        return ret
    
    def on_board(self, move:tuple):
        row, col = move
        return row >= 0 or row < self.width or col >= 0 or  col < self.height
    
    def isValidMove(self, move : tuple) -> bool:
        self.validDirections = []
        if(self.onTurn):
            player = "+"
            opponent = "-"
        else:
            player = "-"
            opponent = "+"
        
        valid = True
        directons = [(0,-1),(1,-1),(0,1),(1,1),(1,0),(-1,1),(-1,0),(-1,-1)]
        for direction in  directons:
            dr, dc = direction
            r, c = move
            if(r < 0):
                valid = False
            elif(r >= self.height):
                valid = False
            elif(c < 0):
                valid = False
            elif(c >= self.width):
                valid = False
            elif (self.board[c][r] != 0):
                valid = False
            
            vals = ""
            while valid and 0 <= r < self.height and 0 <= c < self.width:
                vals +=  str(self.board[c][r])
                r += dr
                c += dc
            if(re.search("^0{1}"+"\{}+\{}".format(opponent, player),vals) != None):
                self.validDirections.append(direction)
                valid = True
        if(len(self.validDirections) == 0):
            valid = False
        return valid
    
    def makeMove(self, move : tuple):
        if(self.onTurn):
            opponent = "-"
        else:
            opponent = "+"
        row, col = move
        if self.on_board(move) and self.isValidMove(move):
            for direction in self.validDirections:
                self.board[col][row] = "-" if self.onTurn else "+"
                dr, dc = direction
                r, c = move
                while 0 <= r < self.height and 0 <= c < self.width and self.board[c][r] == opponent:
                    self.board[c][r] = "+" if self.onTurn else "-"
                    r += dr
                    c += dc
            self.onTurn = not self.onTurn
        else:
            print("Invalid Move!")

    def unmakeMove(self, move : tuple):
        row, col = move
        dirs = ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1))
        for direction in dirs:
            dy, dx = direction

    def checkWin(self):
        self.black = self.white = 0
        for row in self.board:
            for cell in row:
                if cell == "+":
                    self.white += 1
                elif cell == "-":
                    self.black += 1
        if self.black + self.white == 64:
            if self.white > self.black:
                return "White Wins!"
            elif self.black > self.white:
                return "Black Wins!"
            else:
                return "Tie!"
        else:
            if(len(self.moves()) == 0):
                self.onTurn = not self.onTurn
            return "Game on"
        
    def moves(self):
        validMoves = []
        for row in range(8):
            for col in range(8):
                if(self.isValidMove((row,col))):
                    validMoves.append((row, col))
        print(validMoves)
        return validMoves

board = Board()
moves = []

print(board)
row, col = input("{} MOVE: ".format("+" if board.onTurn else "-")).strip().split(" ")
while(row != "q"):
    moves.append((int(row), int(col)))
    if board.checkWin() != "Game on":
        print(board.checkWin())
        break
    board.makeMove(random.choice(board.moves()))
    print(board)
    # row, col = input("{} MOVE: ".format("+" if board.onTurn else "-")).strip().split(" ")
