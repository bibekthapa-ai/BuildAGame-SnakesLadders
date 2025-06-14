"""
UI components for the game
"""
import pygame
import math
import random
from ui.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES, FONTS,
    BOARD_SIZE, BOARD_WIDTH, BOARD_HEIGHT, BOARD_MARGIN,
    SQUARE_SIZE, SNAKES, LADDERS, BILLIONAIRE_SNAKES
)

class Button:
    """Button UI component"""
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
        self.font = pygame.font.SysFont(FONTS["button"], FONT_SIZES["button"])
        
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hover = self.rect.collidepoint(mouse_pos)
        
    def draw(self, surface):
        """Draw the button"""
        # Draw button background
        color = COLORS["button_hover"] if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLORS["text"], self.rect, width=2, border_radius=10)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_clicked(self, mouse_pos):
        """Check if button is clicked"""
        return self.rect.collidepoint(mouse_pos)

class Board:
    """Game board UI component"""
    def __init__(self, surface):
        self.surface = surface
        self.rect = pygame.Rect(BOARD_MARGIN, BOARD_MARGIN, BOARD_WIDTH, BOARD_HEIGHT)
        self.font = pygame.font.SysFont(FONTS["small"], FONT_SIZES["small"])
        
        # Load snake and ladder images
        self.snake_images = {}
        self.ladder_image = None
        
        try:
            # Try to load billionaire snake images
            for pos, filename in BILLIONAIRE_SNAKES.items():
                self.snake_images[pos] = pygame.image.load(f"assets/images/{filename}")
                self.snake_images[pos] = pygame.transform.scale(
                    self.snake_images[pos], 
                    (SQUARE_SIZE * 0.8, SQUARE_SIZE * 0.8)
                )
            
            # Load ladder image
            self.ladder_image = pygame.image.load("assets/images/ladder.png")
            self.ladder_image = pygame.transform.scale(
                self.ladder_image, 
                (SQUARE_SIZE * 0.6, SQUARE_SIZE * 2)
            )
        except:
            print("Warning: Could not load snake/ladder images. Using placeholder graphics.")
            # Create placeholder graphics
            for pos in SNAKES:
                self.snake_images[pos] = None
            self.ladder_image = None
        
    def get_square_position(self, square_number):
        """Get the pixel position of a square on the board"""
        if square_number < 1 or square_number > 100:
            return (0, 0)
            
        # Convert square number to row and column
        # Note: Row 0 is at the bottom, Row 9 is at the top
        row = 9 - (square_number - 1) // 10
        
        # Column depends on the row (alternating left-to-right and right-to-left)
        if row % 2 == 1:  # Odd rows go left to right
            col = (square_number - 1) % 10
        else:  # Even rows go right to left
            col = 9 - (square_number - 1) % 10
            
        # Convert to pixel position
        x = self.rect.left + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.rect.top + row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        return (x, y)
        
    def draw(self, surface):
        """Draw the game board"""
        # Draw board background
        pygame.draw.rect(surface, COLORS["text"], self.rect, width=2)
        
        # Draw squares
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Calculate square number
                if row % 2 == 0:  # Even rows (0, 2, 4, 6, 8)
                    square_num = 100 - row * 10 - col
                else:  # Odd rows (1, 3, 5, 7, 9)
                    square_num = 100 - row * 10 - 9 + col
                
                # Calculate square position
                x = self.rect.left + col * SQUARE_SIZE
                y = self.rect.top + row * SQUARE_SIZE
                
                # Draw square
                color = COLORS["square_light"] if (row + col) % 2 == 0 else COLORS["square_dark"]
                pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw square number
                text = self.font.render(str(square_num), True, COLORS["text"])
                text_rect = text.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                surface.blit(text, text_rect)
        
        # Draw snakes
        for head, tail in SNAKES.items():
            head_pos = self.get_square_position(head)
            tail_pos = self.get_square_position(tail)
            
            # Draw snake body (a curved line with gradient color)
            control_point = (
                (head_pos[0] + tail_pos[0]) // 2 + random.randint(-50, 50),
                (head_pos[1] + tail_pos[1]) // 2 + random.randint(-50, 50)
            )
            
            # Draw a quadratic bezier curve with gradient
            points = []
            for t in range(0, 101, 5):
                t = t / 100
                x = (1 - t) ** 2 * head_pos[0] + 2 * (1 - t) * t * control_point[0] + t ** 2 * tail_pos[0]
                y = (1 - t) ** 2 * head_pos[1] + 2 * (1 - t) * t * control_point[1] + t ** 2 * tail_pos[1]
                points.append((int(x), int(y)))
            
            # Draw snake body with thickness and gradient
            if len(points) >= 2:
                # Draw snake body with gradient effect
                for i in range(len(points) - 1):
                    # Calculate gradient color
                    t = i / (len(points) - 1)
                    r = int(255 - t * 100)
                    g = int(80 - t * 40)
                    b = int(80 - t * 40)
                    color = (r, g, b)
                    
                    # Draw thicker line segment
                    pygame.draw.line(surface, color, points[i], points[i+1], width=8)
                
                # Draw snake scales (small circles along the body)
                for i in range(1, len(points) - 1, 2):
                    pygame.draw.circle(surface, (255, 100, 100), points[i], 4)
            
            # Draw snake head (billionaire image if available)
            if head in self.snake_images and self.snake_images[head] is not None:
                img_rect = self.snake_images[head].get_rect(center=head_pos)
                surface.blit(self.snake_images[head], img_rect)
            else:
                # Draw improved snake head
                pygame.draw.circle(surface, (255, 60, 60), head_pos, SQUARE_SIZE // 3)
                pygame.draw.circle(surface, (200, 30, 30), head_pos, SQUARE_SIZE // 3 - 3)
                
                # Draw eyes
                eye_offset = SQUARE_SIZE // 8
                pygame.draw.circle(surface, (255, 255, 255), 
                                  (head_pos[0] - eye_offset, head_pos[1] - eye_offset), 5)
                pygame.draw.circle(surface, (255, 255, 255), 
                                  (head_pos[0] + eye_offset, head_pos[1] - eye_offset), 5)
                pygame.draw.circle(surface, (0, 0, 0), 
                                  (head_pos[0] - eye_offset, head_pos[1] - eye_offset), 2)
                pygame.draw.circle(surface, (0, 0, 0), 
                                  (head_pos[0] + eye_offset, head_pos[1] - eye_offset), 2)
                
                # Draw tongue
                tongue_points = [
                    head_pos,
                    (head_pos[0], head_pos[1] + SQUARE_SIZE // 4),
                    (head_pos[0] - SQUARE_SIZE // 6, head_pos[1] + SQUARE_SIZE // 3),
                    (head_pos[0] + SQUARE_SIZE // 6, head_pos[1] + SQUARE_SIZE // 3)
                ]
                pygame.draw.line(surface, (255, 0, 0), tongue_points[0], tongue_points[1], 3)
                pygame.draw.line(surface, (255, 0, 0), tongue_points[1], tongue_points[2], 3)
                pygame.draw.line(surface, (255, 0, 0), tongue_points[1], tongue_points[3], 3)
            
            # Draw snake tail
            pygame.draw.circle(surface, (180, 50, 50), tail_pos, SQUARE_SIZE // 5)
            pygame.draw.circle(surface, (150, 30, 30), tail_pos, SQUARE_SIZE // 5 - 2)
        
        # Draw ladders
        for bottom, top in LADDERS.items():
            bottom_pos = self.get_square_position(bottom)
            top_pos = self.get_square_position(top)
            
            if self.ladder_image:
                # Calculate angle and distance
                dx = top_pos[0] - bottom_pos[0]
                dy = top_pos[1] - bottom_pos[1]
                angle = math.degrees(math.atan2(dy, dx))
                distance = math.sqrt(dx ** 2 + dy ** 2)
                
                # Scale ladder image to match distance
                scaled_ladder = pygame.transform.scale(
                    self.ladder_image, 
                    (int(distance * 0.8), self.ladder_image.get_height())
                )
                
                # Rotate ladder image
                rotated_ladder = pygame.transform.rotate(scaled_ladder, angle - 90)
                
                # Calculate position
                mid_x = (bottom_pos[0] + top_pos[0]) // 2
                mid_y = (bottom_pos[1] + top_pos[1]) // 2
                ladder_rect = rotated_ladder.get_rect(center=(mid_x, mid_y))
                
                # Draw ladder
                surface.blit(rotated_ladder, ladder_rect)
            else:
                # Draw improved ladder
                # Calculate direction and length
                dx = top_pos[0] - bottom_pos[0]
                dy = top_pos[1] - bottom_pos[1]
                length = math.sqrt(dx ** 2 + dy ** 2)
                
                if length > 0:
                    # Calculate perpendicular offset for rails
                    offset_x = -dy * 8 / length
                    offset_y = dx * 8 / length
                    
                    # Draw side rails with gradient
                    for i in range(100):
                        t = i / 99
                        # Start and end points for this segment
                        x1 = bottom_pos[0] + dx * t
                        y1 = bottom_pos[1] + dy * t
                        x2 = bottom_pos[0] + dx * (t + 0.01)
                        y2 = bottom_pos[1] + dy * (t + 0.01)
                        
                        # Calculate gradient color (gold to light gold)
                        r = int(180 + t * 75)
                        g = int(140 + t * 60)
                        b = int(20 + t * 40)
                        color = (r, g, b)
                        
                        # Draw rail segments
                        pygame.draw.line(
                            surface, 
                            color, 
                            (x1 - offset_x, y1 - offset_y),
                            (x2 - offset_x, y2 - offset_y),
                            width=4
                        )
                        pygame.draw.line(
                            surface, 
                            color, 
                            (x1 + offset_x, y1 + offset_y),
                            (x2 + offset_x, y2 + offset_y),
                            width=4
                        )
                    
                    # Draw rungs
                    num_rungs = max(3, int(length / 40))
                    for i in range(num_rungs):
                        t = (i + 0.5) / num_rungs
                        x1 = bottom_pos[0] + dx * t - offset_x
                        y1 = bottom_pos[1] + dy * t - offset_y
                        x2 = bottom_pos[0] + dx * t + offset_x
                        y2 = bottom_pos[1] + dy * t + offset_y
                        
                        # Draw rung with 3D effect
                        pygame.draw.line(surface, (180, 140, 20), (x1, y1), (x2, y2), width=5)
                        pygame.draw.line(surface, (220, 180, 60), (x1, y1), (x2, y2), width=3)

class Dice:
    """Dice UI component with enhanced animation"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 80
        self.value = 1
        self.rolling = False
        self.roll_frames = 0
        self.max_roll_frames = 20  # Increased for longer animation
        self.roll_speed = 2  # Frames per dice change
        self.roll_angle = 0  # For rotation animation
        self.roll_scale = 1.0  # For bounce animation
        
        # Load dice images
        self.dice_images = []
        try:
            for i in range(1, 7):
                img = pygame.image.load(f"assets/images/dice_{i}.png")
                img = pygame.transform.scale(img, (self.size, self.size))
                self.dice_images.append(img)
        except:
            print("Warning: Could not load dice images. Using placeholder graphics.")
            self.dice_images = [None] * 6
        
    def update(self, value):
        """Update dice state"""
        if value != self.value and not self.rolling:
            self.value = value
            self.rolling = True
            self.roll_frames = 0
            self.roll_angle = 0
            self.roll_scale = 1.0
        
        if self.rolling:
            self.roll_frames += 1
            
            # Update rotation and scale for animation
            self.roll_angle = (self.roll_frames * 15) % 360
            
            # Bounce effect
            progress = self.roll_frames / self.max_roll_frames
            if progress < 0.5:
                self.roll_scale = 1.0 + 0.3 * math.sin(progress * math.pi)
            else:
                self.roll_scale = 1.0
            
            if self.roll_frames >= self.max_roll_frames:
                self.rolling = False
                self.roll_angle = 0
                self.roll_scale = 1.0
        
    def draw(self, surface):
        """Draw the dice with animation"""
        if self.rolling:
            # Show random dice face during rolling animation
            if self.roll_frames % self.roll_speed == 0:
                random_value = random.randint(1, 6)
            else:
                random_value = (self.roll_frames // self.roll_speed) % 6 + 1
            
            # Apply rotation and scaling
            dice_size = int(self.size * self.roll_scale)
            x_offset = (dice_size - self.size) // 2
            y_offset = (dice_size - self.size) // 2
            
            if 0 < random_value <= len(self.dice_images) and self.dice_images[random_value - 1] is not None:
                # Scale the dice image
                scaled_dice = pygame.transform.scale(self.dice_images[random_value - 1], (dice_size, dice_size))
                # Rotate the dice image
                rotated_dice = pygame.transform.rotate(scaled_dice, self.roll_angle)
                # Get the rect for the rotated image
                rect = rotated_dice.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
                # Draw the dice
                surface.blit(rotated_dice, rect)
            else:
                # Draw placeholder dice with animation
                rect = pygame.Rect(
                    self.x - x_offset, 
                    self.y - y_offset, 
                    dice_size, 
                    dice_size
                )
                
                # Create a surface for the dice
                dice_surface = pygame.Surface((dice_size, dice_size), pygame.SRCALPHA)
                pygame.draw.rect(dice_surface, (255, 255, 255), 
                                (0, 0, dice_size, dice_size), border_radius=dice_size//8)
                pygame.draw.rect(dice_surface, COLORS["text"], 
                                (0, 0, dice_size, dice_size), width=2, border_radius=dice_size//8)
                
                # Draw dots based on value
                dot_positions = {
                    1: [(0.5, 0.5)],
                    2: [(0.25, 0.25), (0.75, 0.75)],
                    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
                    4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
                    5: [(0.25, 0.25), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.75, 0.75)],
                    6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
                }
                
                if random_value in dot_positions:
                    for pos in dot_positions[random_value]:
                        x = pos[0] * dice_size
                        y = pos[1] * dice_size
                        pygame.draw.circle(dice_surface, COLORS["text"], (x, y), dice_size // 10)
                
                # Rotate the dice surface
                rotated_dice = pygame.transform.rotate(dice_surface, self.roll_angle)
                # Get the rect for the rotated surface
                rot_rect = rotated_dice.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
                # Draw the dice
                surface.blit(rotated_dice, rot_rect)
        else:
            # Draw the final dice value
            value = self.value
            
            # Draw dice
            if 0 < value <= len(self.dice_images) and self.dice_images[value - 1] is not None:
                # Draw dice image
                surface.blit(self.dice_images[value - 1], (self.x, self.y))
            else:
                # Draw placeholder dice
                pygame.draw.rect(surface, (255, 255, 255), 
                                (self.x, self.y, self.size, self.size), border_radius=10)
                pygame.draw.rect(surface, COLORS["text"], 
                                (self.x, self.y, self.size, self.size), width=2, border_radius=10)
                
                # Add a subtle gradient effect
                for i in range(10):
                    pygame.draw.rect(surface, (255, 255, 255, 150 - i*15), 
                                    (self.x + i, self.y + i, self.size - i*2, self.size - i*2), 
                                    border_radius=10-i if 10-i > 0 else 0)
                
                # Draw dots based on value
                dot_positions = {
                    1: [(0.5, 0.5)],
                    2: [(0.25, 0.25), (0.75, 0.75)],
                    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
                    4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
                    5: [(0.25, 0.25), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.75, 0.75)],
                    6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
                }
                
                if value in dot_positions:
                    for pos in dot_positions[value]:
                        x = self.x + pos[0] * self.size
                        y = self.y + pos[1] * self.size
                        # Draw dot with shadow effect
                        pygame.draw.circle(surface, (30, 30, 30), (x+2, y+2), self.size // 10)
                        pygame.draw.circle(surface, COLORS["text"], (x, y), self.size // 10)

class PlayerToken:
    """Player token UI component with improved visuals"""
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color
        self.position = 1
        self.visual_position = 1
        self.size = 20
        self.offset = 10 * player_id  # Offset to prevent tokens from overlapping
        self.animation_progress = 0  # For movement animation
        self.is_moving = False
        self.start_pos = None
        self.target_pos = None
        self.bounce_offset = 0  # For bouncing animation
        self.glow_size = 0  # For glow effect
        self.glow_direction = 1  # 1 for increasing, -1 for decreasing
        
        # Token design elements
        self.token_designs = [
            {  # Player 1 (Human)
                "main_color": color,
                "highlight_color": (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)),
                "shadow_color": (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0)),
                "symbol": "H"  # Human
            },
            {  # Player 2 (AI)
                "main_color": color,
                "highlight_color": (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)),
                "shadow_color": (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0)),
                "symbol": "AI"  # AI
            }
        ]
        
        # Font for token symbol
        self.font = pygame.font.SysFont(FONTS["small"], FONT_SIZES["small"], bold=True)
        
    def update(self, position, target_position):
        """Update token position with animation"""
        # If position changed, start animation
        if self.position != position and not self.is_moving:
            self.position = position
            self.start_pos = self.get_interpolated_position()
            self.is_moving = True
            self.animation_progress = 0
            
        # If target position changed, update it
        if target_position != self.visual_position:
            self.visual_position = target_position
            
        # Update animation
        if self.is_moving:
            self.animation_progress += 0.05  # Animation speed
            
            # Update bounce effect
            self.bounce_offset = math.sin(self.animation_progress * math.pi) * 10
            
            if self.animation_progress >= 1.0:
                self.is_moving = False
                self.bounce_offset = 0
                
        # Update glow effect
        self.glow_size += 0.2 * self.glow_direction
        if self.glow_size > 5:
            self.glow_direction = -1
        elif self.glow_size < 0:
            self.glow_direction = 1
    
    def get_interpolated_position(self):
        """Get the current interpolated position for smooth movement"""
        if not self.is_moving or self.start_pos is None:
            return None
            
        # Ease-out function for smooth animation
        t = 1 - (1 - self.animation_progress) ** 2
        
        return t
        
    def draw(self, surface, get_position_func):
        """Draw the player token with improved visuals"""
        # Get position on board
        x, y = get_position_func(self.visual_position)
        
        # Add offset to prevent overlapping
        x += self.offset
        
        # Apply animation if moving
        if self.is_moving and self.start_pos is not None:
            # Get target position
            target_x, target_y = get_position_func(self.position)
            target_x += self.offset
            
            # Interpolate between start and target positions
            t = self.get_interpolated_position()
            x = x * (1 - t) + target_x * t
            
            # Apply bounce effect
            y -= self.bounce_offset
        
        # Get token design
        design = self.token_designs[self.player_id]
        
        # Draw glow effect when moving or as current player
        if self.is_moving or self.glow_size > 0:
            glow_radius = self.size + self.glow_size
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            
            # Create radial gradient for glow
            for i in range(10):
                alpha = 150 - i * 15
                if alpha > 0:
                    pygame.draw.circle(
                        glow_surface, 
                        (*design["highlight_color"], alpha), 
                        (glow_radius, glow_radius), 
                        glow_radius - i
                    )
            
            # Draw glow
            surface.blit(glow_surface, (x - glow_radius, y - glow_radius))
        
        # Draw token base (3D effect)
        pygame.draw.circle(surface, design["shadow_color"], (x+2, y+2), self.size)  # Shadow
        pygame.draw.circle(surface, design["main_color"], (x, y), self.size)  # Main circle
        
        # Draw highlight
        pygame.draw.circle(surface, design["highlight_color"], (x-self.size//3, y-self.size//3), self.size//3)
        
        # Draw border
        pygame.draw.circle(surface, COLORS["text"], (x, y), self.size, width=2)
        
        # Draw player symbol
        text = self.font.render(design["symbol"], True, (255, 255, 255))
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

class Scoreboard:
    """Enhanced scoreboard UI component"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 180
        self.height = 150  # Adjusted height
        self.font = pygame.font.SysFont(FONTS["text"], FONT_SIZES["text"])
        self.font_small = pygame.font.SysFont(FONTS["small"], FONT_SIZES["small"])
        self.font_title = pygame.font.SysFont(FONTS["subtitle"], FONT_SIZES["subtitle"], bold=True)
        self.players = []
        self.current_player_idx = 0
        self.animation_counter = 0
        
        # Stats tracking
        self.stats = {
            "moves": [0, 0],
            "ladders": [0, 0],
            "snakes": [0, 0],
            "sixes": [0, 0]
        }
        
    def update(self, players, current_player_idx):
        """Update scoreboard with player information"""
        self.players = players
        self.current_player_idx = current_player_idx
        
        # Update animation counter
        self.animation_counter = (self.animation_counter + 1) % 60
        
    def update_stats(self, player_idx, stat_type):
        """Update player statistics"""
        if stat_type in self.stats and 0 <= player_idx < 2:
            self.stats[stat_type][player_idx] += 1
        
    def draw(self, surface):
        """Draw the enhanced scoreboard"""
        # Draw scoreboard background with gradient
        for i in range(self.height):
            # Calculate gradient color
            t = i / self.height
            r = int(50 + t * 20)
            g = int(50 + t * 20)
            b = int(65 + t * 20)
            color = (r, g, b)
            
            pygame.draw.line(surface, color, 
                            (self.x, self.y + i), 
                            (self.x + self.width, self.y + i))
        
        # Draw border with rounded corners
        pygame.draw.rect(surface, COLORS["text"], 
                        (self.x, self.y, self.width, self.height), 
                        width=2, border_radius=10)
        
        # Draw player information
        for i, player in enumerate(self.players):
            # Determine player color and name
            if i == 0:
                color = COLORS["player1"]
                name = "HUMAN"
            else:
                color = COLORS["player2"]
                name = "AI"
                
            # Highlight current player with pulsing effect
            if i == self.current_player_idx:
                # Pulsing highlight
                pulse = abs(math.sin(self.animation_counter * 0.1)) * 30
                highlight_color = (color[0], color[1], color[2], 100 + int(pulse))
                
                # Draw highlight background
                highlight_surface = pygame.Surface((self.width - 20, 30), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, highlight_color, 
                                (0, 0, self.width - 20, 30), 
                                border_radius=5)
                surface.blit(highlight_surface, (self.x + 10, self.y + 15 + i * 60))
            
            # Draw player name and position
            player_text = f"{name}: Position {player.position}"
            text = self.font.render(player_text, True, color)
            surface.blit(text, (self.x + 15, self.y + 20 + i * 60))
            
            # Draw last roll with dice icon
            if player.last_roll > 0:
                roll_text = f"Last Roll: {player.last_roll}"
                text = self.font_small.render(roll_text, True, color)
                surface.blit(text, (self.x + 15, self.y + 45 + i * 60))
                
                # Draw mini dice
                dice_size = 15
                dice_x = self.x + 100
                dice_y = self.y + 45 + i * 60
                pygame.draw.rect(surface, (255, 255, 255), 
                                (dice_x, dice_y, dice_size, dice_size), 
                                border_radius=3)
                pygame.draw.rect(surface, color, 
                                (dice_x, dice_y, dice_size, dice_size), 
                                width=1, border_radius=3)
                
                # Draw dots based on last roll
                dot_positions = {
                    1: [(0.5, 0.5)],
                    2: [(0.25, 0.25), (0.75, 0.75)],
                    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
                    4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
                    5: [(0.25, 0.25), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.75, 0.75)],
                    6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
                }
                
                if player.last_roll in dot_positions:
                    for pos in dot_positions[player.last_roll]:
                        x = dice_x + pos[0] * dice_size
                        y = dice_y + pos[1] * dice_size
                        pygame.draw.circle(surface, (0, 0, 0), (x, y), dice_size // 5)
