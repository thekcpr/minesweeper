import pygame
from random import randint
from sys import exit

# TODO:
# - Implement flagging
# - Implement remaining mines counter
# - Implement timer
# - Implement chord reveal
# - Implement options menu
# - Implement pop up window to Fialed and Solved State
# - Implement scoreboard
# - Add docstrings to all functions

# - Implement board solver to check if generated board is solvable without guessing

# - Implement different classes with Game States?
# - Implement Protocol from typing?


class OptionState: pass

class Minesweeper:  # Play State
    def __init__(self):
        self.rows = 16
        self.columns = 16
        self.num_bombs = 40

        self.is_first_move = True
        self.bomb_list = []
        self.open_tiles = []

        # Variables for dict of Tile class elements
        self.tiles: dict[tuple[int, int], Tile] = {}
        self.tile_content = {"bomb": "open_bomb",
                             "fail": "open_bomb_red",
                             "0": "open_0",
                             "1": "open_1",
                             "2": "open_2",
                             "3": "open_3",
                             "4": "open_4",
                             "5": "open_5",
                             "6": "open_6",
                             "7": "open_7",
                             "8": "open_8"}
        
        pygame.init()
        pygame.display.set_caption('Minesweeper')

        self.board: dict[tuple[int, int], dict[str: str, str: str, str: str]] = {}  # dict of tile dicts
        self.empty_cell = {'state': 'closed', 'content': ''}  # states: closed / open / flagged / question. content: bomb, 0, 1, 2, 3, 4, 5, 6, 7, 8

        # Background variables
        self.ui_scale = 2
        self.beavel = 3 * self.ui_scale
        self.border = 6 * self.ui_scale

        self.info_beavel = 2 * self.ui_scale
        self.time_beavel = 1 * self.ui_scale
        self.time_width = 13 * self.ui_scale
        self.time_height = 23 * self.ui_scale
        self.info_height = (2 * 4) * self.ui_scale + self.info_beavel + self.time_height  # (4 + 1 + 23 + 1 + 4)

        self.tile_size = 16 * self.ui_scale
        self.tile_topleft = (2 * self.beavel + self.border + 1, 2* self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height + 1)
        self.mouse_is_down = False

        self.screen_width = 2 * self.border + 4 * self.beavel + self.tile_size * self.rows + 2.5
        self.screen_height = 3 * self.border + 4 * self.beavel + 2 * self.info_beavel + self.info_height + self.tile_size * self.columns + 2.5

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.new_game()


    def draw_background(self) -> None:
        self.screen.fill((192, 192, 192))
        self.draw_bevaled_border((0, 0), (self.screen_width, self.screen_height), self.beavel, 'outset')

        topleft = (self.beavel + self.border,
                   self.beavel + self.border)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.beavel + self.border + 2 * self.info_beavel + self.info_height)
        self.draw_bevaled_border(topleft, bottomright, self.info_beavel , 'inset')

        topleft = (self.beavel + self.border,
                   self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.screen_height - self.beavel - self.border)
        self.draw_bevaled_border(topleft, bottomright, self.beavel , 'inset')

        topleft = (self.beavel + self.border + self.info_beavel + self.border,
                   self.beavel + self.border + self.info_beavel + 4 * self.ui_scale)
        bottomright = (topleft[0] + 3 * self.time_width + 2 * self.time_beavel,
                       topleft[1] + 2 * self.time_beavel + self.time_height)
        self.draw_bevaled_border(topleft, bottomright, self.time_beavel , 'inset')

        bottomright = (self.screen_width - self.beavel - self.border - self.info_beavel - self.border,
                       self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + 2 * self.time_beavel + self.time_height)
        topleft = (bottomright[0] - 3 * self.time_width - 2 * self.time_beavel,
                   bottomright[1] - 2 * self.time_beavel - self.time_height)
        self.draw_bevaled_border(topleft, bottomright, 2 , 'inset')


    def draw_bevaled_border(self, topleft: tuple[int, int], bottomright: tuple[int, int], thickness: int, type: str) -> None:
        if type == 'outset': color = ('White', (128, 128, 128))
        if type == 'inset': color = ((128, 128, 128), 'White')
        points = {'topleft': (topleft[0], topleft[1]),
                  'inner_topleft': (topleft[0] + thickness, topleft[1] + thickness),
                  'topright': (bottomright[0], topleft[1]),
                  'inner_topright': (bottomright[0] - thickness, topleft[1] + thickness),
                  'bottomright': (bottomright[0], bottomright[1]),
                  'inner_bottomright': (bottomright[0] - thickness, bottomright[1] - thickness),
                  'bottomleft': (topleft[0], bottomright[1]), 
                  'inner_bottomleft': (topleft[0] + thickness, bottomright[1] - thickness)}
        pygame.draw.polygon(self.screen, color[0], [points['topleft'],
                                                    points['bottomleft'],
                                                    points['inner_bottomleft'],
                                                    points['inner_topleft'],
                                                    points['inner_topright'],
                                                    points['topright']])
        pygame.draw.polygon(self.screen, color[1], [points['bottomright'],
                                                    points['topright'],
                                                    points['inner_topright'],
                                                    points['inner_bottomright'],
                                                    points['inner_bottomleft'],
                                                    points['bottomleft']])
        del points


    def draw_tiles(self) -> None:
        for position in self.open_tiles:
            tile = Tile(position, self.board[position]['state'], self.board[position]['content'], self.tile_topleft, self.tile_size)
            self.tiles[position] = tile
            self.tiles[position].draw(self.screen)



    def get_surrounding_tiles(self, tile: tuple[int, int]) -> list[tuple[int, int]]:
        surrounding_cells = []
        neighbors = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, +1),
                    (1, -1), (1, 0), (1, 1)]

        for b, a in neighbors:
            y = tile[0]+b
            x = tile[1]+a
            if 0 <= y < self.rows and 0 <= x < self.columns:
                surrounding_cells.append((y, x))
        
        return surrounding_cells


    def reveal(self, tile: tuple[int, int]) -> None:
        if self.is_first_move:
            self.is_first_move = False
            self.calculate_board(tile)
            self.reveal_tile(tile)

        elif self.board[tile]['content'] == self.tile_content['bomb']:
            self.end_game(tile)

        elif self.is_chord(tile):
            print('True')
            # self.reveal_chord(tile)

        else:
            self.reveal_tile(tile)


    def reveal_tile(self, tile: tuple[int, int]) -> None:
        if self.board[(tile)]['state'] == 'closed':
            if self.board[(tile)]['content'] == self.tile_content['0']:
                self.board[tile]['state'] = 'open'
                cluster_tiles = self.get_surrounding_tiles(tile)
                for tile_xy in cluster_tiles:
                    self.reveal_tile(tile_xy)

            elif self.board[(tile)]['content'] != self.tile_content['0']:
                self.board[tile]['state'] = 'open'


    def is_chord(self, tile: tuple[int, int]) -> bool:
        # Make if statement work properly
        if self.board[tile]['content'] == self.tile_content['bomb']: return False
        if self.board[tile]['content'] == self.tile_content['0']: return False
        if self.board[tile]['state'] != 'open': return False
        
        tiles = self.get_surrounding_tiles(tile)
        print(tiles)
        num_flagged = 0
        num_bombs = 0
        for tile_xy in tiles:
            print(tile_xy)
            if self.board[tile_xy]['state'] == 'flagged':
                print('flaga')
                num_flagged += 1
            if self.board[tile_xy]['content'] == self.tile_content['bomb']:
                print('bomba')
                num_bombs += 1
        if num_flagged == num_bombs:
            return True


    def reveal_chord(self, tile: tuple[int, int]) -> None:
        self.board[tile]['state'] = 'open'
        print(tile)
        # self.open_tiles.remove(tile)


    def calculate_board(self, first_choice: tuple[int, int]) -> None:

        # Fills board with bombs of random and unique coordinates, that are at least 1 cell away of player's first click
        safe_tiles = self.get_surrounding_tiles(first_choice)
        safe_tiles.append(first_choice)

        while len(self.bomb_list) < self.num_bombs:
            bomb_y = randint(0, self.rows-1)
            bomb_x = randint(0, self.columns-1)
            bomb_tile = (bomb_y, bomb_x)
        
            if bomb_tile not in self.bomb_list and bomb_tile not in safe_tiles:
                self.bomb_list.append(bomb_tile)
                self.board[bomb_tile]['content'] = self.tile_content['bomb']

        # Calculates number of bombs around each cell and injects it into the board
        for x in range(self.rows):
            for y in range(self.columns):
                
                if self.board[(x, y)]["content"] != self.tile_content["bomb"]:
                    bomb_count = 0

                    # TODO: Learn about generator expressions and reduce nesting
                    for tile in self.get_surrounding_tiles((x, y)):
                        if self.board[tile]["content"] == self.tile_content["bomb"]:
                            bomb_count += 1
                        self.board[(x, y)]["content"] = self.tile_content[f"{bomb_count}"]              


    def end_game(self, tile: tuple[int, int]) -> None:
        print(f'Koniec gierki {tile}')



    def main_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.face = SmileFace(self.screen_width, 'faceooh')
                    self.face.draw(self.screen)
                    # if self.get_tile_under_mouse(pygame.mouse.get_pos()):
                    #     self.update_board(self.get_tile_under_mouse(pygame.mouse.get_pos()))
                    #     self.update_tiles()
                    
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.face = SmileFace(self.screen_width, 'facesmile')
                    self.face.draw(self.screen)
                    tile_uder_mouse = self.get_tile_under_mouse(pygame.mouse.get_pos())
                    if tile_uder_mouse:
                        self.reveal(tile_uder_mouse)
                        self.draw_tiles()


            pygame.display.update()
            self.clock.tick(60)


    def get_tile_under_mouse(self, position) -> tuple[int, int] | bool:
        x = (position[0] - self.tile_topleft[0]) // self.tile_size
        y = (position[1] - self.tile_topleft[1]) // self.tile_size
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return (x, y)
        else: return False


    def new_game(self) -> None:
        # Generates dict of board without content
        for x in range(self.rows):
            for y in range(self.columns):
                self.board[(x, y)] = self.empty_cell.copy()
                self.open_tiles.append((x, y))

        # Draw UI elements
        self.draw_background()
        
        self.face = SmileFace(self.screen_width, 'facesmile')
        self.face.draw(self.screen)
        self.draw_tiles()






class SolvedState: pass

class FailedState: pass

class Tile(pygame.sprite.Group):
    def __init__(self, position: tuple[int, int], state: str, content: str, tile_topleft, tile_size):
        super().__init__()

        self.tile_image = {'closed_blank': pygame.image.load('images/tile/closed_blank.png').convert(),
                      'closed_flagged': pygame.image.load('images/tile/closed_flagged.png').convert(),
                      'closed_question': pygame.image.load('images/tile/closed_question.png').convert(),
                      'open_bomb': pygame.image.load('images/tile/open_bomb.png').convert(),
                      'open_bomb_red': pygame.image.load('images/tile/open_bomb_red.png').convert(),
                      'open_bomb_missflagged': pygame.image.load('images/tile/open_bomb_missflagged.png').convert(),
                      'open_0': pygame.image.load('images/tile/open0.png').convert(),
                      'open_1': pygame.image.load('images/tile/open1.png').convert(),
                      'open_2': pygame.image.load('images/tile/open2.png').convert(),
                      'open_3': pygame.image.load('images/tile/open3.png').convert(),
                      'open_4': pygame.image.load('images/tile/open4.png').convert(),
                      'open_5': pygame.image.load('images/tile/open5.png').convert(),
                      'open_6': pygame.image.load('images/tile/open6.png').convert(),
                      'open_7': pygame.image.load('images/tile/open7.png').convert(),
                      'open_8': pygame.image.load('images/tile/open8.png').convert()}

        self.position = position
        self.state = state  # closed, open, flagged, question, hover
        self.content = content

        if self.state == 'hover': self.image = self.tile_image['open_0']
        if self.state == 'closed': self.image = self.tile_image['closed_blank']
        if self.state == 'open': self.image = self.tile_image[content]

        self.image_scaled = pygame.transform.scale_by(self.image, 2)
        tile_x = tile_topleft[0] + tile_size * self.position[0]
        tile_y = tile_topleft[1] + tile_size * self.position[1]
        self.tile_rect = self.image_scaled.get_rect(topleft = (tile_x, tile_y))

    def draw(self, screen):
        screen.blit((self.image_scaled), self.tile_rect)

class Digit(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        digit_image = {'-': pygame.image.load('images/digit/-.png'),
                       '0': pygame.image.load('images/digit/0.png'),
                       '1': pygame.image.load('images/digit/1.png'),
                       '2': pygame.image.load('images/digit/2.png'),
                       '3': pygame.image.load('images/digit/3.png'),
                       '4': pygame.image.load('images/digit/4.png'),
                       '5': pygame.image.load('images/digit/5.png'),
                       '6': pygame.image.load('images/digit/6.png'),
                       '7': pygame.image.load('images/digit/7.png'),
                       '8': pygame.image.load('images/digit/8.png'),
                       '9': pygame.image.load('images/digit/9.png')}
        self.image = digit_image['0']

class SmileFace(pygame.sprite.Sprite):
    def __init__(self, board_width, state):
        super().__init__()

        self.images = {'facesmile': pygame.image.load('images/face/facesmile.png').convert(),
                       'opensmile': pygame.image.load('images/face/opensmile.png').convert(),
                        'faceooh': pygame.image.load('images/face/faceooh.png').convert(),
                        'facesmile': pygame.image.load('images/face/facesmile.png').convert(),
                        'facewin': pygame.image.load('images/face/facewin.png').convert()}
        
        self.image = pygame.transform.scale_by(self.images[state], 2)
        self.smile_rect = self.image.get_rect(midtop = (board_width / 2, 30))


    def draw(self, screen) -> None:
        screen.blit(self.image, self.smile_rect)

    def get_rect(self) -> pygame.rect.Rect:
        return self.smile_rect


if __name__ == "__main__":
    game = Minesweeper()
    game.main_loop()
