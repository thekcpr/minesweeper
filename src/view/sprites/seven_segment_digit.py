import pygame


class Digit(pygame.sprite.Sprite):
    def __init__(self, images: dict[str: pygame.surface.Surface], position_topleft: tuple[int, int]):
        super().__init__()

        self.images = images  # '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        self.image = self.images['0']
        self.digit_rect = self.image.get_rect(topleft = (position_topleft))
    

    def update(self, content: str) -> None:
        self.image = self.images[content]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.digit_rect)
