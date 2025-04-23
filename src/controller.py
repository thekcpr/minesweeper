import pygame

from sys import exit

from model import BoardModel
from view import ClassicTheme
from view.sprites import Tile

class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        icon = pygame.image.load('assets/icon/Icon-macOS-256x256@1x.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Minesweeper')

        self.rows = 9
        self.cols = 9
        self.bombs = 10

        self.style = 'winxp'

        self.is_first_move = True
        self.is_board_not_solved = True
        self.is_game_active = True
        self.is_button_pressed = False
        self.hover_tile = None

        self.round_start_time = 0
        self.time = 0

        self.display_init()
        self.new_game()


    def main_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.style = 'win31'
                    self.update_theme(self.style)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.style = 'win95'
                    self.update_theme(self.style)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.style = 'winxp'
                    self.update_theme(self.style)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.style = 'mono'
                    self.update_theme(self.style)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    self.rows = 9
                    self.cols = 9
                    self.bombs = 10
                    self.display_init()
                    self.new_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    self.rows = 16
                    self.cols = 16
                    self.bombs = 40
                    self.display_init()
                    self.new_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.rows = 16
                    self.cols = 30
                    self.bombs = 99
                    self.display_init()
                    self.new_game()

                if event.type == self.second and self.is_game_active and self.is_first_move == False:
                    self.gui.play_tick_sound()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.is_button_pressed = True
                    if self.is_game_active:
                        self.gui.update_face_sprite('faceooh')
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button press down animation
                    if self.face and self.face.rect.collidepoint(event.pos):
                        self.gui.update_face_sprite('opensmile')

                if event.type == pygame.MOUSEMOTION and self.is_button_pressed:
                    if not self.face.rect.collidepoint(event.pos):
                        self.gui.update_face_sprite(self.face_state)  # przestań wyglądać na wciśniętą
                    else:
                        self.gui.update_face_sprite('opensmile')  # nadal wciśnięta
                    if self.get_tile_under_mouse(event.pos) and self.is_game_active:
                        self.gui.update_face_sprite('faceooh')

                if event.type == pygame.MOUSEBUTTONUP:
                    self.is_button_pressed = False
                    self.gui.update_face_sprite(self.face_state)
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button click
                    if self.face and self.face.rect.collidepoint(event.pos):
                        self.new_game()

            # Game State Events
                    if not self.is_game_active: break

                    # Tile interaction
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Reveal (Left) click
                    if tile_under_mouse and event.button == 1:

                        if self.is_first_move:
                            self.round_start_time = pygame.time.get_ticks()
                            self.is_first_move = False
                            self.board.generate_board(tile_under_mouse)

                        self.board.reveal(tile_under_mouse)
                        self.draw_tiles(self.board.get_board(), self.board.get_tiles_to_update())

                        # Solved condition
                        if self.board.is_solved():
                            self.is_game_active = False
                            self.gui.play_win_sound()
                            self.face_state = 'facewin'
                            self.gui.update_face_sprite(self.face_state)
                            self.board.flag_remaining_tiles()
                            self.draw_tiles(self.board.get_board(), self.board.get_tiles_to_update())

                        # Failed condition
                        if self.board.is_failed():
                            self.is_game_active = False
                            self.gui.play_lose_sound()
                            self.face_state = 'facedead'
                            self.gui.update_face_sprite(self.face_state)

                    # Flag (Right) click
                    elif tile_under_mouse and event.button == 3:
                        self.board.handle_right_click(tile_under_mouse)
                        self.draw_tiles(self.board.get_board(), self.board.get_tiles_to_update())

            if self.is_game_active and self.is_button_pressed:
                current_hover = self.get_tile_under_mouse(pygame.mouse.get_pos())
                if current_hover != self.hover_tile:
                    if self.hover_tile:
                        self.tiles[self.hover_tile].draw(self.screen)
                    if current_hover:
                        self.tiles[current_hover].draw_hover(self.screen)
                    
                    self.hover_tile = current_hover


            # Updates unflagged bomb counter and timer
            if self.is_game_active and not self.is_first_move:
                self.time = (pygame.time.get_ticks() - self.round_start_time)//1000
                self.gui.update_timer(self.time)
            self.gui.update_mines_couter(self.board.get_unflagged_bombs_num())
                

            pygame.display.update()
            self.clock.tick(60)


    def display_init(self) -> None:
        self.gui = ClassicTheme(self.rows, self.cols)
        screen_size = self.gui.get_screen_size()
        self.screen = pygame.display.set_mode(screen_size)
        self.gui.load_screen(self.screen)
        self.gui.load_style_assets(self.style)
        self.gui.draw_background()

        self.gui.build_info_sprites()
        self.gui.update_mines_couter(self.bombs)
        self.gui.update_timer(0)

        self.face = self.gui.get_face_sprite()


    def new_game(self) -> None:
        self.board = BoardModel(self.rows, self.cols, self.bombs)
        self.is_first_move = True
        self.is_game_active = True
        self.time = 0
        self.face_state = 'facesmile'
        self.gui.update_face_sprite(self.face_state)

        self.draw_board(self.board.get_board(), self.board.get_unrevealed_tiles())
        self.clock = pygame.time.Clock()
        self.second = pygame.USEREVENT + 1
        pygame.time.set_timer(self.second, 1000)


    def get_tile_under_mouse(self, position) -> tuple[int, int] | bool:
        x = (position[0] - self.gui.get_board_topleft()[0]) // self.gui.get_tile_size()
        y = (position[1] - self.gui.get_board_topleft()[1]) // self.gui.get_tile_size()
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return (x, y)
        else: return False


    def update_theme(self, style: str) -> None:
        self.gui.load_style_assets(style)
        self.gui.draw_background()
        self.gui.build_info_sprites()
        self.gui.update_face_sprite(self.face_state)
        self.draw_board(self.board.get_board(), self.board.get_all_tiles())


    def draw_board(self, board: dict[tuple[int, int]: dict[str: str, str: str]], all_tiles: list[tuple[int, int]]):
        # Variables for dict of Tile class elements
        self.tiles: dict[tuple[int, int], Tile] = {}

        for position in all_tiles:
            tile = Tile(position, self.gui.get_tile_images(), self.gui.get_board_topleft(), self.gui.get_tile_size())
            self.tiles[position] = tile
        self.draw_tiles(board, all_tiles)

        self.gui.update_timer(self.time)


    def draw_tiles(self, board: dict[tuple[int, int]: dict[str: str, str: str]], tiles_to_update: list[tuple[int, int]]) -> None:
        for position in tiles_to_update:
            self.tiles[position].update(board[position]['state'], board[position]['content'])
            self.tiles[position].draw(self.screen)