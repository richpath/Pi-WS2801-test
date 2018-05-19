import pygame
import random
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
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

# Lists for LED numbers - this essentially maps the LEDs on the large display box to each 10x10 area of the sketch window
led = [[199,198,197,196,195,194,193,192,191,190,189,188,187,186,185,184,183,182,181,180],
       [160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179],
       [159,158,157,156,155,154,153,152,151,150,149,148,147,146,145,144,143,142,141,140],
       [120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139],
       [119,118,117,116,115,114,113,112,111,110,109,108,107,106,105,104,103,102,101,100],
       [80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99],
       [79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60],
       [40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59],
       [39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20],
       [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]]

# create an array of colors for random color choice
clrs = [RED, ORANGE, GOLD, YELLOW, GREENYELLOW, GREEN, DKGREEN, CYAN, BLUE, DARKVIOLET, MAGENTA]

# add boolean for joystick button, to prevent multiple firings when held in pressed position
bten = False

# Configure the total number of LEDs that the WS2801 library sends the data to
PIXEL_COUNT = 200

# The WS2801 library makes use of the BCM pin numbering scheme.
# Specify a software SPI connection for Raspberry Pi on the following pins:
PIXEL_CLOCK = 18
PIXEL_DOUT = 23

# a class that initializes and draws a square
class square:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.clr = clrs[0]
        self.width = 10
    def draw(self):
        pygame.draw.rect(screen, self.clr, [self.x, self.y, self.width, self.width], 0)
 
# Setup
pygame.init()
 
# Set the width and height of the program window [width,height]
size = [200, 100]
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("LED control test")

# Initiate the LEDs
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)

# Create a square object
sq1 = square(0,0)

# Count the joysticks the computer has
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print("Error - didn't find any joysticks.")
else:
    # Use joystick #0 and initialize it
    print("Joystick found and initialized!")
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

# Clear all the pixels to turn them off.
pixels.clear()
pixels.show()  # Make sure to call show() after changing any pixels!

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    # --- Game Logic  
 
    # --- Drawing Code
    # As long as there is a joystick
    if joystick_count != 0:
    
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0
        horiz_axis_0 = my_joystick.get_axis(0)
        vert_axis_1 = my_joystick.get_axis(1)
        hat = my_joystick.get_hat(0)
        clrbtn = my_joystick.get_button(10)
    
        # Move x according to the axis. We multiply by 10 to speed up the movement.
        # Convert to an integer because we can't draw at pixel 3.5, just 3 or 4.
        sq1.x = sq1.x + int(horiz_axis_0 * 10)
        if sq1.x > 200-width:
            sq1.x = 200-width
        elif sq1.x < 0:
            sq1.x = 0
        sq1.y = sq1.y + int(vert_axis_1 * 10)
        if sq1.y > 100-width:
            sq1.y = 100-width
        elif sq1.y < 0:
            sq1.y = 0
        # Use the verticle switch on the hat button to reduce or increase square size
        sq1.width = sq1.width + (hat[1]*10)
        if sq1.width<10:
            sq1.width=10
        elif sq1.width>100:
            sq1.width=100
        # Change object to a random color in the color array if left joystick is pressed as a button
        if clrbtn==1 and bten==False:
            cnum = random.randint(0,len(clrs)-1)
            sq1.clr = clrs[cnum]
            bten = True
        elif clrbtn==0:
            bten = False
        
    # Clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    
    # draw the square object on the screen
    sq1.draw()
 
    # Go ahead and update the screen to display what's been drawn.
    pygame.display.flip()
    
    # Get colors from specific grid points on screen to send to each led
    for r in range (0,9):
        for c in range (0,19):
            # the pygame function below returns an RGB color list for a pixel on the surface, identified by the coordinates
            ledclr = screen.get_at(((c*10)+5,(r*10)+5))
            # this sets the number of the LED in the strand, based on the led array at the beginning
            px = led[r][c]
            # set the specific led to the pixel screen color - since these LEDs are GBR, the order of values is changed
            pixels.set_pixel_rgb(px, ledclr[1], ledclr[2], ledclr[0])
    
    # Show the LEDs
    pixels.show()
    
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
