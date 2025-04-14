import pygame
from abc import ABC, abstractmethod
from typing import Optional

class Theme(ABC):
    """
    Abstract base class for all visual themes used in the game.

    This class defines the interface that all themes must implement, fully or partially.
    Some methods (like sound or face button) may return None or do nothing if
    the theme does not include those features.
    """

# =========================================================
    # region ASSET LOADERS
# =========================================================
    @abstractmethod
    def load_screen(self, screen: pygame.surface.Surface) -> None:
        """
        Stores the reference to the main screen surface for drawing.
        """
        pass

    @abstractmethod
    def load_style_assets(self, style: str) -> None:
        """
        Loads all visual and audio assets (images, sounds) based on the given style.

        Args:
            style (str): The name of the style variant (e.g., "mono", "win95").
        """
        pass

    # endregion


# =========================================================
    # region SOUND PLAYERS
# =========================================================
    @abstractmethod
    def play_start_sound(self) -> None:
        """
        Plays the game start sound, if used in the theme.
        """
        pass

    @abstractmethod
    def play_tick_sound(self) -> None:
        """
        Plays the ticking sound, typically used by the timer.
        """
        pass

    @abstractmethod
    def play_win_sound(self) -> None:
        """
        Plays the sound that indicates the player has won.
        """
        pass

    @abstractmethod
    def play_lose_sound(self) -> None:
        """
        Plays the sound that indicates the player has lost.
        """
        pass

    # endregion


# =========================================================
    # region BACKGROUND
# =========================================================
    @abstractmethod
    def draw_background(self) -> None:
        """
        Blits the pre-rendered background surface to the screen.

        This is called once per redraw or style change
        """
        pass

    # endregion


# =========================================================
    # region DATA GETTERS
# =========================================================
    @abstractmethod
    def get_screen_size(self) -> tuple[int, int]:
        """
        Returns the size of the game window (width, height).
        """
        pass

    @abstractmethod
    def get_tile_images(self) -> dict[str: pygame.surface.Surface]:
        """
        Returns a dictionary mapping tile state names to image surfaces.
        """
        pass

    @abstractmethod
    def get_board_topleft(self) -> tuple[int, int]:
        """
        Returns the top-left pixel position for the board (where tiles are drawn).
        """
        pass

    @abstractmethod
    def get_tile_size(self) -> int:
        """
        Returns the size (width and height) of a single tile in pixels.
        """
        pass

    # endregion


# =========================================================
    # region INFO SPRITES 
# =========================================================
    @abstractmethod
    def build_info_sprites(self):
        """
        Constructs and initializes the UI sprites used in the info bar,
        such as the mine counter, timer display, and face button.

        This method is called once during theme setup.
        If the theme does not include these components, this method can remain empty.
        """
        pass

    @abstractmethod
    def update_mines_couter(self, number: int) -> None:
        """
        Updates and renders the mine counter display.

        Args:
            number (int): The number of remaining mines to display.

        If the theme does not use a mines counter, this method may do nothing.
        """
        pass

    @abstractmethod
    def update_timer(self, number: int) -> None:
        """
        Updates and renders the game timer display.

        Args:
            number (int): The current time in seconds to display.

        If the theme does not use a timer, this method may do nothing.
        """
        pass

    @abstractmethod
    def update_face_sprite(self, state: str) -> None:
        """
        Updates and renders the face button sprite based on game state.

        Args:
            state (str): A string representing the desired face image,
                         such as 'facesmile', 'facewin', 'facedead'.

        If the theme does not include a face button, this method may do nothing.
        """
        pass

    @abstractmethod
    def get_face_sprite(self) -> Optional[pygame.sprite.Sprite]:
        """
        Returns the face button sprite for user interaction.

        Returns:
            pygame.sprite.Sprite or None: The face sprite, or None if not used.

        Used by the controller to detect user clicks on the face button.
        If the theme does not include a face button, return None.
        """
        pass

    # endregion
