import tkinter as tk
import tkmacosx as ttk
import random
from typing import Protocol

# TODO:
# - playing conditions from Minesweeper.update_board() should be in Minesweeper.reveal() to better handle all player choices
# - Merge Minesweeper.reveal_cell() with Minesweeper.reveal()
# - Implement flagging
# - Add images to buttons. Use tk.Frame, or tk.Label instead of ttk.Button?
# - Get rid of tkmacosx
# - Add options menu
# - Add pop up window to Fialed and Solved State
# - Add top section with timer, an remaining bomb counter
# - Add scoreboard?
# - Add docstrings to all functions
# - Fix error: after clicking on reveald cell Minesweeper.reveal_cell() wants to remve cell from unrevealed_cells list. ValueError: list.remove(x): x not in list


class OptionState: pass

class Minesweeper:  # Play State
    def __init__(self, rows: int, columns: int, num_bombs: int, root: tk.Tk):
        self.rows = rows
        self.columns = columns
        self.num_bombs = num_bombs
        self.board: list[list[dict[str, str | bool]]] = []  # list of dicts lists {"is_revealed": bool, "content": str, "flagged": bool} or empty list
        self.buttons = []
        self.bomb_list = []
        self.unrevealed_cells = []

        self.cell_content = {"bomb": "X",
                             "fail": "*",
                             "0": "",
                             "1": "1",
                             "2": "2",
                             "3": "3",
                             "4": "4",
                             "5": "5",
                             "6": "6",
                             "7": "7",
                             "8": "8"}

        self.root = root
        self.root.geometry(f"{38*self.columns}x{38*self.rows}")

        for i in range(rows):
            btn_row = []

            for j in range(columns):
                btn = ttk.Button(root, text=" ", height=30, width=30, relief='raised', borderwidth=4, command=lambda choice=[i, j]: self.update_board(choice))
                btn.grid(row = i, column = j)
                btn_row.append(btn)
            self.buttons.append(btn_row)


    def update_board(self, choice: list[int, int]) -> None:
        if self.board == []:
            self.generate_board(choice)

        # Failed Condition
        if choice in self.bomb_list:
            self.board[choice[0]][choice[1]]["content"] = self.cell_content["fail"]
            for i, j in self.bomb_list:
                self.reveal_cell([i, j])

        # Playing Condition
        else:
            # Click on empty cell
            if self.board[choice[0]][choice[1]]["content"] == self.cell_content["0"]:
                self.reveal(choice)

            # Click on number cell
            else:
                self.reveal_cell(choice)

        # Solved Condition
        if len(self.unrevealed_cells) == self.num_bombs:
            exit()

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j]["is_revealed"] == True:
                    self.buttons[i][j].config(text=f"{self.board[i][j]["content"]}", height=30, width=30, relief="groove")


    def get_surrounding_cells(self, cell: list[int, int]) -> list[list[int, int]]:
        surrounding_cells = []
        neighbors = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, +1),
                     (1, -1), (1, 0), (1, 1)]

        for b, a in neighbors:
            y = cell[0]+b
            x = cell[1]+a
            if 0 <= y < self.rows and 0 <= x < self.columns:
                surrounding_cells.append([y, x])
        
        return surrounding_cells


    def reveal(self, cell) -> None:
        self.reveal_cell([cell[0], cell[1]])
        cluster_cells = self.get_surrounding_cells(cell)
        for cell_info in cluster_cells:
            y = cell_info[0]
            x = cell_info[1]
            if self.board[y][x]["content"] == self.cell_content["0"] and self.board[y][x]["is_revealed"] == False:
                self.reveal(cell_info)
            elif self.board[y][x]["content"] != self.cell_content["0"] and self.board[y][x]["is_revealed"] == False:
                self.reveal_cell([y, x])


    def reveal_cell(self, cell) -> None:
        self.board[cell[0]][cell[1]]["is_revealed"] = True
        self.unrevealed_cells.remove(cell)


    def generate_board(self, first_choice: list[int, int]) -> None:

        # Generates empty board
        for i in range(self.rows):
            board_row = []
            for j in range(self.columns):
                board_row.append({"is_revealed": False, "content": "", "flagged": False})
                self.unrevealed_cells.append([i, j])
            self.board.append(board_row)

        # Fills board with bombs of random and unique coordinates, that are at least 1 cell away of player's first click
        safe_cells = self.get_surrounding_cells(first_choice)
        safe_cells.append(first_choice)

        while len(self.bomb_list) < self.num_bombs:
            bomb_y = random.randint(0, self.rows-1)
            bomb_x = random.randint(0, self.columns-1)
            single_bomb = [bomb_y, bomb_x]

            if single_bomb not in self.bomb_list and single_bomb not in safe_cells:
                self.bomb_list.append(single_bomb)
                self.board[bomb_y][bomb_x]["content"] = self.cell_content["bomb"]

        # Calculates number of bombs around each cell and injects it into the board
        for i in range(self.rows):
            for j in range(self.columns):
                bomb_count = 0

                for cell in self.get_surrounding_cells([i, j]):
                    y = cell[0]
                    x = cell[1]
                    if self.board[y][x]["content"] == self.cell_content["bomb"]:
                        bomb_count += 1

                if self.board[i][j]["content"] != self.cell_content["bomb"]:
                    self.board[i][j]["content"] = self.cell_content[f"{bomb_count}"]

class SolvedState: pass

class FailedState: pass


def main():
    root = tk.Tk()

    root.title("Minesweeper")

    Minesweeper(16, 16, 40, root)

    root.mainloop()


if __name__ == "__main__":
    main()
