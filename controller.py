import pygame

from sys import exit

from model import BoardModel
from themes import ClassicTheme
from themes.sprites import Tile

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
        self.new_game()

        self.round_time = 0


    def main_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.update_theme('win31')
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.update_theme('win95')
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.update_theme('winxp')
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.update_theme('mono')

                if event.type == self.second and self.is_game_active and self.is_first_move == False:
                    self.gui.play_tick_sound()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.gui.update_face_sprite('faceooh')
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button press down animation
                    if self.face and self.face.rect.collidepoint(event.pos):
                        self.gui.update_face_sprite('opensmile')

                    # Menu bar buttons press down animation
                    # if self.icons[0].get_rect().collidepoint(mouse_pos):
                    #     self.icons[0].update('active')
                    #     self.icons[0].draw(self.screen)
                    # if self.icons[1].get_rect().collidepoint(mouse_pos):
                    #     self.icons[1].update('active')
                    #     self.icons[1].draw(self.screen)
                    # if self.icons[2].get_rect().collidepoint(mouse_pos):
                    #     self.icons[2].update('active')
                    #     self.icons[2].draw(self.screen)

            #         # Tiles press down animation
            #         # if tile_under_mouse:


                if event.type == pygame.MOUSEBUTTONUP:
                    self.gui.update_face_sprite(self.face_state)
                    mouse_pos = pygame.mouse.get_pos()
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Restart button click
                    if self.face and self.face.rect.collidepoint(event.pos):
                        self.new_game()

# region icons

                    # # Menu bar buttons click
                    # if self.icons[0].get_rect().collidepoint(mouse_pos):
                    #     self.icons[0].update('active')
                    #     self.icons[1].update('inactive')
                    #     self.icons[2].update('inactive')
                    #     self.rows = 9
                    #     self.cols = 9
                    #     self.bombs = 10
                    #     self.display_init()
                    #     self.new_board()
                        
                    # if self.icons[1].get_rect().collidepoint(mouse_pos):
                    #     self.icons[0].update('inactive')
                    #     self.icons[1].update('active')
                    #     self.icons[2].update('inactive')
                    #     self.rows = 16
                    #     self.cols = 16
                    #     self.bombs = 40
                    #     self.display_init()
                    #     self.new_board()

                    # if self.icons[2].get_rect().collidepoint(mouse_pos):
                    #     self.icons[0].update('inactive')
                    #     self.icons[1].update('active')
                    #     self.icons[2].update('inactive')
                    #     self.rows = 16
                    #     self.cols = 30
                    #     self.bombs = 99
                    #     self.display_init()
                    #     self.new_board()

# endregion

            # Game State Events
                    if not self.is_game_active: break

                    # Tile interaction
                    tile_under_mouse = self.get_tile_under_mouse(mouse_pos)

                    # Reveal (Left) click
                    if tile_under_mouse and event.button == 1:

                        if self.is_first_move:
                            self.round_time = pygame.time.get_ticks()
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



            # Updates unflagged bomb counter and timer
            if self.is_game_active and not self.is_first_move:
                self.gui.update_timer((pygame.time.get_ticks() - self.round_time)//1000)
            self.gui.update_mines_couter(self.board.get_unflagged_bombs_num())
                

            pygame.display.update()
            self.clock.tick(60)


    def display_init(self) -> None:

        self.gui = ClassicTheme(self.rows, self.cols)
        screen_size = self.gui.get_screen_size()
        self.screen = pygame.display.set_mode(screen_size)
        self.gui.load_screen(self.screen)
        self.gui.load_style_assets('mono')
        self.gui.draw_background()

        self.gui.built_info_sprites()
        self.gui.update_mines_couter(self.bombs)
        self.gui.update_timer(0)

        self.face = self.gui.get_face_sprite()

        # MAKE IT PART OF THEMES
        # # Draws menu bar icons
        # self.icons = []
        # self.menu_topleft = (4, self.ui_theme.menu_bar_height / 2)
        # self.icons.append(view.MenuIcon('beginner', 'inactive', 0, self.ui_theme.menu_icons, self.menu_topleft, 40))
        # self.icons.append(view.MenuIcon('intermediate', 'inactive', 1, self.ui_theme.menu_icons, self.menu_topleft, 40))
        # self.icons.append(view.MenuIcon('expert', 'inactive', 2, self.ui_theme.menu_icons, self.menu_topleft, 40))
        # # self.icons.append(view.MenuIcon('custom', 'inactive', 3, self.ui.menu_icons, self.menu_topleft, 40))

        # for icon in self.icons:
        #     icon.draw(self.screen)


    def new_game(self) -> None:
        self.board = BoardModel(self.rows, self.cols, self.bombs)
        self.is_first_move = True
        self.is_game_active = True
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
        self.gui.built_info_sprites()
        self.gui.update_face_sprite(self.face_state)
        self.draw_board(self.board.get_board(), self.board.get_all_tiles())



    def draw_board(self, board, all_tiles):
        # Variables for dict of Tile class elements
        self.tiles: dict[tuple[int, int], Tile] = {}

        for position in all_tiles:
            tile = Tile(position, self.gui.get_tile_images(), self.gui.get_board_topleft(), self.gui.get_tile_size())
            # self.tiles[position] = tile
            self.tiles[position] = tile
        self.draw_tiles(board, all_tiles)

        self.gui.update_timer(0)

    def draw_tiles(self, board, tiles_to_update: list[tuple[int, int]]) -> None:
        for position in tiles_to_update:
            self.tiles[position].update(board[position]['state'], board[position]['content'])
            self.tiles[position].draw(self.screen)






# class MenuIcon(pygame.sprite.Group):
#     def __init__(self, type: str, state: str, grid_pos: int, images: dict[str: pygame.surface.Surface], screen_midleft: tuple[int, int], spacing: int):
#         super().__init__()

#         self.type = type
#         self.images = images  # 'beginner_active', 'beginner_inactive', 'intermediate_active', 'intermediate_inactive', 'expert_active', 'expert_inactive', 'custom_active', 'custom_inactive'
#         self.image = self.images[f'{self.type}_{state}']
#         x = screen_midleft[0] + spacing * grid_pos
#         y = screen_midleft[1]
#         self.icon_rect = self.image.get_rect(midleft = (x, y))


#     def update(self, state: str) -> None:
#         self.image = self.images[f'{self.type}_{state}']


#     def draw(self, screen: pygame.surface.Surface) -> None:
#         screen.blit(self.image, self.icon_rect)


#     def get_rect(self) -> pygame.rect.Rect:
#         return self.icon_rect
