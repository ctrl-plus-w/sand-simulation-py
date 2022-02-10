import sys

import pygame
from pygame.locals import *

class Sand:
  """
  Sand class
  
  world {World}  - The world containing the sand element
  x     {number} - The x coord
  y     {number} - The y coord
  """
  def __init__(self, world, x, y, v):
    self.world = world
    self.x = x
    self.y = y
    self.v = v
  
  def show_coords(self):
    print(self.x, self.y)
  
  """
  Move the sand element to the given coords
  
  x {number} - The x coord
  y {number} - The y coord
  """
  def move_to(self, x, y):
    self.x = x
    self.y = y
  
  """
  Update the sand coords
  """
  def update(self):
    new_x, new_y = self.x + self.v[0], self.y + self.v[1]

    if self.v[0] != 0 and self.v[1] != 0:
      m = self.v[1] / self.v[0]

      # x takes all values of the velocity x
      for v_x in range(1, self.v[0] + 1):
        v_y = round(m * v_x)
        next_v_y = round(m * (v_x + 1))
        
        x = self.x + v_x
        y = self.y + v_y
        next_y = self.y + next_v_y
        
        in_boundaries = self.world.is_valid(x, y)
        is_next_valid = self.world.is_valid(x + 1, next_y)
        is_final_coords = x == new_x and y == new_y

        if in_boundaries and (not is_next_valid or is_final_coords):
          self.move_to(x, y)
          return

    # element going horizontally (straight) -> y = new_y
    elif self.v[1] == 0:
      for x in range(self.x, new_x + 1):
        in_boundaries = self.world.is_valid(x, new_y)
        is_next_valid = self.world.is_valid(x + 1, new_y)
        is_final_coords = x == new_x

        if in_boundaries and (not is_next_valid or is_final_coords):
          self.move_to(x, new_y)
          return

    # element going down (straight) -> x = new_x
    elif self.v[0] == 0:
      for y in range(self.y, new_y + 1):
        in_boundaries = self.world.in_boundaries(new_x, y)
        is_next_valid = self.world.is_valid(new_x, y + 1)
        is_final_coords = y == new_y

        if in_boundaries and (not is_next_valid or is_final_coords):
          self.move_to(new_x, y)
          return
      

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
  
  size  {(number, number)} - The size of the window, in scaled pixels
  scale {number}           - The scale of the pixels 
  """
  def __init__(self, size, scale):
    self.scale = scale
    self.size = size
    self.width = self.size[0]
    self.height = self.size[1]
    
    self.win = None
    self.surf = pygame.Surface(size)
    self.clock = pygame.time.Clock()
    
    self.world = []
    
    self.world.append(Sand(self, self.width // 2, 10, (0, 1)))

    self.holding = False    
    
  """
  Check if there is any element at the given coords and that the coords are in the surface boundaries
  
  x {number} - The x coord
  y {number} - The y coord
  """
  def is_valid(self, x, y):
    if not self.in_boundaries(x, y) or not self.is_empty(x, y):
      return False

    return True
  
  """
  Check if the coords are in the surface boundaries
  We remove 1 from the width and height because coords starts at 0
  
  x {number} - The x coord
  y {number} - The y coord
  
  """
  def in_boundaries(self, x, y):
    return 0 <= x < self.width and 0 <= y < self.height
    
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
    
    # Add sand when holding the mouse
    if self.holding:
      x, y = pygame.mouse.get_pos()
      
      # Scale the coords
      x = x // self.scale
      y = y // self.scale

      # If the coords are in the boundaries and there is no element at the coords
      if self.in_boundaries(x, y) and self.is_empty(x, y):
        self.world.append(Sand(self, x, y, (0, 1)))
      
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
          self.holding = True

        if event.type == pygame.MOUSEBUTTONUP:
          self.holding = False
      
      # ----- MAIN METHODS
      self.update()
      self.draw()
      
      # ----- OPTIONS
      
      # Scale the window
      self.win.blit(pygame.transform.scale(self.surf, self.win.get_rect().size), (0, 0))
      
      # Set the frame rate
      self.clock.tick(60)
      
      # Update the window
      pygame.display.update()
      
      
if __name__ == '__main__':
  size = (150, 75)
  scale = 8
  
  w = World(size, scale)
  w.start()