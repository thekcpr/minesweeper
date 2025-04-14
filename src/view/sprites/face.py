import pygame

class SmileFace(pygame.sprite.Sprite):
    def __init__(self, images: dict[str: pygame.surface.Surface], screen_midtop: int):
        super().__init__()

        self.images = images  # 'facesmile', 'opensmile', 'faceooh', 'facewin', 'facedead'
        self.image = self.images['facesmile']
        self.rect = self.image.get_rect(midtop = (screen_midtop))

    def update(self, state: str) -> None:
        if state in self.images:
            self.image = self.images[state]
        else:
            raise ValueError(f"Unknown face state: {state}")