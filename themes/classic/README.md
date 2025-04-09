# Classic Theme Styles

To display a style in the app, you need to **register it in the manifest.json** file for the theme.

<br><br>

## `manifest.json`(to be implemented)

Each registered style must define:

- id – unique technical ID
- name – display name
- path – path to the JSON file

TODO: If icon is not defined, it will be loaded from the Classic Theme fallback path `assets/classic/fallback/icon.png`.

Icon will be displayd in option menu

```json
{
    "theme": "Classic",
    "styles": [
        {
            "id": "id1",
            "name": "name",
            "path": "path1/id1.json",
            "icon": "path1/icon.png"
        },
        {
            "id": "id2",
            "name": "name",
            "path": "path2/id2.json"
        }
    ]
}
```
<br><br>

## `style.json`

```json
{
    "id": "id",
    "fallback_id": "id"
    "colors": {
        "highlight": [255, 255, 255],
        "neutral": [192, 192, 192],
        "shadow": [128, 128, 128]
    },
    "paths": {
        "tile": "assets/classic/id/images/tile",
        "digit": "assets/classic/id/images/digit",
        "face": "assets/classic/id/images/face",
        "sound": "assets/classic/id/sounds"
    },
    "logo": "assets/classic/id/logo.png"
}
```

### Style Folder Structure

Each style for the **Classic** theme should include a set of graphics and sounds in the following folder layout:

```bash
id/
├── logo.png                # Style logo (32×32 px)
├── images/
│   ├── tile/               # Board tiles (16×16 px)
│   │   ├── closed_blank.png
│   │   ├── closed_flagged.png
│   │   ├── closed_question.png
│   │   ├── open_0.png
│   │   ├── open_1.png
│   │   ├── open_2.png
│   │   ├── open_3.png
│   │   ├── open_4.png
│   │   ├── open_5.png
│   │   ├── open_6.png
│   │   ├── open_7.png
│   │   ├── open_8.png
│   │   ├── open_bomb.png
│   │   ├── open_bomb_missflagged.png
│   │   └── open_bomb_red.png
│   ├── digit/              # Digit sprites (13×23 px)
│   │   ├── -.png
│   │   ├── 0.png
│   │   ├── 1.png
│   │   ├── 2.png
│   │   ├── 3.png
│   │   ├── 4.png
│   │   ├── 5.png
│   │   ├── 6.png
│   │   ├── 7.png
│   │   ├── 8.png
│   │   └── 9.png
│   └── face/               # Smile face sprites (26×26 px)
│       ├── facedead.png
│       ├── faceooh.png
│       ├── facesmile.png
│       ├── facewin.png
│       └── opensmile.png
└── sounds/                 # Sound effects (.mp3)
    ├── lose.mp3
    ├── tick.mp3
    └── win.mp3
```

### Scaling
All graphics are stored at base resolution (16×16, 13×23, 26×26).  
The actual size in-game is determined dynamically based on `ui_scale`

### TODO: Fallbacks
- Any missing fields or assets will be loaded from its `fallback_id`
- If no fallback_id is specified, the theme will fall back to the `fallback.json` where default paths lead to Windows XP images and sounds.