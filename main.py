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
    
        
class TetrisGame:
    def __init__(self):
        self.vector:List[List[int]] = [[0]*300 for i in range(480)] #480*300 matrix
        self.tetris_step:List[TetrisBlock] = []
        self.tetris_blocks: List[List[TetrisBlock]] = []
        self.moving = True
    
    @staticmethod
    def get_block_on_direction(direction:str, source_position:Tuple[int, int])->TetrisBlock:
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
        self.tetris_blocks.append(tetris_step)
        self.moving = True
    
    def update_tetris_step(self)->None:
        if not any([block.y >= (480-15) for block in self.tetris_step]):
            for block in self.tetris_step:
                block.y += BLOCK_SIZE
        else:
            self.moving = False
    
    def draw_tetris_step(self)->None:
        for step in self.tetris_blocks:
            for block in step:
                pygame.draw.rect(screen, (255, 0, 0), block)
    
    def _get_block_coordinates(self, coord:Tuple[int, int])->Tuple[int, int]:
        (x, y) = (coord[1], coord[0])
        x = 0 if x == 0 else (x+1)//15
        y = 0 if y == 0 else (y+1)//15
        return (x, y)

    def update_block_vector(self)->None:
        if not self.moving:
            for block in self.tetris_step:
                x, y = self._get_block_coordinates(block.topleft)
                self.vector[x][y] = 1


game = TetrisGame()    
game.generate_tetris_step_pos()

while running:
    screen.fill((255, 255, 255))
    #Drawing our tetris board.
    draw_board(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game.moving == False:
        game.generate_tetris_step_pos()
    game.update_tetris_step()
    game.draw_tetris_step()
    game.update_block_vector()

    time.sleep(0.2)
    pygame.display.flip()
