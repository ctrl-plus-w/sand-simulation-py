# coding: utf-8

"""
Preuve de concept de la simulation de chute de sable.
Cet algorithme est basé sur le système d'Automate Cellulare.

voir:
  - https://fr.wikipedia.org/wiki/Automate_cellulaire (EN FRANCAIS)
  - https://en.wikipedia.org/wiki/Cellular_automaton (EN ANGLAIS)
"""

import pygame
import random

from pygame.locals import * 

"""
Retourne une valeur comprise dans l'inverval donné (voir: https://en.wikipedia.org/wiki/Clamping_(graphics))

Exemples:
clamp(0, 25, 100) = 25
clamp(150, 25, 100) = 100
clamp(75, 25, 100) = 75

val  {number} - La valeur à vérifier 
min_ {number} - La valeur minimum
max_ {number} - La valeur maximum

Revoie un nombre
"""
def clamp(val: int, min_: int, max_: int) -> int:
  return max(min_, min(val, max_))


class Salt:
  """
  Classe d'un grain de sel
  
  world       {World}  - Le monde contenant l'instance
  x           {number} - La position x
  y           {number} - La position y
  max_updates {number} - Le nombre maximum de mise à jours de l'instance
  """
  def __init__(self, world, x, y, max_updates):
    self.world = world
    self.x = x
    self.y = y 
    
    self.max_updates = max_updates
    self.updates = 0
  
  
  """
  Déplace le sel aux coordonées données
  
  x {number} - La position x
  y {number} - La position y
  """
  def move_to(self, x: int, y: int) -> None:
    self.x = x
    self.y = y
    
    
  """
  Retire l'instance du monde
  """
  def destroy(self) -> None:
    # On boucle dans chaque élément du monde, "i" étant l'index, "element" étant l'élément
    for i, element in enumerate(self.world.world):
      
      # On regarde si l'élément est égal à l'instance actuelle
      if element is self:
        self.world.world.pop(i)
  
  
  """
  Met à jour l'instance
  """
  def update(self) -> None:
    self.updates += 1

    # Si le nombre de mises à jour est atteint, on détruit l'instance.
    if self.updates == self.max_updates:
      self.destroy()
      return

    ny = self.y + 1 # La nouvelle valeur de y
    my = self.y + 2 # La valeur de y de la mise à jour suivante
    
    # On regarde si des éléments sont présents dans les trois cases en dessous
    # On vérifie chaque conditions une à une pour avoir le minimum de calculs possibles 

    # Case en dessous (x, y-1)
    if self.world.is_empty(self.x, ny) and self.world.in_boundaries(self.x, my):
      self.move_to(self.x, ny)
      return

    # Case en dessous à gauche (x-1, y)    
    if self.world.is_empty(self.x - 1, ny) and self.world.in_boundaries(self.x - 1, my):
      self.move_to(self.x - 1, ny)
      return
    
    # Case de dessous à droite (x+1, y)
    if self.world.is_empty(self.x + 1, ny) and self.world.in_boundaries(self.x + 1, my):
      self.move_to(self.x + 1, ny)
      return
    

  """
  Dessine le grain de sel sur la surface
  
  surf {pygame.Surface} - La surface
  """
  def draw(self, surf) -> None:
    color = (200, 200, 200)
    rect = pygame.Rect(self.x, self.y, 1, 1)
    
    pygame.draw.rect(surf, color, rect)
    

class World:
  """Classe du monde
  
  size          {(number, number)} - La taille de la surface, en pixels à l'ÉCHELLE
  scale         {number}           - L'échelle d'un pixel (multiplicateur)
  fps           {number}           - Le nombre d'images par seconde
  destroy_delay {number}           - Le temps après lequel un élément doit être détruit
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
  Vérifie si les coordonées sont sur la surface
  
  x {number} - La position x
  y {number} - La position y
  """
  def in_boundaries(self, x: int, y: int) -> bool:
    return 0 <= x and x <= self.width and 0 <= y and y <= self.height
    
    
  """
  Vérifie si un élément existe aux coordonées données
  
  x {number} - La position x
  y {number} - La position y
  """
  def is_empty(self, x: int, y: int) -> bool:
    for element in self.world:
      if element.x == x and element.y == y:
        return False
      
    return True
  
  
  """
  Dessine un groupe de grains de sel avec un nombre aléatoire de grains
  
  x                {number}       - La position x
  y                {number}       - La position y
  size             {number}       - La taille (largeur et longueur) du rectangle
  empty_percentage {number ]0-1]} - Le pourcentage de vide
  """
  def add_batch(self, x: int, y: int, size: int = 20, empty_percentage: int = .9) -> None:
    x_range_min = clamp(x - size // 2, 0, self.width - 1)
    x_range_max = clamp(x + size // 2, 0, self.width - 1)
    
    y_range_min = clamp(y - size // 2, 0, self.height - 1)
    y_range_max = clamp(y + size // 2, 0, self.height - 1)
    
    for x in range(x_range_min, x_range_max):
      for y in range(y_range_min, y_range_max):
        if random.random() > empty_percentage and self.is_empty(x, y):
          self.world.append(Salt(self, x, y, self.destroy_delay * self.fps))
        
    
  """
  Remplie la surface avec la couleur donnée
  
  color {(number, number, number)} - La couleur rgb
  """
  def fill_surf(self, color: tuple) -> None:
    rect = pygame.Rect(0, 0, self.width, self.height)
    pygame.draw.rect(self.surf, color, rect)
    
    
  """
  Méthode de mise à jour
  """
  def update(self) -> None:
    # Update the world elements
    for element in self.world:
      element.update()
    
    
  """
  Récupère la position de la souris à l'échelle de la surface
  """
  def get_scaled_mouse_pos(self) -> tuple:
      x, y = pygame.mouse.get_pos()
      
      # Scale the coords
      return x // self.scale, y // self.scale
  
  
  """
  Dessine tous les éléments du monde
  """
  def draw(self) -> None:
    self.fill_surf((0, 0, 0))
    
    for element in self.world:
      element.draw(self.surf)
      
      
  """
  Méthode principale
  """
  def start(self) -> None:
    # On crée une fenêtre à la taille donnée
    self.win = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
  
    # Boucle du jeux
    while True:
      # ----- ÉVÉNEMENTS
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          return

        if event.type == pygame.MOUSEBUTTONDOWN:
          self.add_batch(*self.get_scaled_mouse_pos())
      
      # ----- MÉTHODES PRINCIPALES
      self.update()
      self.draw()
      
      # ----- OPTIONS
      
      # On change la taille des pixels
      self.win.blit(pygame.transform.scale(self.surf, self.win.get_rect().size), (0, 0))
      
      # On défini le taux d'images par seconde
      self.clock.tick(self.fps)
      
      # On actualise la fenêtre
      pygame.display.update()
      

"""
Dans le cas où ce fichier est utilisé comme un module (pour utiliser les classes),
ces lignes sont requises.
"""
if __name__ == '__main__':
  size = (50, 50)        # taille de la surface, à l'échelle
  scale = 16             # taille d'un pixel
  fps = 60               # images par seconde
  destroy_delay = 2      # temps de destruction d'un élément (en seconde)
  
  w = World(size, scale, fps,destroy_delay)
  w.start()