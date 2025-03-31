# Classic Minesweeper in Pygame

<table>
  <tr>
    <td>
      <img src="images/icon/Minesweeper_Icon_App-assets/Icon-macOS-256x256@1x.png" alt="Minesweeper Icon" width="256">
    </td>
    <td>
      Python implementation of the classic Minesweeper game with modern visuals and mechanics.<br>
      Game built using <a href="https://www.pygame.org/news">Pygame</a>.
    </td>
  </tr>
</table>

![Beginner Level](screenshots/gameplay-beginner.png)

---

## Requirements


Make sure you have Python 3 installed, then install the required dependencies from `requirements.txt`. For example:

```bash
pip install -r requirements.txt
```

---

## TODO

- [ ] Implement proper face and tile animation when hovered over and when the mouse button is pressed
- [ ] Implement an options menu with multiple difficulty levels (Beginner, Intermediate, Expert)
- [ ] Implement a pop-up window for "Failed" and "Solved" messages
- [ ] Add a high-score or best-time record system
- [ ] Add docstrings to all functions
- [ ] Implement a board solver to ensure the generated board is solvable without guessing
- [ ] Consider adding different classes or states to manage various game phases (e.g., "Running", "Paused", "GameOver")
- [ ] Offer different Minesweeper visuals and sounds for each Minesweeper version (Windows 3.1, XP, 7)