import pygame
import random

pygame.init()

# Game screen setup
pygame.display.set_caption("2D Game")
screen = pygame.display.set_mode((800, 600))

# Load images
bg = pygame.image.load("bg.png")
bg10 = pygame.image.load("bg10.png")
player = pygame.image.load("rocket.png")
player = pygame.transform.scale(player, (50, 50))
speaker_on_image = pygame.image.load("speaker_on.png")
speaker_on_image = pygame.transform.scale(speaker_on_image, (50, 50))
speaker_off_image = pygame.image.load("speaker_off.png")
speaker_off_image = pygame.transform.scale(speaker_off_image, (50, 50))
meteorite = pygame.image.load("meteorite.png")
meteorite = pygame.transform.scale(meteorite, (30, 60))


button_images = {
    "speaker_on": speaker_on_image,
    "speaker_off": speaker_off_image
}
button_image = button_images["speaker_on"]  # Change to the desired initial state

# Player position
player_x = 375
player_y = 275

# Obstacle properties
obstacle_radius = 10
obstacle_color = (255, 0, 0)
obstacle_x = random.randint(obstacle_radius, 800 - obstacle_radius)
obstacle_y = 0
obstacle_speed = 2

#Meteorite Setup
meteorite_x = random.randint(obstacle_radius, 800 - obstacle_radius)
meteorite_y = 0

# Coin setup
coin = pygame.image.load("coin.png")
coin = pygame.transform.scale(coin, (50, 50))
coin_radius = 25
coin_color = (255, 215, 0)
coins = []
score = 0

# Status for movement
moving_up = False
moving_down = False
moving_left = False
moving_right = False

# Font setup
font = pygame.font.Font(None, 36)

# Game over state
game_over = False

# Background music setup
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.set_volume(0.1)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Start playing the music (-1 for continuous loop)

# Toggle music button setup
button_width = 100
button_height = 50
toggle_button = pygame.Rect(740, 10, button_width, button_height)
button_color = (0, 255, 0)
button_text = "Pause"
button_text_rect = font.render(button_text, True, (255, 255, 255)).get_rect(center=toggle_button.center)

def handle_input_events():
    global w_pressed, a_pressed, s_pressed, d_pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                w_pressed = True
            elif event.key == pygame.K_a:
                a_pressed = True
            elif event.key == pygame.K_s:
                s_pressed = True
            elif event.key == pygame.K_d:
                d_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_pressed = False
            elif event.key == pygame.K_a:
                a_pressed = False
            elif event.key == pygame.K_s:
                s_pressed = False
            elif event.key == pygame.K_d:
                d_pressed = False

def update_player_position():
    global pos_player_x, pos_player_y
    if w_pressed:
        pos_player_y -= 5
    if a_pressed:
        pos_player_x -= 5
    if s_pressed:
        pos_player_y += 5
    if d_pressed:
        pos_player_x += 5
        
def restart_game():
    global player_x, player_y, obstacle_x, obstacle_y, game_over, obstacle_speed, score, meteorite_y
    player_x = 375
    player_y = 275
    obstacle_x = random.randint(obstacle_radius, 800 - obstacle_radius)
    obstacle_y = 0
    obstacle_speed = 2
    score = 0
    meteorite_y = 0
    game_over = False

def toggle_music():
    global button_image
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        button_image = button_images["speaker_off"]
    else:
        pygame.mixer.music.unpause()
        button_image = button_images["speaker_on"]

def generate_coin():
    x = random.randint(coin_radius, 800 - coin_radius)
    y = random.randint(coin_radius, 600 - coin_radius)
    coins.append((x, y))

def check_collision(player_rect, coin_rect):
    return player_rect.colliderect(coin_rect)

def render_button_image():
    screen.blit(button_image, toggle_button)


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moving_up = True
            elif event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_s:
                moving_down = True
            elif event.key == pygame.K_d:
                moving_right = True

        # Keyup events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moving_up = False
            elif event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_s:
                moving_down = False
            elif event.key == pygame.K_d:
                moving_right = False

        # Mouse click event for restart button
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                restart_game()

        # Mouse click event for toggle button
        if event.type == pygame.MOUSEBUTTONDOWN and toggle_button.collidepoint(event.pos):
            toggle_music()

    if not game_over:
        # Player movement
        if moving_up and player_y >= 5:
            player_y -= 5
        if moving_left and player_x >= 5:
            player_x -= 5
        if moving_down and player_y <= 545:
            player_y += 5
        if moving_right and player_x <= 745:
            player_x += 5

        # Update obstacle position
        obstacle_y += obstacle_speed
        meteorite_y += obstacle_speed

        # Check for collision with obstacle
        player_rect = player.get_rect(center=(player_x+25, player_y+25))
        obstacle_rect = pygame.Rect(obstacle_x - obstacle_radius, obstacle_y - obstacle_radius,
                                    obstacle_radius * 2, obstacle_radius * 2)
        meteorite_rect = pygame.Rect(meteorite_x, meteorite_y,30, 60)
        if player_rect.colliderect(obstacle_rect) or player_rect.colliderect(meteorite_rect):
            game_over = True

        # Check if obstacle passed the player
        if obstacle_y > 600 + obstacle_radius:
            obstacle_y = 0
            obstacle_x = random.randint(obstacle_radius, 800 - obstacle_radius)
            obstacle_radius = random.randint(10, 30)
        if meteorite_y > 1000:
            meteorite_y = 0
            meteorite_x = random.randint(15, 800 - 15)

    if score < 10:
        screen.blit(bg, (0, 0))
    else:
        screen.blit(bg10, (0, 0))
    screen.blit(player, (player_x, player_y))
    screen.blit(meteorite, (meteorite_x, meteorite_y))
    # Draw coins
    for coin_pos in coins:
        screen.blit(coin, (coin_pos[0] - coin_radius, coin_pos[1] - coin_radius))
    player_rect = player.get_rect(center=(player_x + 75, player_y + 75))

    # Check for collision with coins
    for coin_pos in coins:
        coin_rect = pygame.Rect(coin_pos[0] + coin_radius, coin_pos[1] + coin_radius, coin_radius * 2, coin_radius * 2)
        if check_collision(player_rect, coin_rect):
            coins.remove(coin_pos)
            score += 1

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.draw.circle(screen, obstacle_color, (obstacle_x, int(obstacle_y)), obstacle_radius)

    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(400, 300))
        screen.blit(game_over_text, game_over_text_rect)

        # Restart button
        restart_button = pygame.Rect(325, 350, 150, 50)
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        restart_text = font.render("Restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        screen.blit(restart_text, restart_text_rect)

    # Toggle button
    render_button_image()


    pygame.display.update()
    # Generate new coin
    if len(coins) < 3:
        generate_coin()

    obstacle_speed += 0.001
pygame.quit()