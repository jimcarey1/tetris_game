import pygame
from pygame.locals import *
import random
from typing import Tuple, List
import time

pygame.init()

screen = pygame.display.set_mode((300, 480))
pygame.display.set_caption("Tetris game")

clock = pygame.time.Clock()

running = True
BLOCK_SIZE = 15

def draw_board(screen: pygame.Surface)->None:
    w, h = screen.get_size()
    #drawing vertical lines
    for i in range(0, w, BLOCK_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, h))
    #drawing horizontal lines
    for i in range(0, h, BLOCK_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (0, i), (w, i))

class TetrisBlock(pygame.Rect):
    def __init__(self, position:Tuple[int, int]):
        super().__init__(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
        self.moving = True
    
        
class TetrisGame:
    def __init__(self):
        self.vector = [[0]*300 for i in range(480)] #480*300 matrix
        self.tetris_step:List[TetrisBlock] = []
    
    @staticmethod
    def get_block_on_direction(direction:str, source_position:Tuple[int, int]):
        x, y = source_position
        if(direction=='up'):
            position = TetrisBlock((x, y-15))
        if(direction=='down'):
            position = TetrisBlock((x, y+15))
        if(direction=='left'):
            position = TetrisBlock((x-15, y))
        if(direction=='right'):
            position = TetrisBlock((x+15, y))
        return position

    def generate_tetris_step_pos(self)->None:
        tetris_step:List[TetrisBlock] = []
        directions = ['up', 'down', 'left', 'right']
        position = TetrisBlock((random.choice(range(0, 300, BLOCK_SIZE)), -15))
        tetris_step.append(position)
        while len(tetris_step) < 4:
            index = random.choice(range(0, len(tetris_step)))
            direction = random.choice(directions)
            position = self.get_block_on_direction(direction, tetris_step[index].topleft)
            tetris_step.append(position)
        self.tetris_step = tetris_step
    
    def update_tetris_step(self):
        if not any([block.y >= (480-15) for block in self.tetris_step]):
            for block in self.tetris_step:
                block.y += BLOCK_SIZE
            else:
                self.moving = False
    
    def draw_tetris_step(self):
        for block in self.tetris_step:
            pygame.draw.rect(screen, (255, 0, 0), block)
    
    def update_block_vector(self):
        if not self.moving:
            pass


game = TetrisGame()    
game.generate_tetris_step_pos()

while running:
    screen.fill((255, 255, 255))
    #Drawing our tetris board.
    draw_board(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    game.update_tetris_step()
    game.draw_tetris_step()
    time.sleep(0.2)
    pygame.display.flip()
