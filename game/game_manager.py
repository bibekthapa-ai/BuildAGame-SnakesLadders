"""
Game Manager module for handling game logic
"""
import random
import time
import pygame
from ui.constants import SNAKES, LADDERS, PLAYER_TYPES, GAME_STATES

class Player:
    """Player class representing a player in the game"""
    def __init__(self, player_id, player_type=PLAYER_TYPES["HUMAN"]):
        self.id = player_id
        self.position = 1  # Start at position 1
        self.type = player_type
        self.target_position = 1  # For animation
        self.is_moving = False
        self.has_won = False
        self.last_roll = 0
        
    def reset(self):
        """Reset player to initial state"""
        self.position = 1
        self.target_position = 1
        self.is_moving = False
        self.has_won = False
        self.last_roll = 0
        
    def roll_dice(self):
        """Roll the dice and return the result"""
        self.last_roll = random.randint(1, 6)
        return self.last_roll
    
    def move(self, steps):
        """Set target position for movement"""
        self.target_position = min(self.position + steps, 100)
        self.is_moving = True
        
    def update_position(self):
        """Update position to target position"""
        self.position = self.target_position
        self.is_moving = False
        
        # Check if player has won
        if self.position == 100:
            self.has_won = True
            return True
        return False
    
    def check_snake_or_ladder(self):
        """Check if player landed on a snake or ladder and update position"""
        if self.position in SNAKES:
            self.target_position = SNAKES[self.position]
            self.is_moving = True
            return "snake"
        elif self.position in LADDERS:
            self.target_position = LADDERS[self.position]
            self.is_moving = True
            return "ladder"
        return None

class GameManager:
    """Game Manager class for handling game logic"""
    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.current_player_idx = 0
        self.game_state = GAME_STATES["IDLE"]
        self.last_state_change = 0
        self.winner = None
        
    def reset_game(self, game_mode="human_vs_ai"):
        """Reset the game with the specified mode"""
        self.players[0].reset()
        self.players[1].reset()
        
        # Always set player 2 as AI
        self.players[1].type = PLAYER_TYPES["AI"]
            
        self.current_player_idx = 0
        self.game_state = GAME_STATES["IDLE"]
        self.last_state_change = 0
        self.winner = None
        
    def get_current_player(self):
        """Get the current player"""
        return self.players[self.current_player_idx]
    
    def next_player(self):
        """Switch to the next player"""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.game_state = GAME_STATES["IDLE"]
        
    def roll_dice(self):
        """Roll the dice for the current player"""
        if self.game_state != GAME_STATES["IDLE"]:
            return None
            
        player = self.get_current_player()
        roll_result = player.roll_dice()
        
        # Set game state to rolling
        self.game_state = GAME_STATES["ROLLING"]
        self.last_state_change = time.time()
        
        # Schedule the move after a delay
        return roll_result
    
    def move_player(self):
        """Move the current player based on dice roll"""
        player = self.get_current_player()
        
        # Move player
        player.move(player.last_roll)
        self.game_state = GAME_STATES["MOVING"]
        
    def update(self):
        """Update game state"""
        player = self.get_current_player()
        
        # Handle state transitions
        if self.game_state == GAME_STATES["ROLLING"]:
            # Wait for rolling animation to complete
            if time.time() - self.last_state_change > 1.0:
                self.move_player()
                
        elif self.game_state == GAME_STATES["MOVING"]:
            # Check if player has reached target position
            if not player.is_moving:
                # Update player position
                player.update_position()
                
                # Check if player landed on a snake or ladder
                result = player.check_snake_or_ladder()
                
                if result:
                    # Player landed on a snake or ladder, wait for animation
                    self.game_state = GAME_STATES["WAITING"]
                    self.last_state_change = time.time()
                else:
                    # Check if player has won
                    if player.position == 100:
                        self.winner = player.id
                        self.game_state = GAME_STATES["GAME_OVER"]
                    else:
                        # Switch to next player
                        self.next_player()
                        
                        # If next player is AI, automatically roll
                        if self.get_current_player().type == PLAYER_TYPES["AI"]:
                            self.roll_dice()
                
        elif self.game_state == GAME_STATES["WAITING"]:
            # Wait for snake/ladder animation to complete
            if time.time() - self.last_state_change > 1.0:
                # Update player position
                player.update_position()
                
                # Check if player has won
                if player.position == 100:
                    self.winner = player.id
                    self.game_state = GAME_STATES["GAME_OVER"]
                else:
                    # Switch to next player
                    self.next_player()
                    
                    # If next player is AI, automatically roll
                    if self.get_current_player().type == PLAYER_TYPES["AI"]:
                        self.roll_dice()
    
    def get_winner(self):
        """Get the winner of the game"""
        return self.winner
