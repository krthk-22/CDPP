import pygame
import random
import sys

pygame.init()

# Constants
NUM_TILES = 4
WINDOW_SIZE = NUM_TILES * 100
TILE_SIZE = 100
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Initialize the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("15 Puzzle Variant")

font = pygame.font.Font(None, 36)

dxn = ['up', 'right', 'left', 'down']
move_num = {'up': 0, 'right': 1, 'left': 2, 'down': 3}


class Puzzle15:
    def __init__(self):
        self.board = [[i + j * NUM_TILES for i in range(1, NUM_TILES + 1)] for j in range(0, NUM_TILES)]
        self.empty_row, self.empty_col = NUM_TILES - 1, NUM_TILES - 1
        self.solved_state = self.board
        self.history = []
        self.rev = False
        self.shuffled = 0

    def shuffle(self):
        for _ in range(1000):
            possible_moves = self.get_possible_moves()
            direction = random.choice(possible_moves)
            self.move(direction)
            self.history = []
        self.shuffled = 1

    def get_possible_moves(self):
        possible_moves = []
        if self.empty_row > 0:
            if (self.empty_row + self.empty_col) % 2 == 1:
                possible_moves.append('down')
        if self.empty_row < NUM_TILES - 1:
            if (self.empty_row + self.empty_col) % 2 == 1:
                possible_moves.append('up')
        if self.empty_col > 0:
            if (self.empty_row + self.empty_col) % 2 == 0:
                possible_moves.append('right')
        if self.empty_col < NUM_TILES - 1:
            if (self.empty_row + self.empty_col) % 2 == 0:
                possible_moves.append('left')
        return possible_moves

    def draw_board(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                num = self.board[row][col]
                if num == NUM_TILES*NUM_TILES and (row + col) % 2 == 0:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif num == NUM_TILES*NUM_TILES and (row + col) % 2 == 1:
                    pygame.draw.rect(screen, GREEN, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif (row + col) % 2 == 0:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render(str(num), True, BLACK)
                    text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)
                elif (row + col) % 2 == 1:
                    pygame.draw.rect(screen, GREEN, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render(str(num), True, BLACK)
                    text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)

        pygame.display.flip()

    def print_nice(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                if row != col and (row + col) % 2 == 0:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif row != col and (row + col) % 2 == 1:
                    pygame.draw.rect(screen, GREEN, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif row == col == 0:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render('N', True, BLACK)
                    text_rect = text.get_rect(
                        center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)
                elif row == col == 1:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render('I', True, BLACK)
                    text_rect = text.get_rect(
                        center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)
                elif row == 2 == col:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render('C', True, BLACK)
                    text_rect = text.get_rect(
                        center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)
                elif row == 3 == col:
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render('E!', True, BLACK)
                    text_rect = text.get_rect(
                        center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)

        pygame.display.flip()

    def move(self, direction):
        # if direction in self.get_possible_moves() or self.rev == True:
        if direction in self.get_possible_moves() or self.rev:

            if not self.rev:
                self.history.append(direction)
            
            new_row, new_col = self.empty_row, self.empty_col

            if direction == 'up':
                new_row += 1
            elif direction == 'down':
                new_row -= 1
            elif direction == 'left':
                new_col += 1
            elif direction == 'right':
                new_col -= 1
            else:
                return

            self.board[self.empty_row][self.empty_col], self.board[new_row][new_col] = \
                self.board[new_row][new_col], self.board[self.empty_row][self.empty_col]
            self.empty_row, self.empty_col = new_row, new_col
        else:
            return

    def reset(self):
        self.board = [[i + j * NUM_TILES for i in range(1, NUM_TILES + 1)] for j in range(0, NUM_TILES)]
        # print(self.board)
        self.empty_row, self.empty_col = NUM_TILES - 1, NUM_TILES - 1
        self.history = []

    def undo(self):
        # print(self.history)
        l = len(self.history)
        self.rev = True
        if l > 0:
            self.move(dxn[3 - move_num[self.history[l-1]]])
            self.history.pop()
        self.rev = False    
        
    def play(self):
        self.draw_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.move('down')
                    elif event.key == pygame.K_LEFT:
                        self.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.move('right')
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_z:
                        self.undo()
                    elif event.key == pygame.K_s:
                        self.shuffle()
                    
                self.draw_board()


if __name__ == "__main__":
    puzzle = Puzzle15()
    puzzle.play()
