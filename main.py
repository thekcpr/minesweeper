import tkinter as tk
import random
from typing import Protocol


class OptionState: pass

class Minesweeper: #  Play State
    def __init__(self, rows: int, columns: int, num_bombs: int, root: tk.Tk):
        self.rows = rows
        self.columns = columns
        self.num_bombs = num_bombs
        self.board: list[list[str]] | list = []
        self.buttons = []

        self.root = root
        self.root.geometry(f"{58*self.columns}x{48*self.rows}")

        for i in range(rows):
            btn_row = []

            for j in range(columns):
                btn = tk.Button(root, text=" ", height=2, width=2, relief='sunken', borderwidth=4, command=lambda choice=[i, j]: self.player_choice(choice))
                btn.grid(row = i, column = j)
                btn_row.append(btn)
            self.buttons.append(btn_row)


    def player_choice(self, choice: list[int, int]) -> None:
        if self.board == []:
            self.generate_board(choice)
            self.update_board()
        else:
            pass


    def update_board(self) -> None:
        for i in range(self.rows):
            for j in range(self.columns):
                self.buttons[i][j].config(text=f"{self.board[i][j]}")


    def get_surrounding_cells(self, cell: list[int, int]) -> list[list[int, int, str]]:
        surrounding_cells = []

        if cell[0]-1 in range(self.rows) and cell[1]-1 in range(self.columns):
            surrounding_cells.append([cell[0]-1, cell[1]-1, self.board[cell[0]-1][cell[1]-1]])
        if cell[0]-1 in range(self.rows) and cell[1] in range(self.columns):
            surrounding_cells.append([cell[0]-1, cell[1], self.board[cell[0]-1][cell[1]]])
        if cell[0]-1 in range(self.rows) and cell[1]+1 in range(self.columns):
            surrounding_cells.append([cell[0]-1, cell[1]+1, self.board[cell[0]-1][cell[1]+1]])

        if cell[0] in range(self.rows) and cell[1]-1 in range(self.columns):
            surrounding_cells.append([cell[0], cell[1]-1, self.board[cell[0]][cell[1]-1]])
        if cell[0] in range(self.rows) and cell[1]+1 in range(self.columns):
            surrounding_cells.append([cell[0], cell[1]+1, self.board[cell[0]][cell[1]+1]])

        if cell[0]+1 in range(self.rows) and cell[1]-1 in range(self.columns):
            surrounding_cells.append([cell[0]+1, cell[1]-1, self.board[cell[0]+1][cell[1]-1]])
        if cell[0]+1 in range(self.rows) and cell[1] in range(self.columns):
            surrounding_cells.append([cell[0]+1, cell[1], self.board[cell[0]+1][cell[1]]])
        if cell[0]+1 in range(self.rows) and cell[1]+1 in range(self.columns):
            surrounding_cells.append([cell[0]+1, cell[1]+1, self.board[cell[0]+1][cell[1]+1]])
        
        return surrounding_cells


    def generate_board(self, first_choice: list[int, int]) -> None:

        # Generates empty board
        for i in range(self.rows):
            board_row = []
            for j in range(self.columns):
                board_row.append(" ")
            self.board.append(board_row)

        # Genrates list of unique bomb coordinates that are at least 1 cell away player's first click
        bomb_cells = []
        safe_cells = []
        k = 0

        for cell in self.get_surrounding_cells(first_choice):
            cell.pop(2)
            safe_cells.append(cell)
        safe_cells.append(first_choice)

        while k < self.num_bombs:
            bomb_y = random.randint(0, self.rows-1)
            bomb_x = random.randint(0, self.columns-1)
            single_bomb = [bomb_y, bomb_x]

            if single_bomb not in bomb_cells and single_bomb not in safe_cells:
                k += 1
                bomb_cells.append(single_bomb)

        # Generates board filled with bombs
        for i in range(self.rows):

            for j in range(self.columns):
                board_cell = [i, j]

                if board_cell in bomb_cells:
                    self.board[i][j] = "X"

        #Calculates number of bombs around each cell and injects it into the board
        for i in range(self.rows):

            for j in range(self.columns):
                bomb_count = 0
                surronding_cells = self.get_surrounding_cells([i, j])

                for cell in surronding_cells:
                    if self.board[cell[0]][cell[1]] == "X":
                        bomb_count += 1

                if self.board[i][j] != "X":
                    if bomb_count == 0:
                        self.board[i][j] = ""
                    else:
                        self.board[i][j] = f"{bomb_count}"

class SolvedState: pass

class FailedState: pass


def main():
    root = tk.Tk()

    root.title("Minesweeper")

    Minesweeper(16, 16, 40, root)

    root.mainloop()


if __name__ == "__main__":
    main()
