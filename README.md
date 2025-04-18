# Classic Minesweeper in Pygame

<table>
  <tr>
    <td style="border: 0px">
      <img src="docs/images/icon.png" alt="Minesweeper Icon" width="256">
    </td>
    <td style="border: 0px">
<p>
  A faithful Python remake of the classic Minesweeper, rebuilt from scratch using
  <a href="https://www.pygame.org/news">Pygame</a>.
</p>
    </td>
  </tr>
</table>

  This project started as a personal challenge to learn how to structure larger programs in Python.<br>
  As a huge fan of Minesweeper, I wanted to create a version that's true to the original —
  fully playable and ad-free.

  The long-term goal is to build a modular, expandable Minesweeper engine with support for themes
  that replicate the look and feel of every major version — from classic styles like Windows 3.1 and XP,
  to the Aero theme seen in Windows Vista and 7.

---

<br><br><br>

# Gameplay Screenshots

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/theme_swap_beginner_dark.gif">
  <img alt="Minesweeper Themes" src="docs/images/theme_swap_beginner_light.gif">
</picture>

---

<br><br><br>

# Themes

This project aims to support visual styles that replicate the look and feel of two main design categories: **Classic** and **Aero**.

Available and planned themes include:

- **Classic**
  - [ ] PMMine
  - [ ] Mine 2.6 / 2.9
  - [x] Minesweeper for Windows 3.1
  - [x] Minesweeper for Windows 95 / 98 / ME
  - [x] Minesweeper for Windows 2000 / XP
  - [ ] Prato Fiorito for Windows 2000
  - [ ] Prato Fiorito for Windows XP
  - [ ] Prato Fiorito Monochrome
  - [x] Monochrome

- **Aero**
  - [ ] Windows Vista / 7 *(Blue and Green Tiles, Bombs and Flowers)*

---

<br><br><br>


# Keyboard Controls

- **Visual Style**  
  Switch between visual styles (Classic theme) at any time by pressing:
  - `1` – Windows 3.1 style
  - `2` – Windows 95 style
  - `3` – Windows XP style
  - `4` – Mono style

- **Game Difficulty**  
  Instantly start a new game with a selected difficulty by pressing:
  - `B` – Beginner (9×9, 10 Mines)  
  - `I` – Intermediate (16×16, 40 Mines)  
  - `E` – Expert (30×16, 99 Mines)

---

<br><br><br>

# Requirements


Make sure you have Python 3 installed, then install the required dependencies from `requirements.txt`. For example:

```bash
pip install -r requirements.txt
```

---

<br><br><br>

## TODO

- [ ] Implement proper face and tile animation when hovered over and when the mouse button is pressed
- [x] Implement an options menu with multiple difficulty levels (Beginner, Intermediate, Expert)
- [ ] Implement proper menu bar
- [ ] Implement a pop-up window for "Failed" and "Solved" messages
- [ ] Add a high-score or best-time record system
- [ ] Add docstrings to all functions
- [ ] Implement a board solver to ensure the generated board is solvable without guessing
- [ ] Consider adding different classes or states to manage various game phases (e.g., "Running", "Paused", "GameOver")
- [x] Offer different Minesweeper visuals and sounds for classic Minesweeper versions (Windows 3.1, XP)
- [ ] Create theme for Aero Minesweeper (Windows Vista)
- [ ] Implement animations for tile generation, bomb detonation, and more