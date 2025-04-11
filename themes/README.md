# Theme System — Minesweeper Game

This folder contains the **visual themes** used in the game.

Each theme is a separate Python class that defines:
- The look of the game board
- Custom user interface components (mine counter, timer, face button)
- The visual layout (background, bevels, borders)
- Sounds for win, lose, and tick events

Themes allow complete customization of the game's appearance and feel.

---

<br><br><br>

## How Themes Work

Every theme is a Python class that inherits from the abstract base class `Theme` (defined in `base_theme.py`).  
This class defines the full interface a theme must implement.

A theme class handles:
- Drawing the game background
- Providing images for tiles
- Managing UI elements like the counter, timer, and face button
- Playing optional sounds

---

<br><br><br>

## Folder Structure

```bash
themes/
├── sprites/                # Shared UI sprite components (Digit, Face, etc.)
├── base_theme.py           # Abstract base class for all themes
├── classic_theme.py        # Example complete theme of classic minesweeper look
├── aero.py                 # Another example of theme for aero minesweeper look
└── my_custom_theme.py           # Your custom theme
```

Each theme is a **Python file with a class**, e.g. `ClassicTheme`, `AeroTheme`, etc.

---

<br><br><br>

## Required Methods

Each theme must implement all methods defined in `Theme`. These include:

| Method                       | Purpose                                                |
|------------------------------|--------------------------------------------------------|
| `load_screen(screen)`        | Store screen reference for drawing                     |
| `load_style_assets(style)`   | Load assets (images, sounds, etc.)                     |
| `draw_background()`          | Blit background to the screen                          |
| `get_screen_size()`          | Return width and height of the screen                  |
| `get_tile_images()`          | Return tile graphics as a dictionary                   |
| `get_board_topleft()`        | Return top-left position for tile grid                 |
| `get_tile_size()`            | Return pixel size of a single tile                     |
| `build_info_sprites()`       | Create mine counter, timer, face button                |
| `update_mines_couter(num)`   | Update mine counter display                            |
| `update_timer(num)`          | Update timer display                                   |
| `update_face_sprite(state)`  | Change face image (e.g., smile, dead, win)             |
| `get_face_sprite()`          | Return the face sprite for mouse interaction           |
| `play_tick_sound()`          | Play ticking sound (optional)                          |
| `play_win_sound()`           | Play win sound (optional)                              |
| `play_lose_sound()`          | Play lose sound (optional)                             |
| `play_start_sound()`         | Play start sound (optional)                            |

> **Note**: If your theme does not use a specific UI element (e.g., no face button or no sounds), your methods can return `None` or do nothing.

---

<br><br><br>

## Creating Your Own Theme

To build a new theme:

1. Create a new file, e.g. `themes/my_custom_theme.py`
2. Create a class `MyCustomTheme` that inherits from `Theme`
3. Implement all required methods
4. Use your own images, colors, and sounds
5. In your game setup, load the theme:

---

<br><br><br>

## Sprite Components

You can reuse ready-made UI elements from themes/sprites/:
- ThreeDigitDisplay — counter for mines or timer
- SmileFace — face button
- Digit — individual number sprite

You are also free to design your own.

---

<br><br><br>

## Design Goals
- Full control over visuals and layout
- Optional support for sounds
- Easy to create and test standalone themes
- No assumptions about color, style, or assets