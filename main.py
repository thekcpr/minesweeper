import pygame
from random import randint
from sys import exit


class Minesweeper:  # Play State
    def __init__(self):
        self.rows = 9
        self.columns = 9
        self.num_bombs = 10

        # Variables for dict of Tile class elements
        self.tiles: dict[tuple[int, int], Tile] = {}
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
        
        pygame.init()
        pygame.display.set_caption('Minesweeper')
        self.second = pygame.USEREVENT + 1
        pygame.time.set_timer(self.second, 1000)

        self.round_time = 0

        self.board: dict[tuple[int, int], dict[str: str, str: str, str: str]] = {}  # dict of tile dicts
        self.empty_cell = {'state': 'closed', 'content': ''}  # states: closed / open / flagged / question. content: bomb, 0, 1, 2, 3, 4, 5, 6, 7, 8

        # Background variables
        self.ui_scale = 2
        self.beavel = 3 * self.ui_scale
        self.border = 6 * self.ui_scale

        self.info_beavel = 2 * self.ui_scale
        self.digit_beavel = 1 * self.ui_scale
        self.digit_width = 13 * self.ui_scale
        self.digit_height = 23 * self.ui_scale
        self.info_height = (2 * 4) * self.ui_scale + self.info_beavel + self.digit_height  # (4 + 1 + 23 + 1 + 4)

        self.tile_size = 16 * self.ui_scale

        self.mouse_is_down = False

        self.screen_width = 2 * self.border + 4 * self.beavel + self.tile_size * self.columns + 2.5
        self.screen_height = 3 * self.border + 4 * self.beavel + 2 * self.info_beavel + self.info_height + self.tile_size * self.rows + 2.5

        self.board_topleft = (2 * self.beavel + self.border + 1,
                              2 * self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height + 1)
        self.digits_bomb_topleft = (self.beavel + 2  * self.border + self.info_beavel + self.digit_beavel,
                                    self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + self.digit_beavel)
        self.digits_time_topleft = (self.screen_width - self.beavel - 2 * self.border - self.info_beavel - 2 * self.digit_beavel - 3 * self.digit_width,
                                    self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + self.digit_beavel)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.load_assets()
        self.new_game()


    def load_assets(self) -> None:
        self.tile_images = {'closed_blank': pygame.transform.scale_by(pygame.image.load('images/tile/closed_blank.png').convert(), self.ui_scale),
                            'closed_flagged': pygame.transform.scale_by(pygame.image.load('images/tile/closed_flagged.png').convert(), self.ui_scale),
                            'closed_question': pygame.transform.scale_by(pygame.image.load('images/tile/closed_question.png').convert(), self.ui_scale),
                            'open_bomb': pygame.transform.scale_by(pygame.image.load('images/tile/open_bomb.png').convert(), self.ui_scale),
                            'open_bomb_red': pygame.transform.scale_by(pygame.image.load('images/tile/open_bomb_red.png').convert(), self.ui_scale),
                            'open_bomb_missflagged': pygame.transform.scale_by(pygame.image.load('images/tile/open_bomb_missflagged.png').convert(), self.ui_scale),
                            'open_0': pygame.transform.scale_by(pygame.image.load('images/tile/open0.png').convert(), self.ui_scale),
                            'open_1': pygame.transform.scale_by(pygame.image.load('images/tile/open1.png').convert(), self.ui_scale),
                            'open_2': pygame.transform.scale_by(pygame.image.load('images/tile/open2.png').convert(), self.ui_scale),
                            'open_3': pygame.transform.scale_by(pygame.image.load('images/tile/open3.png').convert(), self.ui_scale),
                            'open_4': pygame.transform.scale_by(pygame.image.load('images/tile/open4.png').convert(), self.ui_scale),
                            'open_5': pygame.transform.scale_by(pygame.image.load('images/tile/open5.png').convert(), self.ui_scale),
                            'open_6': pygame.transform.scale_by(pygame.image.load('images/tile/open6.png').convert(), self.ui_scale),
                            'open_7': pygame.transform.scale_by(pygame.image.load('images/tile/open7.png').convert(), self.ui_scale),
                            'open_8': pygame.transform.scale_by(pygame.image.load('images/tile/open8.png').convert(), self.ui_scale)}
        
        self.digit_images = {'-': pygame.transform.scale_by(pygame.image.load('images/digit/-.png').convert(), self.ui_scale),
                             '0': pygame.transform.scale_by(pygame.image.load('images/digit/0.png').convert(), self.ui_scale),
                             '1': pygame.transform.scale_by(pygame.image.load('images/digit/1.png').convert(), self.ui_scale),
                             '2': pygame.transform.scale_by(pygame.image.load('images/digit/2.png').convert(), self.ui_scale),
                             '3': pygame.transform.scale_by(pygame.image.load('images/digit/3.png').convert(), self.ui_scale),
                             '4': pygame.transform.scale_by(pygame.image.load('images/digit/4.png').convert(), self.ui_scale),
                             '5': pygame.transform.scale_by(pygame.image.load('images/digit/5.png').convert(), self.ui_scale),
                             '6': pygame.transform.scale_by(pygame.image.load('images/digit/6.png').convert(), self.ui_scale),
                             '7': pygame.transform.scale_by(pygame.image.load('images/digit/7.png').convert(), self.ui_scale),
                             '8': pygame.transform.scale_by(pygame.image.load('images/digit/8.png').convert(), self.ui_scale),
                             '9': pygame.transform.scale_by(pygame.image.load('images/digit/9.png').convert(), self.ui_scale)}

        self.face_images = {'facesmile': pygame.transform.scale_by(pygame.image.load('images/face/facesmile.png').convert(), self.ui_scale),
                            'opensmile': pygame.transform.scale_by(pygame.image.load('images/face/opensmile.png').convert(), self.ui_scale),
                            'faceooh': pygame.transform.scale_by(pygame.image.load('images/face/faceooh.png').convert(), self.ui_scale),
                            'facewin': pygame.transform.scale_by(pygame.image.load('images/face/facewin.png').convert(), self.ui_scale),
                            'facedead': pygame.transform.scale_by(pygame.image.load('images/face/facedead.png').convert(), self.ui_scale)}
    


    def draw_background(self) -> None:
        self.screen.fill((192, 192, 192))
        # Border around the screen
        topleft = (0, 0)
        bottomright = (self.screen_width, self.screen_height)
        self.draw_bevaled_border(topleft, bottomright, self.beavel, 'outset')

        # Border around info bar
        topleft = (self.beavel + self.border,
                   self.beavel + self.border)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.beavel + self.border + 2 * self.info_beavel + self.info_height)
        self.draw_bevaled_border(topleft, bottomright, self.info_beavel, 'inset')

        # Border around tile board
        topleft = (self.beavel + self.border,
                   self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.screen_height - self.beavel - self.border)
        self.draw_bevaled_border(topleft, bottomright, self.beavel, 'inset')

        # Border around bomb counter
        topleft = (self.digits_bomb_topleft[0] - self.digit_beavel,
                   self.digits_bomb_topleft[1] - self.digit_beavel)
        bottomright = (topleft[0] + 3 * self.digit_width + 2 * self.digit_beavel,
                       topleft[1] + 2 * self.digit_beavel + self.digit_height)
        self.draw_bevaled_border(topleft, bottomright, self.digit_beavel, 'inset')

        # Border around timer
        topleft = (self.digits_time_topleft[0] - self.digit_beavel,
                   self.digits_time_topleft[1] - self.digit_beavel)
        bottomright = (topleft[0] + 3 * self.digit_width + 2 * self.digit_beavel,
                       topleft[1] + 2 * self.digit_beavel + self.digit_height)
        self.draw_bevaled_border(topleft, bottomright, self.digit_beavel, 'inset')


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
        for position in self.tiles_to_update:
            self.tiles[position].update(self.board[position]['state'], self.board[position]['content'])
            self.tiles[position].draw(self.screen)
        self.tiles_to_update = []



    def get_surrounding_tiles(self, tile: tuple[int, int]) -> list[tuple[int, int]]:
        surrounding_tiles = []
        neighbors = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (1, 0),
                    (-1, 1), (0, 1), (1, 1)]

        for a, b in neighbors:
            x = tile[0]+a
            y = tile[1]+b
            if 0 <= x < self.columns and 0 <= y < self.rows:
                surrounding_tiles.append((x, y))
        
        return surrounding_tiles


    def reveal(self, tile: tuple[int, int]) -> None:
        if self.is_first_move:
            self.is_first_move = False
            self.calculate_board(tile)
            self.reveal_tile(tile)

        if self.board[tile]['state'] == 'flagged':
            return

        else:
            self.hendle_chord(tile)
            self.reveal_tile(tile)


    def reveal_tile(self, tile: tuple[int, int]) -> None:
        if self.board[tile]['content'] == self.tile_content['bomb']:
            self.face.update('facedead')
            self.face.draw(self.screen)
            self.failed(tile)
            return
        if self.board[tile]['state'] == 'closed':
            if self.board[tile]['content'] == self.tile_content['0']:
                self.board[tile]['state'] = 'open'
                self.closed_tiles.remove(tile)
                self.tiles_to_update.append(tile)
                cluster_tiles = self.get_surrounding_tiles(tile)
                for tile_xy in cluster_tiles:
                    self.reveal_tile(tile_xy)

            elif self.board[tile]['content'] != self.tile_content['0']:
                self.board[tile]['state'] = 'open'
                self.closed_tiles.remove(tile)
                self.tiles_to_update.append(tile)


    def hendle_chord(self, tile: tuple[int, int]) -> bool:
        if self.board[tile]['content'] == self.tile_content['0']:
            return
        if self.board[tile]['state'] != 'open':
            return
        
        tiles = self.get_surrounding_tiles(tile)
        num_flagged = 0
        num_bombs = 0
        chords = []
        for tile_xy in tiles:
            if self.board[tile_xy]['state'] == 'flagged':
                num_flagged += 1
            if self.board[tile_xy]['content'] == self.tile_content['bomb']:
                num_bombs += 1
            if self.board[tile_xy]['state'] == 'closed' and self.board[tile_xy]['content'] != 'bomb':
                chords.append(tile_xy)
        if num_flagged == num_bombs:
            for chord in chords:
                self.reveal_tile(chord)


    def handle_flagging(self, tile: tuple[int, int]) -> None:
        if self.board[tile]['state'] == 'closed':
            self.board[tile]['state'] = 'flagged'
            self.num_flags += 1

        elif self.board[tile]['state'] == 'flagged':
            self.board[tile]['state'] = 'closed'
            self.num_flags -= 1

        self.tiles_to_update.append(tile)


    def calculate_board(self, first_tile: tuple[int, int]) -> None:

        # Fills board with bombs of random and unique coordinates, that are at least 1 cell away of player's first click
        safe_tiles = self.get_surrounding_tiles(first_tile)
        safe_tiles.append(first_tile)

        while len(self.bomb_list) < self.num_bombs:
            bomb_x = randint(0, self.columns-1)
            bomb_y = randint(0, self.rows-1)
            bomb_tile = (bomb_x, bomb_y)
        
            if bomb_tile not in self.bomb_list and bomb_tile not in safe_tiles:
                self.bomb_list.append(bomb_tile)
                self.board[bomb_tile]['content'] = self.tile_content['bomb']

        # Calculates number of bombs around each cell and injects it into the board
        for x in range(self.columns):
            for y in range(self.rows):
                
                if self.board[(x, y)]["content"] != self.tile_content["bomb"]:
                    bomb_count = 0
                    
                    # print(f'{(x, y)}, {self.get_surrounding_tiles((x, y))}')
                    # TODO: Learn about generator expressions to reduce nesting
                    for tile in self.get_surrounding_tiles((x, y)):
                        if self.board[tile]["content"] == self.tile_content["bomb"]:
                            bomb_count += 1
                    self.board[(x, y)]["content"] = self.tile_content[f"{bomb_count}"]
                # else:
                    # print(f'{(x, y)}, Bomb')


    def failed(self, tile: tuple[int, int]) -> None:
        self.board[tile]['content'] = self.tile_content['fail']
        for tile_xy in self.closed_tiles:
            if self.board[tile_xy]['state'] == 'flagged' and self.board[tile_xy]['content'] != self.tile_content['bomb']:
                self.board[tile_xy]['state'] = 'missflagged'
                self.tiles_to_update.append(tile_xy)
        self.tiles_to_update.append(tile)
        self.is_game_active = False
        for bomb in self.bomb_list:
            self.board[bomb]['state'] = 'open'
            self.tiles_to_update.append(bomb)




    def main_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.face.update('faceooh')
                    self.face.draw(self.screen)
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button press down animation
                    if self.face.get_rect().collidepoint(mouse_pos):
                        self.face.update('opensmile')
                        self.face.draw(self.screen)

                    # Tiles press down animation
                    # if tile_under_mouse:


                if event.type == pygame.MOUSEBUTTONUP:
                    self.face.update('facesmile')
                    self.face.draw(self.screen)
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button click
                    if self.face.get_rect().collidepoint(mouse_pos):
                        self.face.update('opensmile')
                        self.face.draw(self.screen)
                        self.new_game()

                if event.type == pygame.MOUSEBUTTONUP and self.is_game_active:

                    # Tile interaction
                    if tile_under_mouse and event.button == 1:
                        self.reveal(tile_under_mouse)
                        self.draw_tiles()
                    if tile_under_mouse and event.button == 3:
                        self.handle_flagging(tile_under_mouse)
                        self.draw_tiles()

            # Solved condition
            if len(self.closed_tiles) == self.num_bombs:
                self.is_game_active = False
                self.face.update('facewin')
                self.face.draw(self.screen)
                self.flag_remaining_tiles()

            # Remaining bomb counter digits
            bombs_left = str(self.num_bombs - self.num_flags).zfill(3)
            self.info_bomb[0].update(bombs_left[-3])
            self.info_bomb[1].update(bombs_left[-2])
            self.info_bomb[2].update(bombs_left[-1])
            
            # Timer
            time_elapsed = str(pygame.time.get_ticks() - self.round_time).zfill(6)
            self.info_time[0].update(time_elapsed[-6])
            self.info_time[1].update(time_elapsed[-5])
            self.info_time[2].update(time_elapsed[-4])

            # Updates remaining bomb counter digits
            self.info_bomb[0].draw(self.screen)
            self.info_bomb[1].draw(self.screen)
            self.info_bomb[2].draw(self.screen)

            if self.is_game_active:
                # Updates timer
                self.info_time[0].draw(self.screen)
                self.info_time[1].draw(self.screen)
                self.info_time[2].draw(self.screen)
                

            pygame.display.update()
            self.clock.tick(60)


    def get_tile_under_mouse(self, position) -> tuple[int, int] | bool:
        x = (position[0] - self.board_topleft[0]) // self.tile_size
        y = (position[1] - self.board_topleft[1]) // self.tile_size
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return (x, y)
        else: return False


    def new_game(self) -> None:
        self.is_game_active = True
        self.is_first_move = True
        self.bomb_list = []
        self.closed_tiles = []
        self.num_flags = 0
        self.round_time = pygame.time.get_ticks()

        # Generates dict of board without content
        for x in range(self.columns):
            for y in range(self.rows):
                self.board[(x, y)] = self.empty_cell.copy()
                self.closed_tiles.append((x, y))

        self.tiles_to_update = self.closed_tiles.copy()

        # Draws UI elements
        self.draw_background()
        
        # Draws info bar content
        self.face = SmileFace(self.face_images, self.screen_width, self.ui_scale)
        self.face.draw(self.screen)

        self.info_bomb = []
        self.info_time = []

        for i in range(0, 3):
            self.info_bomb.append(Digit(i, self.digit_images, self.digits_bomb_topleft, self.digit_width, self.ui_scale))
            self.info_time.append(Digit(i, self.digit_images, self.digits_time_topleft, self.digit_width, self.ui_scale))
            self.info_bomb[i].draw(self.screen)
            self.info_time[i].draw(self.screen)

        # Draws board
        for position in self.closed_tiles:
            tile = Tile(position, self.tile_images, self.board_topleft, self.tile_size, self.ui_scale)
            self.tiles[position] = tile
        self.draw_tiles()


    def flag_remaining_tiles(self) -> None:
        for tile in self.closed_tiles:
            if self.board[tile]['state'] != 'flagged':
                self.handle_flagging(tile)
        self.draw_tiles()


class Tile(pygame.sprite.Group):
    def __init__(self, grid_pos: tuple[int, int], images: dict[str: pygame.surface.Surface], screen_topleft: tuple[int, int], tile_size: int, ui_scale: int):
        super().__init__()

        self.images = images  # 'closed_blank', 'closed_flag', 'closed_question', 'open_bomb', 'open_bomb_red', 'open_bomb_missflagged'
                              # 'open_0', 'open_1', 'open_2', 'open_3', 'open_4', 'open_5', 'open_6', 'open_7', 'open_8'
        self.image = self.images['closed_blank']
        tile_x = screen_topleft[0] + tile_size * grid_pos[0]
        tile_y = screen_topleft[1] + tile_size * grid_pos[1]
        self.tile_rect = self.image.get_rect(topleft = (tile_x, tile_y))


    def update(self, state: str, content: str) -> None:
        self.state = state  # 'closed', 'open', 'flagged', 'question', 'hover'
        if self.state == 'hover': self.image = self.images['open_0']
        if self.state == 'closed': self.image = self.images['closed_blank']
        if self.state == 'missflagged': self.image = self.images['open_bomb_missflagged']
        if self.state == 'flagged': self.image = self.images['closed_flagged']
        if self.state == 'open': self.image = self.images[content]

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.tile_rect)
        print(type(screen))

class Digit(pygame.sprite.Group):
    def __init__(self, grid_pos: int, images: dict[str: pygame.surface.Surface], screen_topleft: tuple[int, int], digit_size: int, ui_scale: int):
        super().__init__()

        self.images = images  # '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        self.image = self.images['0']
        tile_x = screen_topleft[0] + digit_size * grid_pos
        tile_y = screen_topleft[1]
        self.digit_rect = self.image.get_rect(topleft = (tile_x, tile_y))
    

    def update(self, content: str) -> None:
        self.image = self.images[content]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.digit_rect)

class SmileFace(pygame.sprite.Sprite):
    def __init__(self, images: dict[str: pygame.surface.Surface], screen_width: int, ui_scale: int):
        super().__init__()

        self.images = images  # 'facesmile', 'opensmile', 'faceooh', 'facewin', 'facedead'
        self.image = self.images['facesmile']
        self.smile_rect = self.image.get_rect(midtop = (screen_width / ui_scale, 30))


    def update(self, state: str):
        self.image = self.images[state]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.smile_rect)


    def get_rect(self) -> pygame.rect.Rect:
        return self.smile_rect


if __name__ == "__main__":
    game = Minesweeper()
    game.main_loop()
