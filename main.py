import pygame
import random

from pygame.locals import * 

"""
Clamp the given value

x    {number} - The value to clamp
min_ {number} - The minimum value
max_ {number} - The maximum value
"""
def clamp(x, min_, max_):
  return max(min_, min(x, max_))


class Sand:
  """
  Sand class
  
  world       {World}  - The world containing the sand element
  x           {number} - The x coord
  y           {number} - The y coord
  max_updates {number} - The max number of updates of the element
  """
  def __init__(self, world, x, y, max_updates):
    self.world = world
    self.x = x
    self.y = y 
    
    self.max_updates = max_updates
    self.updates = 0
  
  """
  Move the sand element to the given coords
  
  x {number} - The x coord
  y {number} - The y coord
  """
  def move_to(self, x, y):
    self.x = x
    self.y = y
    
  """
  Remove the element from the world
  """
  def destroy(self):
    for i, element in enumerate(self.world.world):
      if element is self:
        self.world.world.pop(i)
  
  """
  Update the sand coords
  """
  def update(self):
    ny = self.y + 1 # new y value
    my = self.y + 2 # next iteration y value
    
    bottom = self.world.is_empty(self.x, ny)
    bottom_left = self.world.is_empty(self.x - 1, ny)
    bottom_right = self.world.is_empty(self.x + 1, ny)
        
    if bottom and self.world.in_boundaries(self.x, my):
      self.move_to(self.x, ny)
    
    elif bottom_left and self.world.in_boundaries(self.x - 1, my):
      self.move_to(self.x - 1, ny)
      
    elif bottom_right and self.world.in_boundaries(self.x + 1, my):
      self.move_to(self.x + 1, ny)
    
    if self.updates == self.max_updates:
      self.destroy()
    
    self.updates += 1

  """
  Draw the sand into the surface
  
  surf {pygame.Surface} - The surface
  """
  def draw(self, surf):
    color = (235, 168, 52)
    rect = pygame.Rect(self.x, self.y, 1, 1)
    
    pygame.draw.rect(surf, color, rect)
    

class World:
  """
  World class
  
  size          {(number, number)} - The size of the window, in scaled pixels
  scale         {number}           - The scale of the pixels 
  fps           {number}           - The amount of frames per second
  destroy_delay {number}           - Time after which we destroy each element
  """
  def __init__(self, size, scale, fps, destroy_delay):
    self.scale = scale
    self.size = size
    self.width = self.size[0]
    self.height = self.size[1]

    self.fps = fps
    self.destroy_delay = destroy_delay
    
    self.win = None
    self.surf = pygame.Surface(size)
    self.clock = pygame.time.Clock()
    
    self.world = []
    
  """
  Check if the coords are in the surface boundaries
  
  x {number} - The x coord
  y {number} - The y coord
  """
  def in_boundaries(self, x, y):
    return 0 <= x and x <= self.width and 0 <= y and y <= self.height
    
  """
  Check if there is an element at the given coords
  
  x {number} - The x coord
  y {number} - The y coord
  """
  def is_empty(self, x, y):
    for element in self.world:
      if element.x == x and element.y == y:
        return False
      
    return True
  
  """
  Draw a batch of sand with a random number of grains
  
  x                {number}       - The x coord
  y                {number}       - The y coord
  size             {number}       - The total size of the rect
  empty_percentage {number ]0-1]} - The amount of white space
  """
  def add_batch(self, x, y, size = 20, empty_percentage = .9):
    x_range_min = clamp(x - size // 2, 0, self.width - 1)
    x_range_max = clamp(x + size // 2, 0, self.width - 1)
    
    y_range_min = clamp(y - size // 2, 0, self.height - 1)
    y_range_max = clamp(y + size // 2, 0, self.height - 1)
    
    for x in range(x_range_min, x_range_max):
      for y in range(y_range_min, y_range_max):
        if random.random() > empty_percentage:
          self.world.append(Sand(self, x, y, self.destroy_delay * self.fps))
        
    
  """
  Fill the surface with the given color
  
  color {(number, number, number)} - The rgb color
  """
  def fill_surf(self, color):
    rect = pygame.Rect(0, 0, self.width, self.height)
    pygame.draw.rect(self.surf, color, rect)
    
  """
  Update method
  """
  def update(self):
    # Update the world elements
    for element in self.world:
      element.update()
    
  """
  Get the mouse position on the scaled surface
  """
  def get_scaled_mouse_pos(self):
      x, y = pygame.mouse.get_pos()
      
      # Scale the coords
      return x // self.scale, y // self.scale
  
  """
  Draw all the necessary elements on the surfcae
  """
  def draw(self):
    self.fill_surf((255, 255, 255))
    
    for element in self.world:
      element.draw(self.surf)
      
  """
  Start the pygame loop
  """
  def start(self):
    # Make the pygame window sized at the pixels scale
    self.win = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
  
    # Game loop
    while True:
      # ----- EVENTS
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          return

        if event.type == pygame.MOUSEBUTTONDOWN:
          self.add_batch(*self.get_scaled_mouse_pos())
      
      # ----- MAIN METHODS
      self.update()
      self.draw()
      
      # ----- OPTIONS
      
      # Scale the window
      self.win.blit(pygame.transform.scale(self.surf, self.win.get_rect().size), (0, 0))
      
      # Set the frame rate
      self.clock.tick(self.fps)
      
      # Update the window
      pygame.display.update()
      
      
if __name__ == '__main__':
  size = (50, 50)        # scaled pixels size
  scale = 16             # pixel scale
  fps = 60               # frames per second
  sand_destory_delay = 4 # in seconds
  
  w = World(size, scale, fps,sand_destory_delay)
  w.start()