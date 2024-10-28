# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

x_direction = -1
y_direction = 1

velocity = pygame.Vector2(-1, 1)
velocity = velocity.normalize()

boundary_rad = 300
player_rad = 10

screen_center = (screen.get_width()/2, screen.get_height()/2)
screen_center_x = screen.get_width() / 2
screen_center_y = screen.get_height() / 2

player_pos = pygame.Vector2(screen.get_width() / 2 + 100, screen.get_height() / 2 + 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    
    pygame.draw.circle(screen, "white",(screen_center_x, screen_center_y), boundary_rad )

    pygame.draw.circle(screen, "red", player_pos, player_rad)

    
    #dist_center = math.sqrt((screen_center_x - player_pos.x) * (screen_center_x - player_pos.x) + (screen_center_y - player_pos.y) * (screen_center_y - player_pos.y))
    dist_center = player_pos.distance_to(screen_center)


    if dist_center + player_rad >= boundary_rad:
        # Find the normal vector at the point of collision (from the center to the ball position)
        normal = (player_pos - (screen_center_x, screen_center_y)).normalize()
        # Reflect the velocity vector along the normal
        velocity = velocity.reflect(normal)

    # Movement
    player_pos += velocity * 200 * dt




    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
