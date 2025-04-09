from random import randint


class BoardModel:
    def __init__(self, rows: int, cols: int, num_bombs: int):
        self.rows = rows
        self.cols = cols
        self.num_bombs = num_bombs

        self.game_failed = False
        self.bomb_list = []
        self.all_tiles = []
        self.closed_tiles = []
        self.tiles_to_update = []
        self.num_flags = 0

        self.CLOSED = 'closed'
        self.FLAGGED = 'flagged'
        self.MISSFLAGGED = 'missflagged'
        self.QUESTION = 'question'
        self.OPEN = 'open'

        self.tile_content = {'bomb': 'open_bomb',
                             'fail': 'open_bomb_red',
                             '0': 'open_0',
                             '1': 'open_1',
                             '2': 'open_2',
                             '3': 'open_3',
                             '4': 'open_4',
                             '5': 'open_5',
                             '6': 'open_6',
                             '7': 'open_7',
                             '8': 'open_8'}


        self.board: dict[tuple[int, int]: dict[str: str, str: str]] = {}  # dict of tile dicts
        self.empty_tile = {'state': self.CLOSED, 'content': ''}  # states: closed / open / flagged / question. content: bomb, 0, 1, 2, 3, 4, 5, 6, 7, 8

        # Generates dict of board without content
        for x in range(self.cols):
            for y in range(self.rows):
                self.board[(x, y)] = self.empty_tile.copy()
                self.all_tiles.append((x, y))
                self.closed_tiles.append((x, y))
                self.tiles_to_update.append((x, y))

    def get_cols(self) -> int:
        return self.cols
    

    def get_rows(self) -> int:
        return self.rows


    def get_board(self) -> dict[tuple[int, int]: dict[str: str, str: str]]:
        return self.board


    def get_unflagged_bombs_num(self) -> int:
        return self.num_bombs - self.num_flags


    def get_all_tiles(self) -> list[tuple[int, int]]:
        return self.all_tiles


    def get_tiles_to_update(self) -> list[tuple[int, int]]:
        return self.tiles_to_update


    def get_unrevealed_tiles(self) -> list[tuple[int, int]]:
        return self.closed_tiles
    

    def is_solved(self) -> bool:
        if len(self.closed_tiles) == self.num_bombs:
            return True
        else: return False


    def is_failed(self) -> bool:
        return self.game_failed


    def generate_board(self, first_tile: tuple[int, int]) -> None:

        # Fills board with bombs of random and unique coordinates, that are at least 1 cell away of player's first click
        safe_tiles = self.get_surrounding_tiles(first_tile)
        safe_tiles.append(first_tile)

        while len(self.bomb_list) < self.num_bombs:
            bomb_x = randint(0, self.cols-1)
            bomb_y = randint(0, self.rows-1)
            bomb_tile = (bomb_x, bomb_y)

            if bomb_tile not in self.bomb_list and bomb_tile not in safe_tiles:
                self.bomb_list.append(bomb_tile)
                self.board[bomb_tile]['content'] = self.tile_content['bomb']

        # Calculates number of bombs around each cell and injects it into the board
        for x in range(self.cols):
            for y in range(self.rows):

                if self.board[(x, y)]["content"] != self.tile_content["bomb"]:
                    bomb_count = 0

                    # TODO: Learn about generator expressions to reduce nesting
                    for tile in self.get_surrounding_tiles((x, y)):
                        if self.board[tile]["content"] == self.tile_content["bomb"]:
                            bomb_count += 1
                    self.board[(x, y)]["content"] = self.tile_content[f"{bomb_count}"]


    def reveal(self, tile: tuple[int, int]) -> None:
        self.tiles_to_update = []

        if self.board[tile]['state'] != self.FLAGGED:
            self.hendle_chord(tile)
            self.reveal_tile(tile)


    def handle_right_click(self, tile: tuple[int, int]) -> None:
        if self.board[tile]['state'] == self.CLOSED:
            self.board[tile]['state'] = self.FLAGGED
            self.num_flags += 1

        elif self.board[tile]['state'] == self.FLAGGED:
            self.board[tile]['state'] = self.QUESTION
            self.num_flags -= 1

        elif self.board[tile]['state'] == self.QUESTION:
            self.board[tile]['state'] = self.CLOSED

        self.tiles_to_update.append(tile)



    def get_surrounding_tiles(self, tile: tuple[int, int]) -> list[tuple[int, int]]:
        surrounding_tiles = []
        neighbors = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (1, 0),
                    (-1, 1), (0, 1), (1, 1)]

        for a, b in neighbors:
            x = tile[0]+a
            y = tile[1]+b
            if 0 <= x < self.cols and 0 <= y < self.rows:
                surrounding_tiles.append((x, y))

        return surrounding_tiles


    def reveal_tile(self, tile: tuple[int, int]) -> None:
        if self.board[tile]['content'] == self.tile_content['bomb']:
            self.game_failed = True
            self.failed(tile)
            return
        
        if self.board[tile]['state'] == self.CLOSED or self.board[tile]['state'] == self.QUESTION:
            if self.board[tile]['content'] == self.tile_content['0']:
                self.board[tile]['state'] = self.OPEN
                self.closed_tiles.remove(tile)
                self.tiles_to_update.append(tile)
                cluster_tiles = self.get_surrounding_tiles(tile)
                for tile_xy in cluster_tiles:
                    self.reveal_tile(tile_xy)

            elif self.board[tile]['content'] != self.tile_content['0']:
                self.board[tile]['state'] = self.OPEN
                self.closed_tiles.remove(tile)
                self.tiles_to_update.append(tile)


    def hendle_chord(self, tile: tuple[int, int]) -> None:
        if self.board[tile]['content'] == self.tile_content['0']:
            return
        if self.board[tile]['state'] != self.OPEN:
            return

        tiles = self.get_surrounding_tiles(tile)
        num_flagged = 0
        num_bombs = 0
        chords = []
        for tile_xy in tiles:
            if self.board[tile_xy]['state'] == self.FLAGGED:
                num_flagged += 1
            if self.board[tile_xy]['content'] == self.tile_content['bomb']:
                num_bombs += 1
            if self.board[tile_xy]['state'] == self.CLOSED:
                chords.append(tile_xy)
        if num_flagged == num_bombs:
            for chord in chords:
                self.reveal_tile(chord)


    def failed(self, tile: tuple[int, int]) -> None:
        self.board[tile]['content'] = self.tile_content['fail']

        # Reveal missflagged tiles
        for tile_xy in self.closed_tiles:
            if self.board[tile_xy]['state'] == self.FLAGGED and self.board[tile_xy]['content'] != self.tile_content['bomb']:
                self.board[tile_xy]['state'] = self.MISSFLAGGED
                self.tiles_to_update.append(tile_xy)
        self.tiles_to_update.append(tile)
        self.is_game_active = False

        # Reveal all bombs
        for bomb in self.bomb_list:
            if self.board[bomb]['state'] != self.FLAGGED:
                self.board[bomb]['state'] = self.OPEN
                self.tiles_to_update.append(bomb)


    def flag_remaining_tiles(self) -> None:
        for tile in self.closed_tiles:
            if self.board[tile]['state'] != self.FLAGGED:
                self.board[tile]['state'] = self.FLAGGED
                self.num_flags += 1
                self.tiles_to_update.append(tile)