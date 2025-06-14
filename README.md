# Modern Snakes and Ladders

A modern and polished implementation of the classic Snakes and Ladders board game using Python and Pygame.

## Features

- 10x10 grid board (100 squares) with alternating colors for a checkerboard effect
- Snakes represented with billionaire faces (Elon Musk, Jeff Bezos, etc.)
- Clean and vibrant UI with dark mode theme
- Human vs AI gameplay
- Animated dice roll with visual effects and smooth transitions
- Enhanced player tokens with glowing effects and smooth animations
- Sound effects for dice roll, landing on snakes or ladders, and game win
- Modularized code structure using OOP principles
- Responsive design that works with different screen resolutions

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/modern-snakes-and-ladders.git
   cd modern-snakes-and-ladders
   ```

2. Install the required dependencies:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python main.py
   ```

## How to Play

1. Click "Start Game" on the main menu
2. Click "Roll Dice" or press SPACE to roll the dice and move your token
3. If you land on a ladder, you'll climb up
4. If you land on a snake, you'll slide down
5. First player to reach square 100 wins!

## Game Controls

- Click "Roll Dice" or press SPACE to roll the dice
- Click "Main Menu" to return to the main menu
- Close the window to quit

## Project Structure

- `main.py`: Main entry point for the game
- `game/`: Contains game logic
  - `game_manager.py`: Manages game state and rules
- `ui/`: Contains UI components
  - `constants.py`: Game constants and settings
  - `components.py`: UI components (Board, Dice, PlayerToken, etc.)
  - `screens.py`: Game screens (Welcome, Game, GameOver)
- `assets/`: Contains game assets
  - `images/`: Images for billionaires, dice, etc.
  - `sounds/`: Sound effects

## Customization

You can customize the game by modifying the constants in `ui/constants.py`:
- Change the board size
- Modify snake and ladder positions
- Adjust colors and fonts
- Add or remove billionaire snake heads

## License

This project is licensed under the MIT License - see the LICENSE file for details.
