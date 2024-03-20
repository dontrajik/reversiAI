from PIL import Image

class Board:
    def __init__(self):
        self.width, self.height = 8, 8

        self.board = [ [0]*self.width for i in range(self.height)]

        self.board[3][3] = self.board[4][4] = "-"
        self.board[3][4] = self.board[4][3] = "+"

        self.onTurn = True #true if White (-)
    
    def export(self):
            file = open(".\\output.ppm", "w")
            file.writelines(("P6\n", "8 8\n", "255\n"))
            for row in range(self.height):
                for col in range(self.width):
                    if(self.board[col][row] == 0):
                        file.writelines(("0 255 0\n"))
                    elif(self.board[col][row] == "+"):
                        file.writelines(("255 255 255\n"))
                    else:
                        file.writelines(("0 0 0\n"))
            file.close()
    
    def __repr__(self) -> str:
        ret = ""
        for i in range(self.width):
            for j in range(self.height):
                ret  += str(self.board[i][j])+"  "
            ret += "\n"
        return ret

    def makeMove(self, move : tuple):
        row, col = move
        if row < 0 or row >= self.width or col < 0 or  col >= self.height:
            raise IndexError("Invalid Move!")
        if self.board[col][row] != 0:
            raise ValueError("There is already a piece here.")

board = Board()
board.export()
row, col = input("MOVE: ").strip().split(" ")
while(row != "q"):
    board.makeMove((int(row), int(col)))
    print(board)
    row, col = input("MOVE: ").strip().split(" ")