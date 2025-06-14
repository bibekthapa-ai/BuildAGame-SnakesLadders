"""
Constants for the UI components
"""
import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game board dimensions
BOARD_SIZE = 10  # 10x10 grid
BOARD_WIDTH = 500
BOARD_HEIGHT = 500
BOARD_MARGIN = 50  # Margin from the left and top of the screen

# Square dimensions
SQUARE_SIZE = BOARD_WIDTH // BOARD_SIZE

# Colors - Dark Mode Theme
COLORS = {
    "background": (30, 30, 40),
    "text": (220, 220, 220),
    "button": (80, 120, 200),
    "button_hover": (100, 140, 220),
    "button_text": (255, 255, 255),
    "square_light": (50, 50, 65),
    "square_dark": (35, 35, 50),
    "player1": (255, 100, 100),
    "player2": (100, 255, 100),
    "ai": (100, 180, 255),
    "snake": (255, 80, 80),
    "ladder": (120, 220, 120),
    "highlight": (255, 255, 0, 128),  # Semi-transparent yellow
}

# Fonts
FONT_SIZES = {
    "title": 42,
    "subtitle": 28,
    "button": 22,
    "text": 16,
    "small": 12,
}

# Font names - using more modern and attractive fonts
FONTS = {
    "title": "Arial Black",
    "subtitle": "Arial Bold",
    "text": "Helvetica",
    "button": "Arial",
    "small": "Helvetica"
}

# Game settings
FPS = 60
ANIMATION_SPEED = 10  # Pixels per frame for animations

# Player types
PLAYER_TYPES = {
    "HUMAN": 0,
    "AI": 1,
}

# Game states
GAME_STATES = {
    "IDLE": 0,
    "ROLLING": 1,
    "MOVING": 2,
    "WAITING": 3,
    "GAME_OVER": 4,
}

# Asset paths
ASSETS_PATH = "assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
SOUNDS_PATH = ASSETS_PATH + "sounds/"

# Sound effects
SOUND_EFFECTS = {
    "dice_roll": "dice_roll.wav",
    "move": "move.wav",
    "snake": "snake.wav",
    "ladder": "ladder.wav",
    "win": "win.wav",
}

# Snakes and Ladders positions (start: end)
# Snake positions (head: tail)
SNAKES = {
    17: 7,
    54: 34,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 79,
}

# Ladder positions (bottom: top)
LADDERS = {
    4: 14,
    9: 31,
    20: 38,
    28: 84,
    40: 59,
    51: 67,
    63: 81,
    71: 91,
}

# Billionaire snake heads (for special snake graphics)
BILLIONAIRE_SNAKES = {
    17: "elon_musk.png",
    54: "jeff_bezos.png",
    62: "bill_gates.png",
    87: "mark_zuckerberg.png",
    93: "warren_buffett.png",
    95: "larry_ellison.png",
    98: "bernard_arnault.png",
}
