import pygame
import os

# Load the game images for the bird
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("/kaggle/input/flappy-bird-game-dataset", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("/kaggle/input/flappy-bird-game-dataset", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("/kaggle/input/flappy-bird-game-dataset", "bird3.png")))]

# Bird class
class Bird:
    IMGS = BIRD_IMGS  # List of bird images for animation
    MAX_ROTATION = 25  # Max tilt angle when falling
    ROT_VEL = 20  # Rotation velocity
    ANIMATION_TIME = 5  # Time between animation frames

    def __init__(self, x, y):
        # Initialization of bird's position and physics variables
        self.x = x  # Horizontal position of the bird
        self.y = y  # Vertical position of the bird
        self.tilt = 0  # Rotation angle
        self.tick_count = 0  # Time counter for jump physics
        self.vel = 0  # Vertical velocity (initially zero)
        self.height = self.y  # Starting height of the bird
        self.img_count = 0  # Counter to cycle through bird images
        self.img = self.IMGS[0]  # Default bird image

    def jump(self):
        # Make the bird jump by setting a negative vertical velocity
        self.vel = -10.5  # Set jump velocity
        self.tick_count = 0  # Reset the time counter
        self.height = self.y  # Reset the height to current position

    def move(self):
        # Update bird's movement and position
        self.tick_count += 1  # Increment the time counter
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2  # Calculate displacement using physics formula

        if d >= 16:  # Terminal velocity condition
            d = 16  # Limit displacement to avoid too fast falling
        if d < 0:  # If moving upwards
            d -= 2  # Slight downward adjustment when moving up

        self.y = self.y + d  # Update bird's position

        # Check if the bird has hit the peak of the jump or needs to start tilting down
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION  # Limit upward tilt
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL  # Rotate the bird to simulate falling

    def draw(self, win):
        # Animate the bird by cycling through the images
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0  # Reset the animation cycle

        # If bird is falling too much, set it to the first frame of animation
        if self.tilt <= -80:
            self.img = self.IMGS[0]
            self.img_count = self.ANIMATION_TIME * 2  # Speed up animation

        # Rotate and draw the bird image at the current position
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)  # Draw rotated image at the correct position

    def get_mask(self):
        # Get a mask for collision detection (used for pixel-perfect collision)
        return pygame.mask.from_surface(self.img)