#!/usr/bin/env python3
"""
Modern Snakes and Ladders Game
Main entry point for the game
"""
import sys
import pygame
from game.game_manager import GameManager
from ui.screens import WelcomeScreen, GameScreen, GameOverScreen
from ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLORS

def main():
    """Main function to initialize and run the game"""
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()  # For sound effects
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Modern Snakes and Ladders")
    
    # Create a clock for controlling the frame rate
    clock = pygame.time.Clock()
    
    # Initialize game manager
    game_manager = GameManager()
    
    # Initialize screens
    welcome_screen = WelcomeScreen(screen)
    game_screen = GameScreen(screen, game_manager)
    game_over_screen = GameOverScreen(screen)
    
    # Set initial screen
    current_screen = welcome_screen
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to current screen
            result = current_screen.handle_event(event)
            
            # Handle screen transitions
            if result == "start_game":
                game_manager.reset_game(welcome_screen.get_game_mode())
                current_screen = game_screen
            elif result == "game_over":
                game_over_screen.set_winner(game_manager.get_winner())
                current_screen = game_over_screen
            elif result == "main_menu":
                current_screen = welcome_screen
            elif result == "quit":
                running = False
        
        # Update current screen
        current_screen.update()
        
        # Draw current screen
        screen.fill(COLORS["background"])
        current_screen.draw()
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
