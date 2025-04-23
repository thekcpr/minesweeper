import pygame
import pygame.gfxdraw
import json
from .base_theme import Theme
from .sprites import ThreeDigitDisplay, SmileFace

class ClassicTheme(Theme): 
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

        self.round_time = 0

        # Background variables
        self.ui_scale = 2
        self.beavel_thickness = 3
        self.beavel = self.beavel_thickness * self.ui_scale
        self.border = 6 * self.ui_scale


        # self.menu_bar_height = 18 * self.ui_scale
        self.menu_bar_height = 0
        self.info_beavel_thickness = 2
        self.info_beavel = self.info_beavel_thickness * self.ui_scale
        self.digit_beavel_thickness = 1
        self.digit_beavel = self.digit_beavel_thickness * self.ui_scale
        self.digit_width = 13 * self.ui_scale
        self.digit_height = 23 * self.ui_scale
        self.info_height = (2 * 4) * self.ui_scale + self.info_beavel + self.digit_height  # (4 + 1 + 23 + 1 + 4)

        self.tile_size = 16 * self.ui_scale

        self.screen_width = 2 * self.border + 4 * self.beavel + self.tile_size * self.columns
        self.screen_height = self.menu_bar_height + 3 * self.border + 4 * self.beavel + 2 * self.info_beavel + self.info_height + self.tile_size * self.rows

        self.board_topleft = (self.beavel + self.border + self.beavel,
                              self.menu_bar_height + 2 * self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height)
        self.digits_bomb_topleft = (self.beavel + 2  * self.border + self.info_beavel + self.digit_beavel,
                                    self.menu_bar_height + self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + self.digit_beavel)
        self.digits_time_topleft = (self.screen_width - self.beavel - 2 * self.border - self.info_beavel - 2 * self.digit_beavel - 3 * self.digit_width,
                                    self.menu_bar_height + self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + self.digit_beavel)
        self.face_button_midtop = (self.screen_width / 2,
                                   self.menu_bar_height + self.beavel + self.border + self.info_beavel + 4 * self.ui_scale)


# =========================================================
    # region ASSET LOADERS
# =========================================================

    def load_screen(self, screen: pygame.surface.Surface) -> None:
        self.screen = screen

    def load_style_assets(self, style: str) -> None:

        style_path = f"view/classic/{style}.json"
        with open(f'{style_path}', 'r') as style_json:
            self.style_config = json.load(style_json, )
            style_json.close

        # Background color variables
        self.highlight_color = tuple(self.style_config['colors']['highlight'])
        self.neutral_color = tuple(self.style_config['colors']['neutral'])
        self.shadow_color = tuple(self.style_config['colors']['shadow'])

        tile_path = self.style_config['paths']['tile']
        digit_path = self.style_config['paths']['digit']
        face_path = self.style_config['paths']['face']
        sound_path = self.style_config['paths']['sound']

        tile_names = ['closed_blank', 'closed_flagged', 'closed_question', 'open_bomb', 'open_bomb_red', 'open_bomb_missflagged',
                      'open_0', 'open_1', 'open_2', 'open_3', 'open_4', 'open_5', 'open_6', 'open_7', 'open_8']
        face_names = ['facesmile', 'opensmile', 'faceooh', 'facewin', 'facedead']
        digit_names = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        sound_names = ['tick', 'win', 'lose']

        self.tile_surf: dict[str: pygame.surface.Surface] = {}
        for name in tile_names:
            self.tile_surf[name] = pygame.transform.scale_by(pygame.image.load(f'{tile_path}/{name}.png').convert(), self.ui_scale)

        self.face_surf: dict[str: pygame.surface.Surface] = {}
        for name in face_names:
            self.face_surf[name] = pygame.transform.scale_by(pygame.image.load(f'{face_path}/{name}.png').convert(), self.ui_scale)

        self.digit_surf: dict[str: pygame.surface.Surface] = {}
        for name in digit_names:
            self.digit_surf[name] = pygame.transform.scale_by(pygame.image.load(f'{digit_path}/{name}.png').convert(), self.ui_scale)

        self.sounds: dict[str: pygame.mixer.Sound] = {}
        for name in sound_names:
            self.sounds[name] = pygame.mixer.Sound(f'{sound_path}/{name}.mp3')

        self.sounds['tick'].set_volume(0.05)
        self.sounds['win'].set_volume(0.1)
        self.sounds['lose'].set_volume(0.1)

    # endregion


# =========================================================
    # region SOUND PLAYERS
# =========================================================

    def play_start_sound(self) -> None:
        pass


    def play_tick_sound(self) -> None:
        self.sounds['tick'].play()


    def play_win_sound(self) -> None:
        self.sounds['win'].play()


    def play_lose_sound(self) -> None:
        self.sounds['lose'].play()

    # endregion


# =========================================================
    # region BACKGROUND
# =========================================================

    def draw_background(self) -> None:
        self.construct_background()
        self.screen.blit(self.background, (0, 0))


    def construct_background(self) -> None:

        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(self.neutral_color)

        # Border around the screen
        topleft = (0, self.menu_bar_height)
        bottomright = (self.screen_width, self.screen_height)
        self.draw_bevaled_border(self.background, topleft, bottomright, self.beavel_thickness, 'outset')

        # Border around info bar
        topleft = (self.beavel + self.border,
                   self.menu_bar_height + self.beavel + self.border)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.menu_bar_height + self.beavel + self.border + 2 * self.info_beavel + self.info_height)
        self.draw_bevaled_border(self.background, topleft, bottomright, self.info_beavel_thickness, 'inset')

        # Border around tile board
        topleft = (self.beavel + self.border,
                   self.menu_bar_height + self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.screen_height - self.beavel - self.border)
        self.draw_bevaled_border(self.background, topleft, bottomright, self.beavel_thickness, 'inset')

        # Border around bomb counter
        topleft = (self.digits_bomb_topleft[0] - self.digit_beavel,
                   self.digits_bomb_topleft[1] - self.digit_beavel)
        bottomright = (topleft[0] + 3 * self.digit_width + 2 * self.digit_beavel,
                       topleft[1] + 2 * self.digit_beavel + self.digit_height)
        self.draw_bevaled_border(self.background, topleft, bottomright, self.digit_beavel_thickness, 'inset')

        # Border around timer
        topleft = (self.digits_time_topleft[0] - self.digit_beavel,
                   self.digits_time_topleft[1] - self.digit_beavel)
        bottomright = (topleft[0] + 3 * self.digit_width + 2 * self.digit_beavel,
                       topleft[1] + 2 * self.digit_beavel + self.digit_height)
        self.draw_bevaled_border(self.background, topleft, bottomright, self.digit_beavel_thickness, 'inset')

 
    def draw_bevaled_border(self, screen: pygame.surface.Surface, topleft: tuple[int, int], bottomright: tuple[int, int], bevel_thickness: int, type: str) -> None:
        if type == 'outset': color = (self.highlight_color, self.shadow_color)
        if type == 'inset': color = (self.shadow_color, self.highlight_color)
        
        for i in range(bevel_thickness):
            topleft_point = (topleft[0] + i * self.ui_scale, topleft[1] + i * self.ui_scale)
            pygame.draw.line(screen, color[0], (topleft_point[0], topleft_point[1]), (topleft_point[0], bottomright[1] - (i + 1) * self.ui_scale - self.ui_scale / 2), self.ui_scale)
            pygame.draw.line(screen, color[0], (topleft_point[0], topleft_point[1]), (bottomright[0] - (i + 1) * self.ui_scale - self.ui_scale / 2, topleft_point[1]), self.ui_scale)

            bottomright_point = (bottomright[0] - (i + 1) * self.ui_scale, bottomright[1] - (i + 1) * self.ui_scale)
            pygame.draw.line(screen, color[1], (bottomright_point[0], bottomright_point[1] + self.ui_scale / 2), (bottomright_point[0], topleft[1] + (i + 1) * self.ui_scale), self.ui_scale)
            pygame.draw.line(screen, color[1], (bottomright_point[0] + self.ui_scale / 2, bottomright_point[1]), (topleft[0] + (i + 1) * self.ui_scale, bottomright_point[1]), self.ui_scale)


        # thickness = bevel_thickness * self.ui_scale
        # points = {'topleft': (topleft[0], topleft[1]),
        #           'inner_topleft': (topleft[0] + thickness, topleft[1] + thickness),
        #           'topright': (bottomright[0], topleft[1]),
        #           'inner_topright': (bottomright[0] - thickness, topleft[1] + thickness),
        #           'bottomright': (bottomright[0], bottomright[1]),
        #           'inner_bottomright': (bottomright[0] - thickness, bottomright[1] - thickness),
        #           'bottomleft': (topleft[0], bottomright[1]), 
        #           'inner_bottomleft': (topleft[0] + thickness, bottomright[1] - thickness)}
        
        # first_bevel_points = [points['topleft'], points['bottomleft']]
        # second_bevel_points = [points['bottomright'], points['topright']]

        # for i in range(bevel_thickness):
        #     point = (first_bevel_points[-1][0], first_bevel_points[-1][1] - self.ui_scale)
        #     first_bevel_points.append(point)
        #     point = (first_bevel_points[-1][0] + self.ui_scale, first_bevel_points[-1][1])
        #     first_bevel_points.append(point)

        #     point = (second_bevel_points[-1][0], second_bevel_points[-1][1] + self.ui_scale)
        #     second_bevel_points.append(point)
        #     point = (second_bevel_points[-1][0] - self.ui_scale, second_bevel_points[-1][1])
        #     second_bevel_points.append(point)

        # first_bevel_points.append(points['inner_topleft'])
        # first_bevel_points.append(points['inner_topright'])
        # second_bevel_points.append(points['inner_bottomright'])
        # second_bevel_points.append(points['inner_bottomleft'])

        # for i in range(bevel_thickness):
        #     point = (first_bevel_points[-1][0], first_bevel_points[-1][1] - self.ui_scale)
        #     first_bevel_points.append(point)
        #     point = (first_bevel_points[-1][0] + self.ui_scale, first_bevel_points[-1][1])
        #     first_bevel_points.append(point)

        #     point = (second_bevel_points[-1][0], second_bevel_points[-1][1] + self.ui_scale)
        #     second_bevel_points.append(point)
        #     point = (second_bevel_points[-1][0] - self.ui_scale, second_bevel_points[-1][1])
        #     second_bevel_points.append(point)

        # first_bevel_points.pop(1)
        # first_bevel_points.pop(-1)
        # second_bevel_points.pop(1)
        # second_bevel_points.pop(-1)

        # print(f"1st: {first_bevel_points}")
        # print(f"2nd: {second_bevel_points}")
        # pygame.gfxdraw.filled_polygon(screen, first_bevel_points, color[0])
        # pygame.gfxdraw.filled_polygon(screen, second_bevel_points, color[1])

        # pygame.draw.polygon(screen, color[0], [points['topleft'],
        #                                             points['bottomleft'],
        #                                             points['inner_bottomleft'],
        #                                             points['inner_topleft'],
        #                                             points['inner_topright'],
        #                                             points['topright']])
        # pygame.draw.polygon(screen, color[1], [points['bottomright'],
        #                                             points['topright'],
        #                                             points['inner_topright'],
        #                                             points['inner_bottomright'],
        #                                             points['inner_bottomleft'],
        #                                             points['bottomleft']])
        # del points

# endregion


# =========================================================
    # region DATA GETTERS
# =========================================================

    def get_screen_size(self) -> tuple[int, int]:
        return (self.screen_width, self.screen_height)


    def get_tile_images(self) -> dict[str: pygame.surface.Surface]:
        return self.tile_surf
    

    def get_board_topleft(self) -> tuple[int, int]:
        return self.board_topleft
    

    def get_tile_size(self) -> int:
        return self.tile_size

    # endregion


# =========================================================
    # region INFO SPRITES
# =========================================================

    def build_info_sprites(self):
        self.mines_couter = ThreeDigitDisplay(self.digit_surf, self.digits_bomb_topleft)
        self.timer = ThreeDigitDisplay(self.digit_surf, self.digits_time_topleft)
        self.face = SmileFace(self.face_surf, self.face_button_midtop)


    def update_mines_couter(self, number: int) -> None:
        self.mines_couter.update(number)
        self.mines_couter.draw(self.screen)


    def update_timer(self, number: int) -> None:
        self.timer.update(number)
        self.timer.draw(self.screen)


    def update_face_sprite(self, state: str) -> None:
        self.face.update(state)
        self.screen.blit(self.face.image, self.face.rect)


    def get_face_sprite(self) -> pygame.sprite.Sprite:
        return self.face

    # endregion
