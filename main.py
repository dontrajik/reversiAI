import re
from random import choice, shuffle

class Board:
    def __init__(self):
        self.width, self.height = 8, 8

        self.black, self.white = 2,2

        self.board = [[" "]*self.height for row in range(self.width)]

        self.board[3][3] = self.board[4][4] = "-"
        self.board[3][4] = self.board[4][3] = "+"

        self.onTurn = True #true if White (+), false if Black (-)
        self.validMoves = []

        self.moves = []

    def __repr__(self) -> str:
        ret = "──┬───┬───┬───┬───┬───┬───┬───┬───\n"
        self.validMoves = []
        for row in range(self.height - 1,-1,-1):
            ret += str(row)
            for col in range(self.width):
                ret  += " │ " + str(self.board[col][row])
            ret += "\n──┼───┼───┼───┼───┼───┼───┼───┼───\n"
        ret += "  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 \n"
        return ret
    
    def endTurn(self) -> None:
        self.onTurn = not self.onTurn
        
    def on_board(self, move:tuple) -> bool:
        col, row = move
        return (row >= 0) and (row < self.height) and (col >= 0) and (col < self.width)
    
    def scan(self, position) -> list:
        validDirections = []
        if(self.onTurn):
            player = "+"
            opponent = "-"
        else:
            player = "-"
            opponent = "+"

        directons = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for direction in  directons:
            dc, dr = direction
            c, r = position
            
            vals = ""
            while 0 <= r < self.height and 0 <= c < self.width:
                vals +=  str(self.board[c][r])
                r += dr
                c += dc
            if(re.search("^\s{1}"+"\{}+\{}".format(opponent, player),vals) != None):
                validDirections.append(direction)
        return validDirections

    def isValidMove(self, move : tuple) -> bool:
        if(not(self.on_board(move))):
            return False
        c, r = move
        if(self.board[c][r] != " "):
            return False
        
        if(len(self.scan(move)) == 0):
            return False
        return True
    
    def makeMove(self, move : list) -> int:
        move = [int(i) for i in move]
        if(self.onTurn):
            opponent = "-"
        else:
            opponent = "+"
        col, row = move
        if self.on_board(move) and self.isValidMove(move):
            validDirections = self.scan(move)
            for direction in validDirections:
                self.board[col][row] = "-" if self.onTurn else "+"
                dc, dr = direction
                c, r = move
                while 0 <= r < self.height and 0 <= c < self.width and self.board[c][r] == opponent:
                    self.board[c][r] = "+" if self.onTurn else "-"
                    r += dr
                    c += dc
            self.endTurn()
            self.moves.append(move)
        else:
            print("Invalid Move!")
        
        self.updateScore()

    def unmakeMove(self) -> None:
        self.board = [[" "]*self.height for row in range(self.width)]

        self.board[3][3] = self.board[4][4] = "-"
        self.board[3][4] = self.board[4][3] = "+"

        self.onTurn = True
        
        moves = self.moves[:-1]
        self.moves = []

        for move in moves:
            self.makeMove(move)
        self.updateScore()

    def updateScore(self):
        self.black = self.white = 0
        for row in self.board:
            for cell in row:
                if cell == "+":
                    self.white += 1
                elif cell == "-":
                    self.black += 1
        return self.white - self.black

    def checkWin(self) -> str:
        self.updateScore()
        if self.black + self.white == 64:
            if self.white > self.black or self.black == 0:
                return "White Wins! {} : {}".format(self.white, self.black)
            elif self.black > self.white or self.white == 0:
                return "Black Wins! {} : {}".format(self.black, self.white)
            else:
                return "Tie!"
        else:
            if(len(self.getValidMoves()) == 0):
                self.endTurn()
            return "Game on"
        
    def getValidMoves(self) -> list:
        self.validMoves = []
        for col in range(self.width):
            for row in range(self.height):
                if(self.isValidMove((col,row))):
                    self.validMoves.append((col, row))
        return self.validMoves
       
class AlphaBeta:
  def __init__(self, depth = 8):
    self.game = Board()
    self.depth = depth

  # returns a move based on an alpha-beta search
  def act(self):
    move = self.search()
    return move

  # update the internal board state for the class
  def feed(self, move):
    self.game.makeMove(move)

  # the root node of an alpha-beta search
  def search(self):
    print("AlphaBeta searching")
    moves = self.game.getValidMoves()

    # a list to store the values associated with each move
    scores = []      
    alpha = -10
    for move in moves:
      print(move, end="\r")
      res = self.game.makeMove(move)
      # if the move wins the game, play it immediately
      if res:                     
        self.game.unmakeMove()
        return move
      val = -self.alpha_beta(-10, -alpha, self.depth - 1)
      self.game.unmakeMove()
      scores.append((val, move))

    # the algorithm randomises between moves that have the same value 
    shuffle(scores)
    scores.sort(key = lambda x: -x[0])
    print("\nAlphaBeta score: " + str(scores[0][0]))
    return scores[0][1]

 

  def alpha_beta(self, alpha, beta, depth):
    if depth == 0: return 0 
    moves = self.game.getValidMoves()
    for move in moves:
      self.game.makeMove(move)

      res = not(self.game.checkWin() == "Game on")

      if res:
        self.game.unmakeMove()
        return 1 + 0.01 * depth
      
      val = -self.alpha_beta(-beta, -alpha, depth - 1)
      self.game.unmakeMove()
    
      # check for alpha node
      if val >= alpha:
        alpha = val

      # check for beta cut
      if val >= beta:
        return val
    return self.game.updateScore() 

board = Board()
print(board)

player1 = AlphaBeta(depth = 2)

while(board.checkWin() == "Game on"):
    print(board)
    print("Current score:", board.white, ":", board.black)
    print("Valid moves: ", board.getValidMoves())
    bestmove = player1.act()
    print(bestmove)
    
    board.makeMove(bestmove)
    player1.feed(bestmove)

    end = board.checkWin()
    if(end != "Game on"):
        break
    print(board)
    print("Current score:", board.white, ":", board.black)
    print("Valid moves: ", board.getValidMoves())
    move = input("Move ({}): ".format("+" if board.onTurn else "-"))
    move = move.strip().split(" ")
    board.makeMove(move) 
    player1.feed(move)
print(board.white, ":", board.black)