import pygame

from .seven_segment_digit import Digit

class ThreeDigitDisplay(pygame.sprite.Group):
    def __init__(self, images: dict[str: pygame.surface.Surface], position_topleft: tuple[int, int]):
        super().__init__()
        self.images = images
        self.position_topleft = position_topleft
        spacing = self.images['0'].get_width()
        digits = []

        for i in range(0, 3):
            x = self.position_topleft[0] + i * spacing
            y = self.position_topleft[1]
            digit = Digit(self.images, (x, y))
            digits.append(digit)
            self.add(digit)

        self.digits = digits

    def update(self, number) -> None:
        number = str(number).rjust(3, "0")[-3:]
        for digit, char in zip(self.digits, number):
            digit.update(char)



class Digit(pygame.sprite.Sprite):
    def __init__(self, images: dict[str: pygame.surface.Surface], position_topleft: tuple[int, int]):
        super().__init__()

        self.images = images  # '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        self.image = self.images['0']
        self.rect = self.image.get_rect(topleft = position_topleft)
    

    def update(self, content: str) -> None:
        self.image = self.images[content]