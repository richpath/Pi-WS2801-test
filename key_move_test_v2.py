import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DKGREEN = (0, 100, 0)
GREENYELLOW = (173, 255, 47)
CYAN = (0, 255, 255)
DARKVIOLET = (148, 0, 211)
MAGENTA = (255, 0, 255)
GOLD = (255, 215, 0)

# create array for a random color choice
clrs = [RED, ORANGE, GOLD, YELLOW, GREENYELLOW, GREEN, DKGREEN, CYAN, BLUE, DARKVIOLET, MAGENTA]
clrnum = 0

# boolean for joystick button press tracking
b10press = False

# a class that initializes and draws a square
class square:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.clr = RED
    self.width = 10
  def draw(self):
    pygame.draw.rect(screen, self.clr, [self.x, self.y, self.width, self.width], 0)
 
# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [200, 100]
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("LED control test")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Create a square object
sq1 = square(0,0)
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key
 
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
            elif event.key == pygame.K_SPACE:
                c = random.randint(0,len(clrs)-1)
                print(c)
                sq1.clr = clrs[c]
            elif event.key == pygame.K_MINUS:
                sq1.width = sq1.width - 5
                if sq1.width<10:
                  sq1.width=10                
            elif event.key == pygame.K_EQUALS:
                sq1.width = sq1.width + 5
                if sq1.width>100:
                  sq1.width=100                 

            # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
 
    # --- Game Logic
 
    # Move the object according to the speed vector.
    sq1.x = sq1.x + x_speed
    sq1.y = sq1.y + y_speed   
 
    # --- Drawing Code
        
    # First, clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    sq1.draw()
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()