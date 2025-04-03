import pygame

from sys import exit

from model import BoardModel
import view


class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        icon = pygame.image.load('images/icon/Minesweeper_Icon_App-assets/Icon-macOS-256x256@1x.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Minesweeper')

        self.rows = 9
        self.cols = 9
        self.bombs = 10

        self.is_first_move = True
        self.is_board_not_solved = True
        self.is_game_active = True

        self.display_init()
        self.new_board()

        self.round_time = 0


    def main_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.second and self.is_game_active and self.is_first_move == False:
                    pass
                    self.ui.play_tick_sound()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ui.update_restart_button('faceooh')
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button press down animation
                    if self.ui.face.get_rect().collidepoint(mouse_pos):
                        self.ui.update_restart_button('opensmile')

                    # Menu bar buttons press down animation
                    if self.icons[0].get_rect().collidepoint(mouse_pos):
                        self.icons[0].update('active')
                        self.icons[0].draw(self.screen)
                    if self.icons[1].get_rect().collidepoint(mouse_pos):
                        self.icons[1].update('active')
                        self.icons[1].draw(self.screen)
                    if self.icons[2].get_rect().collidepoint(mouse_pos):
                        self.icons[2].update('active')
                        self.icons[2].draw(self.screen)

            #         # Tiles press down animation
            #         # if tile_under_mouse:


                if event.type == pygame.MOUSEBUTTONUP:
                    self.ui.update_restart_button('facesmile')
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button click
                    if self.ui.face.get_rect().collidepoint(mouse_pos):
                        self.new_board()

                    # Menu bar buttons click
                    if self.icons[0].get_rect().collidepoint(mouse_pos):
                        self.icons[0].update('active')
                        self.icons[1].update('inactive')
                        self.icons[2].update('inactive')
                        self.rows = 9
                        self.cols = 9
                        self.bombs = 10
                        self.display_init()
                        self.new_board()
                        
                    if self.icons[1].get_rect().collidepoint(mouse_pos):
                        self.icons[0].update('inactive')
                        self.icons[1].update('active')
                        self.icons[2].update('inactive')
                        self.rows = 16
                        self.cols = 16
                        self.bombs = 40
                        self.display_init()
                        self.new_board()

                    if self.icons[2].get_rect().collidepoint(mouse_pos):
                        self.icons[0].update('inactive')
                        self.icons[1].update('active')
                        self.icons[2].update('inactive')
                        self.rows = 16
                        self.cols = 30
                        self.bombs = 99
                        self.display_init()
                        self.new_board()


            # Game State Events
                    if not self.is_game_active: break

                    # Tile interaction
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)
                    if tile_under_mouse and self.is_first_move:
                        self.round_time = pygame.time.get_ticks()
                        self.is_first_move = False
                        self.board.generate_board(tile_under_mouse)
                        self.board.reveal_tile(tile_under_mouse)
                        self.update_tiles(self.board.get_tiles_to_update())

                    # Reveal (Left) click
                    elif tile_under_mouse and event.button == 1:
                        self.board.reveal(tile_under_mouse)
                        self.update_tiles(self.board.get_tiles_to_update())

                        # Solved condition
                        if self.board.is_solved():
                            self.is_game_active = False
                            self.ui.play_win_sound()
                            self.ui.update_restart_button('facewin')
                            self.board.flag_remaining_tiles()
                            self.update_tiles(self.board.get_tiles_to_update())

                        # Failed condition
                        if self.board.is_failed():
                            self.is_game_active = False
                            self.ui.play_lose_sound()
                            self.ui.update_restart_button('facedead')

                    # Flag (Right) click
                    elif tile_under_mouse and event.button == 3:
                        self.board.handle_right_click(tile_under_mouse)
                        self.update_tiles(self.board.get_tiles_to_update())



            # Updates unflagged bomb counter and timer
            if self.is_game_active and not self.is_first_move:
                self.ui.update_time_digits(pygame.time.get_ticks() - self.round_time)
            self.ui.update_bomb_digits(self.board.get_unflagged_bombs_num())

                

            pygame.display.update()
            self.clock.tick(60)


    def display_init(self) -> None:
        self.ui = view.WindowsXPView(self.rows, self.cols)
        self.screen = self.ui.get_screen()

        # Draws menu bar icons
        self.icons = []
        self.menu_topleft = (4, self.ui.menu_bar_height / 2)
        self.icons.append(view.MenuIcon('beginner', 'inactive', 0, self.ui.menu_icons, self.menu_topleft, 40))
        self.icons.append(view.MenuIcon('intermediate', 'inactive', 1, self.ui.menu_icons, self.menu_topleft, 40))
        self.icons.append(view.MenuIcon('expert', 'inactive', 2, self.ui.menu_icons, self.menu_topleft, 40))
        # self.icons.append(view.MenuIcon('custom', 'inactive', 3, self.ui.menu_icons, self.menu_topleft, 40))

        for icon in self.icons:
            icon.draw(self.screen)


    def new_board(self) -> None:
        self.board = BoardModel(self.rows, self.cols, self.bombs)
        self.is_first_move = True
        self.is_game_active = True

        # Variables for dict of Tile class elements
        self.tiles: dict[tuple[int, int], view.Tile] = {}

        # Draws board
        for position in self.board.get_unrevealed_tiles():
            tile = view.Tile(position, self.ui.get_tile_images(), self.ui.get_board_topleft(), self.ui.get_tile_size())
            # self.tiles[position] = tile
            self.tiles[position] = tile
        self.update_tiles(self.board.get_unrevealed_tiles())

        self.clock = pygame.time.Clock()
        self.second = pygame.USEREVENT + 1
        pygame.time.set_timer(self.second, 1000)


    def get_tile_under_mouse(self, position) -> tuple[int, int] | bool:
        x = (position[0] - self.ui.get_board_topleft()[0]) // self.ui.get_tile_size()
        y = (position[1] - self.ui.get_board_topleft()[1]) // self.ui.get_tile_size()
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return (x, y)
        else: return False


    def update_tiles(self, tiles_to_update: list[tuple[int, int]]) -> None:
        board = self.board.get_board()
        for position in tiles_to_update:
            self.tiles[position].update(board[position]['state'], board[position]['content'])
            self.tiles[position].draw(self.screen)