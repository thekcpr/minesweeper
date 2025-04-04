import pygame

# TODO:
# - Create Theme class


class ViewTheme():
    def __init__(self): pass
    def load_assets(self): pass

    def play_new_game_sound(self): pass
    def play_first_tick_sound(self): pass
    def play_time_tick_sound(self): pass
    def play_win_sound(self): pass
    def play_fail_sound(self): pass

    def draw_background(self): pass

    # Getters
    def get_screen(self): pass
    def get_tile_images(self): pass
    def get_board_topleft(slef): pass
    def get_tile_size(self): pass
    def get_face_images(self): pass
    def get_face_button_midtop(self): pass

class WinXP(ViewTheme): 
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

        self.round_time = 0

        # Background variables
        self.ui_scale = 2
        self.beavel = 3 * self.ui_scale
        self.border = 6 * self.ui_scale


        # self.menu_bar_height = 18 * self.ui_scale
        self.menu_bar_height = 0
        self.info_beavel = 2 * self.ui_scale
        self.digit_beavel = 1 * self.ui_scale
        self.digit_width = 13 * self.ui_scale
        self.digit_height = 23 * self.ui_scale
        self.info_height = (2 * 4) * self.ui_scale + self.info_beavel + self.digit_height  # (4 + 1 + 23 + 1 + 4)

        self.tile_size = 16 * self.ui_scale

        self.screen_width = 2 * self.border + 4 * self.beavel + self.tile_size * self.columns + 1
        self.screen_height = self.menu_bar_height + 3 * self.border + 4 * self.beavel + 2 * self.info_beavel + self.info_height + self.tile_size * self.rows + 1

        self.board_topleft = (2 * self.beavel + self.border + 1,
                              self.menu_bar_height + 2 * self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height + 1)
        self.digits_bomb_topleft = (self.beavel + 2  * self.border + self.info_beavel + self.digit_beavel,
                                    self.menu_bar_height + self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + self.digit_beavel)
        self.digits_time_topleft = (self.screen_width - self.beavel - 2 * self.border - self.info_beavel - 2 * self.digit_beavel - 3 * self.digit_width,
                                    self.menu_bar_height + self.beavel + self.border + self.info_beavel + 4 * self.ui_scale + self.digit_beavel)
        self.face_button_midtop = (self.screen_width / 2,
                                   self.menu_bar_height + self.beavel + self.border + self.info_beavel + 4 * self.ui_scale)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.load_assets()
        self.draw_background()

        # Draws info bar content
        self.face = SmileFace(self.face_images, self.face_button_midtop)
        self.face.draw(self.screen)

        self.info_bomb = []
        self.info_time = []

        for i in range(0, 3):
            self.info_bomb.append(Digit(i, self.digit_images, self.digits_bomb_topleft, self.digit_width))
            self.info_time.append(Digit(i, self.digit_images, self.digits_time_topleft, self.digit_width))
            self.info_bomb[i].draw(self.screen)
            self.info_time[i].draw(self.screen)


    def load_assets(self) -> None:

        # Background color variables
        self.WHITE = (255, 255, 255)
        self.LIGHT_GREY = (192, 192, 192)
        self.DARK_GREY = (128, 128, 128)

        tile_path = 'themes/classic/winxp/images/tile'
        digit_path = 'themes/classic/winxp/images/digit'
        face_path = 'themes/classic/winxp/images/face'
        sound_path = 'themes/classic/winxp/sounds'

        self.tile_images = {'closed_blank': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_blank.png').convert(), self.ui_scale),
                            'closed_flagged': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_flagged.png').convert(), self.ui_scale),
                            'closed_question': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_question.png').convert(), self.ui_scale),
                            'open_bomb': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb.png').convert(), self.ui_scale),
                            'open_bomb_red': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb_red.png').convert(), self.ui_scale),
                            'open_bomb_missflagged': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb_missflagged.png').convert(), self.ui_scale),
                            'open_0': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open0.png').convert(), self.ui_scale),
                            'open_1': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open1.png').convert(), self.ui_scale),
                            'open_2': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open2.png').convert(), self.ui_scale),
                            'open_3': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open3.png').convert(), self.ui_scale),
                            'open_4': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open4.png').convert(), self.ui_scale),
                            'open_5': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open5.png').convert(), self.ui_scale),
                            'open_6': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open6.png').convert(), self.ui_scale),
                            'open_7': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open7.png').convert(), self.ui_scale),
                            'open_8': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open8.png').convert(), self.ui_scale)}

        self.digit_images = {'-': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/-.png').convert(), self.ui_scale),
                             '0': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/0.png').convert(), self.ui_scale),
                             '1': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/1.png').convert(), self.ui_scale),
                             '2': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/2.png').convert(), self.ui_scale),
                             '3': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/3.png').convert(), self.ui_scale),
                             '4': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/4.png').convert(), self.ui_scale),
                             '5': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/5.png').convert(), self.ui_scale),
                             '6': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/6.png').convert(), self.ui_scale),
                             '7': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/7.png').convert(), self.ui_scale),
                             '8': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/8.png').convert(), self.ui_scale),
                             '9': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/9.png').convert(), self.ui_scale)}

        self.face_images = {'facesmile': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facesmile.png').convert(), self.ui_scale),
                            'opensmile': pygame.transform.scale_by(pygame.image.load(f'{face_path}/opensmile.png').convert(), self.ui_scale),
                            'faceooh': pygame.transform.scale_by(pygame.image.load(f'{face_path}/faceooh.png').convert(), self.ui_scale),
                            'facewin': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facewin.png').convert(), self.ui_scale),
                            'facedead': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facedead.png').convert(), self.ui_scale)}

        self.menu_icons = {'beginner_active': pygame. transform.scale_by(pygame.image.load('images/menu/beginner_active.png').convert(), self.ui_scale),
                           'beginner_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/beginner_inactive.png').convert(), self.ui_scale),
                           'intermediate_active': pygame. transform.scale_by(pygame.image.load('images/menu/intermediate_active.png').convert(), self.ui_scale),
                           'intermediate_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/intermediate_inactive.png').convert(), self.ui_scale),
                           'expert_active': pygame. transform.scale_by(pygame.image.load('images/menu/expert_active.png').convert(), self.ui_scale),
                           'expert_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/expert_inactive.png').convert(), self.ui_scale),
                           'custom_active': pygame. transform.scale_by(pygame.image.load('images/menu/custom_active.png').convert(), self.ui_scale),
                           'custom_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/custom_inactive.png').convert(), self.ui_scale)}

        self.tick_sound = pygame.mixer.Sound(f'{sound_path}/windows_xp_tick.mp3')
        self.win_sound = pygame.mixer.Sound(f'{sound_path}/windows_xp_win.mp3')
        self.lose_sound = pygame.mixer.Sound(f'{sound_path}/windows_xp_lose.mp3')


    def play_tick_sound(self) -> None:
        self.tick_sound.play()

    def play_win_sound(self) -> None:
        self.win_sound.play()

    def play_lose_sound(self) -> None:
        self.lose_sound.play()


    def draw_background(self) -> None:
        self.screen.fill(self.LIGHT_GREY)

        # Menu bar
        # pygame.draw.rect(self.screen, 'White', [(0, 0), (self.screen_width, self.menu_bar_height - 1)])

        # Border around the screen
        topleft = (0, self.menu_bar_height)
        bottomright = (self.screen_width, self.screen_height)
        self.draw_bevaled_border(topleft, bottomright, self.beavel, 'outset')

        # Border around info bar
        topleft = (self.beavel + self.border,
                   self.menu_bar_height + self.beavel + self.border)
        bottomright = (self.screen_width - self.beavel - self.border,
                       self.menu_bar_height + self.beavel + self.border + 2 * self.info_beavel + self.info_height)
        self.draw_bevaled_border(topleft, bottomright, self.info_beavel, 'inset')

        # Border around tile board
        topleft = (self.beavel + self.border,
                   self.menu_bar_height + self.beavel + 2 * self.border + 2 * self.info_beavel + self.info_height)
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
        if type == 'outset': color = (self.WHITE, self.DARK_GREY)
        if type == 'inset': color = (self.DARK_GREY, self.WHITE)
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


    def get_screen(self) -> pygame.surface.Surface:
        return self.screen


    def get_tile_images(self) -> dict[str: pygame.surface.Surface]:
        return self.tile_images
    
    def get_board_topleft(self) -> tuple[int, int]:
        return self.board_topleft
    
    def get_tile_size(self) -> int:
        return self.tile_size


    def get_face_images(self) -> dict[str: pygame.surface.Surface]:
        return self.face_images

    def get_face_button_midtop(self) -> tuple[int, int]:
        return self.face_button_midtop


    def update_bomb_digits(self, number: int) -> None:
        bombs_left = str(number).zfill(3)
        self.info_bomb[0].update(bombs_left[-3])
        self.info_bomb[1].update(bombs_left[-2])
        self.info_bomb[2].update(bombs_left[-1])
        self.info_bomb[0].draw(self.screen)
        self.info_bomb[1].draw(self.screen)
        self.info_bomb[2].draw(self.screen)
    
    def update_time_digits(self, number: int) -> None:
        time_elapsed = str(number).zfill(6)
        self.info_time[0].update(time_elapsed[-6])
        self.info_time[1].update(time_elapsed[-5])
        self.info_time[2].update(time_elapsed[-4])
        self.info_time[0].draw(self.screen)
        self.info_time[1].draw(self.screen)
        self.info_time[2].draw(self.screen)

    def update_restart_button(self, state: str) -> None:
        self.face.update(state)
        self.face.draw(self.screen)


class Win31(WinXP):

    def load_assets(self) -> None:

        # Background color variables
        self.WHITE = (255, 255, 255)
        self.LIGHT_GREY = (193, 196, 199)
        self.DARK_GREY = (133, 136, 139)

        tile_path = 'themes/classic/win31/images/tile'
        digit_path = 'themes/classic/win31/images/digit'
        face_path = 'themes/classic/win31/images/face'
        sound_path = 'themes/classic/win31/sounds'

        self.tile_images = {'closed_blank': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_blank.png').convert(), self.ui_scale),
                            'closed_flagged': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_flagged.png').convert(), self.ui_scale),
                            'closed_question': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_question.png').convert(), self.ui_scale),
                            'open_bomb': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb.png').convert(), self.ui_scale),
                            'open_bomb_red': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb_red.png').convert(), self.ui_scale),
                            'open_bomb_missflagged': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb_missflagged.png').convert(), self.ui_scale),
                            'open_0': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open0.png').convert(), self.ui_scale),
                            'open_1': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open1.png').convert(), self.ui_scale),
                            'open_2': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open2.png').convert(), self.ui_scale),
                            'open_3': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open3.png').convert(), self.ui_scale),
                            'open_4': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open4.png').convert(), self.ui_scale),
                            'open_5': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open5.png').convert(), self.ui_scale),
                            'open_6': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open6.png').convert(), self.ui_scale),
                            'open_7': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open7.png').convert(), self.ui_scale),
                            'open_8': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open8.png').convert(), self.ui_scale)}

        self.digit_images = {'-': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/-.png').convert(), self.ui_scale),
                             '0': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/0.png').convert(), self.ui_scale),
                             '1': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/1.png').convert(), self.ui_scale),
                             '2': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/2.png').convert(), self.ui_scale),
                             '3': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/3.png').convert(), self.ui_scale),
                             '4': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/4.png').convert(), self.ui_scale),
                             '5': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/5.png').convert(), self.ui_scale),
                             '6': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/6.png').convert(), self.ui_scale),
                             '7': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/7.png').convert(), self.ui_scale),
                             '8': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/8.png').convert(), self.ui_scale),
                             '9': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/9.png').convert(), self.ui_scale)}

        self.face_images = {'facesmile': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facesmile.png').convert(), self.ui_scale),
                            'opensmile': pygame.transform.scale_by(pygame.image.load(f'{face_path}/opensmile.png').convert(), self.ui_scale),
                            'faceooh': pygame.transform.scale_by(pygame.image.load(f'{face_path}/faceooh.png').convert(), self.ui_scale),
                            'facewin': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facewin.png').convert(), self.ui_scale),
                            'facedead': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facedead.png').convert(), self.ui_scale)}

        self.menu_icons = {'beginner_active': pygame. transform.scale_by(pygame.image.load('images/menu/beginner_active.png').convert(), self.ui_scale),
                           'beginner_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/beginner_inactive.png').convert(), self.ui_scale),
                           'intermediate_active': pygame. transform.scale_by(pygame.image.load('images/menu/intermediate_active.png').convert(), self.ui_scale),
                           'intermediate_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/intermediate_inactive.png').convert(), self.ui_scale),
                           'expert_active': pygame. transform.scale_by(pygame.image.load('images/menu/expert_active.png').convert(), self.ui_scale),
                           'expert_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/expert_inactive.png').convert(), self.ui_scale),
                           'custom_active': pygame. transform.scale_by(pygame.image.load('images/menu/custom_active.png').convert(), self.ui_scale),
                           'custom_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/custom_inactive.png').convert(), self.ui_scale)}

        self.tick_sound = pygame.mixer.Sound(f'{sound_path}/windows_3_1_tick.mp3')
        self.win_sound = pygame.mixer.Sound(f'{sound_path}/windows_3_1_win.mp3')
        self.lose_sound = pygame.mixer.Sound(f'{sound_path}/windows_3_1_lose.mp3')


class Win95(WinXP):

    def load_assets(self) -> None:

        # Background color variables
        self.WHITE = (255, 255, 255)
        self.LIGHT_GREY = (192, 192, 192)
        self.DARK_GREY = (128, 128, 128)

        tile_path = 'themes/classic/win95/images/tile'
        digit_path = 'themes/classic/winxp/images/digit'
        face_path = 'themes/classic/win95/images/face'
        sound_path = 'themes/classic/win31/sounds'

        self.tile_images = {'closed_blank': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_blank.png').convert(), self.ui_scale),
                            'closed_flagged': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_flagged.png').convert(), self.ui_scale),
                            'closed_question': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/closed_question.png').convert(), self.ui_scale),
                            'open_bomb': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb.png').convert(), self.ui_scale),
                            'open_bomb_red': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb_red.png').convert(), self.ui_scale),
                            'open_bomb_missflagged': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open_bomb_missflagged.png').convert(), self.ui_scale),
                            'open_0': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open0.png').convert(), self.ui_scale),
                            'open_1': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open1.png').convert(), self.ui_scale),
                            'open_2': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open2.png').convert(), self.ui_scale),
                            'open_3': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open3.png').convert(), self.ui_scale),
                            'open_4': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open4.png').convert(), self.ui_scale),
                            'open_5': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open5.png').convert(), self.ui_scale),
                            'open_6': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open6.png').convert(), self.ui_scale),
                            'open_7': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open7.png').convert(), self.ui_scale),
                            'open_8': pygame.transform.scale_by(pygame.image.load(f'{tile_path}/open8.png').convert(), self.ui_scale)}

        self.digit_images = {'-': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/-.png').convert(), self.ui_scale),
                             '0': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/0.png').convert(), self.ui_scale),
                             '1': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/1.png').convert(), self.ui_scale),
                             '2': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/2.png').convert(), self.ui_scale),
                             '3': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/3.png').convert(), self.ui_scale),
                             '4': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/4.png').convert(), self.ui_scale),
                             '5': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/5.png').convert(), self.ui_scale),
                             '6': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/6.png').convert(), self.ui_scale),
                             '7': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/7.png').convert(), self.ui_scale),
                             '8': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/8.png').convert(), self.ui_scale),
                             '9': pygame.transform.scale_by(pygame.image.load(f'{digit_path}/9.png').convert(), self.ui_scale)}

        self.face_images = {'facesmile': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facesmile.png').convert(), self.ui_scale),
                            'opensmile': pygame.transform.scale_by(pygame.image.load(f'{face_path}/opensmile.png').convert(), self.ui_scale),
                            'faceooh': pygame.transform.scale_by(pygame.image.load(f'{face_path}/faceooh.png').convert(), self.ui_scale),
                            'facewin': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facewin.png').convert(), self.ui_scale),
                            'facedead': pygame.transform.scale_by(pygame.image.load(f'{face_path}/facedead.png').convert(), self.ui_scale)}

        self.menu_icons = {'beginner_active': pygame. transform.scale_by(pygame.image.load('images/menu/beginner_active.png').convert(), self.ui_scale),
                           'beginner_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/beginner_inactive.png').convert(), self.ui_scale),
                           'intermediate_active': pygame. transform.scale_by(pygame.image.load('images/menu/intermediate_active.png').convert(), self.ui_scale),
                           'intermediate_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/intermediate_inactive.png').convert(), self.ui_scale),
                           'expert_active': pygame. transform.scale_by(pygame.image.load('images/menu/expert_active.png').convert(), self.ui_scale),
                           'expert_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/expert_inactive.png').convert(), self.ui_scale),
                           'custom_active': pygame. transform.scale_by(pygame.image.load('images/menu/custom_active.png').convert(), self.ui_scale),
                           'custom_inactive': pygame. transform.scale_by(pygame.image.load('images/menu/custom_inactive.png').convert(), self.ui_scale)}

        # self.tick_sound = pygame.mixer.Sound(f'{sound_path}/windows_3_1_tick.mp3')
        # self.win_sound = pygame.mixer.Sound(f'{sound_path}/windows_3_1_win.mp3')
        # self.lose_sound = pygame.mixer.Sound(f'{sound_path}/windows_3_1_lose.mp3')


    def play_tick_sound(self) -> None: pass

    def play_win_sound(self) -> None: pass

    def play_lose_sound(self) -> None: pass

class Tile(pygame.sprite.Group):
    def __init__(self, grid_pos: tuple[int, int], images: dict[str: pygame.surface.Surface], screen_topleft: tuple[int, int], spacing: int):
        super().__init__()

        self.images = images  # 'closed_blank', 'closed_flag', 'closed_question', 'open_bomb', 'open_bomb_red', 'open_bomb_missflagged'
                              # 'open_0', 'open_1', 'open_2', 'open_3', 'open_4', 'open_5', 'open_6', 'open_7', 'open_8'
        self.image = self.images['closed_blank']
        x = screen_topleft[0] + spacing * grid_pos[0]
        y = screen_topleft[1] + spacing * grid_pos[1]
        self.tile_rect = self.image.get_rect(topleft = (x, y))


    def update(self, state: str, content: str) -> None:
        self.state = state  # 'closed', 'open', 'flagged', 'question', 'hover'
        if self.state == 'hover': self.image = self.images['open_0']
        if self.state == 'closed': self.image = self.images['closed_blank']
        if self.state == 'missflagged': self.image = self.images['open_bomb_missflagged']
        if self.state == 'flagged': self.image = self.images['closed_flagged']
        if self.state == 'question': self.image = self.images['closed_question']
        if self.state == 'open': self.image = self.images[content]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.tile_rect)

class Digit(pygame.sprite.Group):
    def __init__(self, grid_pos: int, images: dict[str: pygame.surface.Surface], screen_topleft: tuple[int, int], spacing: int):
        super().__init__()

        self.images = images  # '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        self.image = self.images['0']
        x = screen_topleft[0] + spacing * grid_pos
        y = screen_topleft[1]
        self.digit_rect = self.image.get_rect(topleft = (x, y))
    

    def update(self, content: str) -> None:
        self.image = self.images[content]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.digit_rect)

class SmileFace(pygame.sprite.Sprite):
    def __init__(self, images: dict[str: pygame.surface.Surface], screen_midtop: int):
        super().__init__()

        self.images = images  # 'facesmile', 'opensmile', 'faceooh', 'facewin', 'facedead'
        self.image = self.images['facesmile']
        self.smile_rect = self.image.get_rect(midtop = (screen_midtop))


    def update(self, state: str):
        self.image = self.images[state]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.smile_rect)


    def get_rect(self) -> pygame.rect.Rect:
        return self.smile_rect

class MenuIcon(pygame.sprite.Group):
    def __init__(self, type: str, state: str, grid_pos: int, images: dict[str: pygame.surface.Surface], screen_midleft: tuple[int, int], spacing: int):
        super().__init__()

        self.type = type
        self.images = images  # 'beginner_active', 'beginner_inactive', 'intermediate_active', 'intermediate_inactive', 'expert_active', 'expert_inactive', 'custom_active', 'custom_inactive'
        self.image = self.images[f'{self.type}_{state}']
        x = screen_midleft[0] + spacing * grid_pos
        y = screen_midleft[1]
        self.icon_rect = self.image.get_rect(midleft = (x, y))


    def update(self, state: str) -> None:
        self.image = self.images[f'{self.type}_{state}']


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.icon_rect)


    def get_rect(self) -> pygame.rect.Rect:
        return self.icon_rect
