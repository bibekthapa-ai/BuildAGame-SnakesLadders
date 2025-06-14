"""
Screen classes for the game UI
"""
import pygame
from ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES, FONTS
from ui.components import Button, Board, Dice, PlayerToken, Scoreboard

class Screen:
    """Base class for all screens"""
    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.SysFont(FONTS["title"], FONT_SIZES["title"], bold=True)
        self.font_subtitle = pygame.font.SysFont(FONTS["subtitle"], FONT_SIZES["subtitle"], bold=True)
        self.font_text = pygame.font.SysFont(FONTS["text"], FONT_SIZES["text"])
        self.font_small = pygame.font.SysFont(FONTS["small"], FONT_SIZES["small"])
        
    def handle_event(self, event):
        """Handle events for the screen"""
        pass
        
    def update(self):
        """Update the screen"""
        pass
        
    def draw(self):
        """Draw the screen"""
        pass

class WelcomeScreen(Screen):
    """Welcome screen with game options"""
    def __init__(self, surface):
        super().__init__(surface)
        
        # Game mode is always human vs AI
        self.game_mode = "human_vs_ai"
        
        # Create start button
        button_width = 300
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.start_button = Button(
            button_x, 320, 
            button_width, button_height, 
            "Start Game", 
            COLORS["button"], 
            COLORS["button_text"]
        )
        
    def handle_event(self, event):
        """Handle events for the welcome screen"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos):
                return "start_game"
        return None
        
    def update(self):
        """Update the welcome screen"""
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.update(mouse_pos)
        
    def draw(self):
        """Draw the welcome screen"""
        # Draw title
        title_text = self.font_title.render("Modern Snakes and Ladders", True, COLORS["text"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.surface.blit(title_text, title_rect)
        
        # Draw button
        self.start_button.draw(self.surface)
        
        # Draw instructions
        instructions = [
            "How to Play:",
            "1. Roll the dice to move your token",
            "2. Land on a ladder to climb up",
            "3. Land on a snake to slide down",
            "4. First player to reach 100 wins!"
        ]
        
        for i, line in enumerate(instructions):
            text = self.font_text.render(line, True, COLORS["text"])
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 420 + i * 25))
            self.surface.blit(text, rect)
    
    def get_game_mode(self):
        """Get the selected game mode"""
        return self.game_mode

class GameScreen(Screen):
    """Main game screen"""
    def __init__(self, surface, game_manager):
        super().__init__(surface)
        self.game_manager = game_manager
        
        # Create game components
        self.board = Board(surface)
        self.dice = Dice(650, 200)
        self.player_tokens = [
            PlayerToken(0, COLORS["player1"]),
            PlayerToken(1, COLORS["player2"])
        ]
        self.scoreboard = Scoreboard(600, 350)
        
        # Create buttons
        self.roll_button = Button(
            600, 150, 
            150, 50, 
            "Roll Dice", 
            COLORS["button"], 
            COLORS["button_text"]
        )
        
        self.menu_button = Button(
            600, 500, 
            150, 50, 
            "Main Menu", 
            COLORS["button"], 
            COLORS["button_text"]
        )
        
        # Load sounds
        self.sounds = {}
        try:
            self.sounds["dice_roll"] = pygame.mixer.Sound("assets/sounds/dice_roll.wav")
            self.sounds["move"] = pygame.mixer.Sound("assets/sounds/move.wav")
            self.sounds["snake"] = pygame.mixer.Sound("assets/sounds/snake.wav")
            self.sounds["ladder"] = pygame.mixer.Sound("assets/sounds/ladder.wav")
            self.sounds["win"] = pygame.mixer.Sound("assets/sounds/win.wav")
        except:
            print("Warning: Could not load sound files. Using placeholder sounds.")
            # Create placeholder sounds
            self.sounds["dice_roll"] = pygame.mixer.Sound(buffer=bytes([0]))
            self.sounds["move"] = pygame.mixer.Sound(buffer=bytes([0]))
            self.sounds["snake"] = pygame.mixer.Sound(buffer=bytes([0]))
            self.sounds["ladder"] = pygame.mixer.Sound(buffer=bytes([0]))
            self.sounds["win"] = pygame.mixer.Sound(buffer=bytes([0]))
        
    def handle_event(self, event):
        """Handle events for the game screen"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.roll_button.is_clicked(event.pos):
                # Only allow rolling if it's the current player's turn and they're human
                current_player = self.game_manager.get_current_player()
                if current_player.type == 0 and self.game_manager.game_state == 0:
                    self.game_manager.roll_dice()
                    self.sounds["dice_roll"].play()
                return None
            elif self.menu_button.is_clicked(event.pos):
                return "main_menu"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Space bar also rolls the dice
                current_player = self.game_manager.get_current_player()
                if current_player.type == 0 and self.game_manager.game_state == 0:
                    self.game_manager.roll_dice()
                    self.sounds["dice_roll"].play()
                return None
        
        # Check if game is over
        if self.game_manager.game_state == 4:  # GAME_OVER
            self.sounds["win"].play()
            return "game_over"
            
        return None
        
    def update(self):
        """Update the game screen"""
        # Update game manager
        self.game_manager.update()
        
        # Update dice animation
        current_player = self.game_manager.get_current_player()
        self.dice.update(current_player.last_roll)
        
        # Update player tokens
        for player in self.game_manager.players:
            self.player_tokens[player.id].update(player.position, player.target_position)
            
            # Play sound effects for movement
            if player.is_moving:
                from ui.constants import SNAKES, LADDERS
                if player.position in SNAKES:
                    self.sounds["snake"].play()
                    self.scoreboard.update_stats(player.id, "snakes")
                elif player.position in LADDERS:
                    self.sounds["ladder"].play()
                    self.scoreboard.update_stats(player.id, "ladders")
                else:
                    self.sounds["move"].play()
                    self.scoreboard.update_stats(player.id, "moves")
                    
                    # Track sixes
                    if player.last_roll == 6:
                        self.scoreboard.update_stats(player.id, "sixes")
                        
                player.is_moving = False
        
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        self.roll_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        
        # Update scoreboard
        self.scoreboard.update(self.game_manager.players, self.game_manager.current_player_idx)
        
    def draw(self):
        """Draw the game screen"""
        # Draw board
        self.board.draw(self.surface)
        
        # Draw player tokens
        for token in self.player_tokens:
            token.draw(self.surface, self.board.get_square_position)
        
        # Draw dice
        self.dice.draw(self.surface)
        
        # Draw scoreboard
        self.scoreboard.draw(self.surface)
        
        # Draw buttons
        self.roll_button.draw(self.surface)
        self.menu_button.draw(self.surface)
        
        # Draw current player indicator with proper margins
        current_player = self.game_manager.get_current_player()
        player_text = f"Player {current_player.id + 1}'s Turn"
        if current_player.type == 1:  # AI
            player_text += " (AI)"
        text = self.font_text.render(player_text, True, COLORS["text"])
        # Position text with proper margins to ensure it's not cut off
        self.surface.blit(text, (600, 100))

class GameOverScreen(Screen):
    """Game over screen"""
    def __init__(self, surface):
        super().__init__(surface)
        self.winner = None
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.play_again_button = Button(
            button_x, 300, 
            button_width, button_height, 
            "Play Again", 
            COLORS["button"], 
            COLORS["button_text"]
        )
        
        self.main_menu_button = Button(
            button_x, 370, 
            button_width, button_height, 
            "Main Menu", 
            COLORS["button"], 
            COLORS["button_text"]
        )
        
    def set_winner(self, winner):
        """Set the winner of the game"""
        self.winner = winner
        
    def handle_event(self, event):
        """Handle events for the game over screen"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_button.is_clicked(event.pos):
                return "start_game"
            elif self.main_menu_button.is_clicked(event.pos):
                return "main_menu"
        return None
        
    def update(self):
        """Update the game over screen"""
        mouse_pos = pygame.mouse.get_pos()
        self.play_again_button.update(mouse_pos)
        self.main_menu_button.update(mouse_pos)
        
    def draw(self):
        """Draw the game over screen"""
        # Draw title
        title_text = self.font_title.render("Game Over", True, COLORS["text"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.surface.blit(title_text, title_rect)
        
        # Draw winner
        if self.winner is not None:
            winner_text = self.font_subtitle.render(f"Player {self.winner + 1} Wins!", True, COLORS["text"])
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.surface.blit(winner_text, winner_rect)
        
        # Draw buttons
        self.play_again_button.draw(self.surface)
        self.main_menu_button.draw(self.surface)
