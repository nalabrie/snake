# Snake

This is the classic Snake game written in Python 3 using Pygame. It was made by very loosely following [this](https://youtu.be/QFvqStqPCRU) YouTube tutorial made by **Clear Code**. My implementation has a handful of changes and I continued to extend it beyond what that video covers.

## How To Play

* Use the `arrow keys` to move the snake
* Press `r` to start a new game
* Eat apples to gain points and grow the snake
* Hitting a wall or yourself kills the snake and ends the game

## Usage

### Pre-Packaged Install

1. Go to the [Releases](https://github.com/nalabrie/snake/releases) page
2. Download the version you want (get the [latest](https://github.com/nalabrie/snake/releases/latest) if unsure)
3. Extract the zip folder somewhere
4. Run `snake.exe`

These pre-packaged releases **only run on Windows 10 64-bit!** They are made with [PyInstaller](https://www.pyinstaller.org/) and do not require any prerequisites.

### Manual Install

1. Check that you have the required [prerequisites](#prerequisites)
2. Download the `snake.py` script, `Font` folder, `Graphics` folder, and `Sound` folder (directory structure should look like it does below)
3. Run the `snake.py` script in a Python 3 interpreter

```
.
├── Font
│   └── PoetsenOne-Regular.ttf
├── Graphics
│   ├── apple.png
│   ├── body_bl.png
│   ├── body_br.png
│   ├── body_horizontal.png
│   ├── body_tl.png
│   ├── body_tr.png
│   ├── body_vertical.png
│   ├── head_down.png
│   ├── head_left.png
│   ├── head_right.png
│   ├── head_up.png
│   ├── tail_down.png
│   ├── tail_left.png
│   ├── tail_right.png
│   └── tail_up.png
├── Sound
│   └── crunch.wav
└── snake.py
```

## Prerequisites

I used

* Python 3.9.2
* Pygame 2.0.1
* SDL 2.0.14

Python 3 is required but older versions of Pygame and SDL may work. I did not test older versions. I also did not test Python 3.8 or older.
