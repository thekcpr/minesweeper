import pygame
from abc import ABC, abstractmethod

class Theme(ABC):
    # @abstractmethod
    def load_assets(self): pass


    # @abstractmethod
    def play_new_game_sound(self): pass


    # @abstractmethod
    def play_first_tick_sound(self): pass


    # @abstractmethod
    def play_time_tick_sound(self): pass


    # @abstractmethod
    def play_win_sound(self): pass


    # @abstractmethod
    def play_fail_sound(self): pass


    # @abstractmethod
    def construct_background(self): pass


    # Getters
    # @abstractmethod
    def get_screen(self): pass


    # @abstractmethod
    def get_tile_images(self): pass


    # @abstractmethod
    def get_board_topleft(self): pass


    # @abstractmethod
    def get_tile_size(self): pass


    # @abstractmethod
    def get_face_images(self): pass


    # @abstractmethod
    def get_face_button_midtop(self): pass
