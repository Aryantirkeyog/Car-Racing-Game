
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game window
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 150, 0)
RED = (220, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 55)

# Road boundaries
ROAD_LEFT = 50
ROAD_RIGHT = 350

# Car settings
CAR_WIDTH = 40
CAR_HEIGHT = 80
PLAYER_Y = 500
PLAYER_SPEED = 10
OBSTACLE_SPEED = 5

# Game variables
player_x = 180
score = 0
obstacles = []
game_over = False
spawn_timer = 0


def reset_game():
    global player_x, score, obstacles, game_over, spawn_timer

    player_x = 180
    score = 0
    obstacles = []
    game_over = False
    spawn_timer = 0


def draw_car(x, y, color):
    pygame.draw.rect(
        screen, color,
        (x, y, CAR_WIDTH, CAR_HEIGHT)
    )

    # Windows
    pygame.draw.rect(
        screen, WHITE,
        (x + 7, y + 12, 26, 20)
    )

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 4, y + 12, 5, 18))
    pygame.draw.rect(screen, BLACK, (x + 39, y + 12, 5, 18))
    pygame.draw.rect(screen, BLACK, (x - 4, y + 52, 5, 18))
    pygame.draw.rect(screen, BLACK, (x + 39, y + 52, 5, 18))


def show_score():
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))


# Main game loop
running = True

while running:

    clock.tick(60)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if game_over and event.key == pygame.K_r:
                reset_game()

    # Game logic
    if not game_over:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED

        # Keep player inside road
        player_x = max(
            ROAD_LEFT,
            min(player_x, ROAD_RIGHT - CAR_WIDTH)
        )

        # Spawn obstacle cars
        spawn_timer += 1

        if spawn_timer >= 60:
            obstacle_x = random.randint(
                ROAD_LEFT, ROAD_RIGHT - CAR_WIDTH
            )

            obstacles.append(
                pygame.Rect(
                    obstacle_x, -CAR_HEIGHT,
                    CAR_WIDTH, CAR_HEIGHT
                )
            )

            spawn_timer = 0

        player_rect = pygame.Rect(
            player_x, PLAYER_Y,
            CAR_WIDTH, CAR_HEIGHT
        )

        # Move obstacles and check collisions
        for obstacle in obstacles[:]:

            obstacle.y += OBSTACLE_SPEED

            if player_rect.colliderect(obstacle):
                game_over = True

            # Increase score when obstacle passes
            if obstacle.top > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

    # Drawing
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(
        screen, GRAY,
        (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT)
    )

    # Road boundaries
    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5
    )

    pygame.draw.line(
        screen, WHITE,
        (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5
    )

    # Road center markings
    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(
            screen, YELLOW,
            (198, y, 4, 40)
        )

    # Draw player
    draw_car(player_x, PLAYER_Y, BLUE)

    # Draw obstacles
    for obstacle in obstacles:
        draw_car(obstacle.x, obstacle.y, RED)

    show_score()

    # Game over screen
    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = big_font.render(
            "GAME OVER", True, RED
        )

        final_score = font.render(
            "Final Score: " + str(score),
            True, WHITE
        )

        restart_text = font.render(
            "Press R to Restart",
            True, YELLOW
        )

        screen.blit(text, (85, 230))
        screen.blit(final_score, (115, 300))
        screen.blit(restart_text, (85, 360))

    pygame.display.update()

pygame.quit()
sys.exit()