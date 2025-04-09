import pygame


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
        self.state = state  # 'closed', 'flagged', 'missflagged', 'question', 'open'
        if self.state == 'hover': self.image = self.images['open_0']
        if self.state == 'closed': self.image = self.images['closed_blank']
        if self.state == 'flagged': self.image = self.images['closed_flagged']
        if self.state == 'missflagged': self.image = self.images['open_bomb_missflagged']
        if self.state == 'question': self.image = self.images['closed_question']
        if self.state == 'open': self.image = self.images[content]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.tile_rect)
