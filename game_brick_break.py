import pygame
import random
import sys

"""
    TEST FOR game_brick_pong.py
    TODO
        - duplicate ball
        - (BUG) redo duplicate_ball(); previously turning into a square
        - (BUG) bricks collision and ball deflection
"""

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
COLORS = [WHITE,RED,GREEN,BLUE,YELLOW] # BG IS BLACK

# Brick dimensions
BRICK_WIDTH = 80
BRICK_HEIGHT = 30

# Ball properties
BALL_RADIUS = 10
BALL_SPEED = 5

# Platform properties
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = BLUE

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Break Game")

FPS = 60
clock = pygame.time.Clock()

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface([2 * radius, 2 * radius], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Collision with X walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        # Collision with Top wall
        if self.rect.top <= 0:
            self.dy = -self.dy
        # platform missed ball. Game closes
        if self.rect.top > SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = (x - width) // 2
        self.rect.y = SCREEN_HEIGHT - height - 10
        self.speed = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Function to create the brick wall
def create_brick_wall(empty_space=1, max_col=10, max_row=5):
    bricks = pygame.sprite.Group()
    for row in range(max_row):
        for column in range(max_col):
            brick = Brick(RED, BRICK_WIDTH, BRICK_HEIGHT)
            brick.rect.x = column * (BRICK_WIDTH + 2) + 1
            brick.rect.y = row * (BRICK_HEIGHT + 2) + 1 + empty_space
            bricks.add(brick)
    return bricks

def duplicate_ball(ball: Ball):
    pass

# Main function
def main():
    all_sprites = pygame.sprite.Group()
    bricks = create_brick_wall(50)
    all_sprites.add(bricks)

    # create platform
    platform = Platform(SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)
    all_sprites.add(platform)

    # create ball
    ball = Ball(WHITE, BALL_RADIUS)
    ball.rect.x = (SCREEN_WIDTH - BALL_RADIUS * 2) // 2
    ball.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT - BALL_RADIUS * 2 - PLATFORM_HEIGHT
    all_sprites.add(ball)

    # Game loop
    running = True
    ball_moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not ball_moving:
                    ball_moving = True
                    ball.dx = BALL_SPEED
                    ball.dy = -BALL_SPEED

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            platform.speed = -5
        elif keys[pygame.K_d]:
            platform.speed = 5
        else:
            platform.speed = 0

        all_sprites.update()

        # Check for ball collision with platform
        if pygame.sprite.collide_rect(ball, platform):
            ball.dy = -ball.dy
            
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

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
