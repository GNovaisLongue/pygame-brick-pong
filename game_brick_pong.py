import pygame
import random
import sys
from enum import Enum

"""
    TODO
        - (BUG) sometimes, ball slides on platform; paddle and ball collision
        - (BUG) bricks collision and ball wrong deflection
        - (FIX) KEYS: .QUIT and .K_ESCAPE to close
        - (FIX) KEYS: .MOUSEBUTTONDOWN and .K_SPACE to begin
        - SEPARATE classes and functions
        - ORGANIZE logic
"""

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Pong")

FPS = 60
clock = pygame.time.Clock()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [WHITE,RED,GREEN,BLUE,YELLOW] # BG IS BLACK

# PADDLE
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_COLOR = WHITE

# BALL
BALL_SIZE = 20
BALL_RADIUS = 10
BALL_SPEED= 5
BALL_POS = ["middle", "left", "right"]
BEGIN_POS = "left"

# BRICK
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ORIENTATION = ['horizontal', 'vertical']
WALL_SIDE = "vertical"

# Pong ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, begin_pos=BALL_POS):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.ball_moving = False
        self.ball_pos(begin_pos)
        
    def ball_pos(self, begin_pos):
        # Ball initial position
        if begin_pos not in BALL_POS:
            print("Ball_pos: Wrong ball position")
            begin_pos="middle"
        match begin_pos:
            case "middle":
                self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            case "left":
                self.rect.x = BALL_SIZE * 2
                self.rect.y = (SCREEN_HEIGHT - BALL_RADIUS * 2) // 2
            case "right":
                self.rect.x = SCREEN_WIDTH - BALL_SIZE * 2 - PADDLE_WIDTH
                self.rect.y = (SCREEN_HEIGHT - BALL_RADIUS * 2) // 2
            case _:
                raise pygame.error("Ball_pos: Something went wrong")
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Collision with Y walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy = -self.dy
        # Platform missed ball. Reset ball position
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.ball_pos(begin_pos=BEGIN_POS)
            self.ball_moving = False

# Pong Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# Function to create the brick wall
def create_brick_wall(max_col=2, max_row=6, sided=BRICK_ORIENTATION):
    bricks = pygame.sprite.Group()
    
    # Brick orientation
    if sided not in BRICK_ORIENTATION:
        print("Brick_side: Wrong brick orientation")
        sided="vertical"
    match sided:
        case "horizontal":
            for row in range(max_row*2):
                for column in range(max_col):
                    brick = Brick(RED, BRICK_WIDTH, BRICK_HEIGHT)
                    brick.rect.x = column * (BRICK_WIDTH + 2) + SCREEN_WIDTH // 2 - BRICK_WIDTH
                    brick.rect.y = row * (BRICK_HEIGHT + 2) + SCREEN_HEIGHT // max_row
                    bricks.add(brick)
        case "vertical":
            for row in range(max_col):
                for column in range(max_row):
                    # invert dimensions
                    brick = Brick(RED, BRICK_HEIGHT, BRICK_WIDTH)
                    brick.rect.x = row * (BRICK_HEIGHT + 2) + SCREEN_WIDTH // 2 - BRICK_HEIGHT
                    brick.rect.y = column * (BRICK_WIDTH + 2) + SCREEN_HEIGHT // BALL_RADIUS
                    bricks.add(brick)
        case _:
            raise pygame.error("Brick_side: Something went wrong")
    return bricks

def main():
    all_sprites = pygame.sprite.Group()
    # Bricks
    bricks = create_brick_wall(sided=WALL_SIDE)
    all_sprites.add(bricks)
    # Create the ball
    ball = Ball(WHITE, BALL_RADIUS,begin_pos=BEGIN_POS)
    # Create the paddles
    paddle1 = Paddle(20, SCREEN_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    paddle2 = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    all_sprites.add(paddle1, paddle2, ball)

    # Game loop
    running = True
    ball.ball_moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not ball.ball_moving:
                    if BEGIN_POS == "left":
                        ball.dx = BALL_SPEED
                        ball.dy = -BALL_SPEED
                    elif BEGIN_POS == "right":
                        ball.dx = -BALL_SPEED
                        ball.dy = -BALL_SPEED
                    else:
                        if random.random() < 0.5:    
                            ball.dx = BALL_SPEED
                            ball.dy = -BALL_SPEED
                        else:
                            ball.dx = -BALL_SPEED
                            ball.dy = -BALL_SPEED
                    ball.ball_moving = True
        
        keys = pygame.key.get_pressed()
        # player 1
        if keys[pygame.K_w]:
            paddle1.speed = -5
        elif keys[pygame.K_s]:
            paddle1.speed = 5
        else:
            paddle1.speed = 0
        # player 2
        if keys[pygame.K_UP]:
            paddle2.speed = -5
        elif keys[pygame.K_DOWN]:
            paddle2.speed = 5
        else:
            paddle2.speed = 0

        # Update
        all_sprites.update()
        
        # Collision with paddles
        if pygame.sprite.collide_rect(ball, paddle1) or pygame.sprite.collide_rect(ball, paddle2):
            ball.dx = -ball.dx
        
        # Check for collision with bricks
        brick_collisions = pygame.sprite.spritecollide(ball, bricks, True)
        if brick_collisions:
            for brick in brick_collisions:
                if random.random() < 0.3:  # 30% chance to duplicate ball when a brick is destroyed
                    break
                    new_ball = duplicate_ball(ball) # nothing happens for now
                    all_sprites.add(new_ball)
                ball.dy = -ball.dy
        
        # Draw / Render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
