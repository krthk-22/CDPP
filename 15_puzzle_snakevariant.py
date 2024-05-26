import pygame
import random
import sys

pygame.init()

# Constants
NUM_TILES = 6
WINDOW_SIZE = (NUM_TILES-2) * 200
CENTRE = 100
TILE_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)

# Initialize the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("15 Puzzle Variant")

font = pygame.font.Font(None, 36)

dxn = ['up', 'right', 'left', 'down']
dnum = {'up':0, 'right':1, 'left':2, 'down':3}

class Puzzle15:
    def __init__(self):

        self.board = [[0 for i in range(NUM_TILES)] for j in range(NUM_TILES)]
        self.snake = [16, 15, 14, 13, 9, 10, 11, 12, 8, 7, 6, 5, 1, 2, 3 ,4]
        self.snake = self.snake[::-1]
        self.body = {}
        for i in range(1, NUM_TILES - 1):
            for j in range(1, NUM_TILES - 1):
                x = 4*(i-1) + j 
                self.board[i][j] = x
                self.body[x] = [i, j]
            
        print(self.body)
        self.empty_row, self.empty_col = NUM_TILES - 2, NUM_TILES - 2 #head 
        self.solved_state = self.board
        self.history = []
        self.rev = False
        #self.shuffle()
        
        
        print(self.snake)

    
    def shuffle(self):
        for _ in range(1000):
            possible_moves = self.get_possible_moves()
            direction = random.choice(possible_moves)
            self.move(direction)

    def get_possible_moves(self):
        possible_moves = []
        x = self.empty_row
        y = self.empty_col
        if self.empty_row > 0:
            if(self.board[x-1][y]) == 0:
                possible_moves.append('up')
        if self.empty_row < NUM_TILES - 1:
            if(self.board[x+1][y] == 0):
                possible_moves.append('down')
        if self.empty_col > 0:
            if(self.board[x][y-1] == 0):
                possible_moves.append('left')
        if self.empty_col < NUM_TILES - 1:
            if(self.board[x][y+1] == 0):
                possible_moves.append('right')

        #remove later
        #possible_moves = ['up', 'down', 'left', 'right']
        return possible_moves

    def draw_board(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                num = self.board[row][col]
                if num == 25 and (row + col) % 2 == 0:
                    pygame.draw.rect(screen, ORANGE, (CENTRE + col * TILE_SIZE, CENTRE + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif num == 25 and (row + col) % 2 == 1:
                    pygame.draw.rect(screen, GREEN, (CENTRE + col * TILE_SIZE, CENTRE + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif (row + col) % 2 == 0:
                    pygame.draw.rect(screen, ORANGE, (CENTRE + col * TILE_SIZE, CENTRE + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render(str(num), True, BLACK)
                    text_rect = text.get_rect(center=(CENTRE + col * TILE_SIZE + TILE_SIZE // 2, CENTRE + row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)
                elif (row + col) % 2 == 1:
                    pygame.draw.rect(screen, GREEN, (CENTRE + col * TILE_SIZE, CENTRE + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    text = font.render(str(num), True, BLACK)
                    text_rect = text.get_rect(center=(CENTRE + col * TILE_SIZE + TILE_SIZE // 2, CENTRE + row * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(text, text_rect)

        pygame.display.flip()

    def clear(self):
        self.board = [[0 for i in range(NUM_TILES)] for j in range(NUM_TILES)]

    def move(self, direction):
        if direction in self.get_possible_moves() or self.rev == True:

            if(self.rev == False):
                self.history.append(direction)
            
            new_row, new_col = self.empty_row, self.empty_col

            if direction == 'up':
                new_row -= 1
            elif direction == 'down':
                new_row += 1
            elif direction == 'left':
                new_col -= 1
            elif direction == 'right':
                new_col += 1
            else:
                return
            '''
            self.board[self.empty_row][self.empty_col], self.board[new_row][new_col] = \
                self.board[new_row][new_col], self.board[self.empty_row][self.empty_col]
            self.empty_row, self.empty_col = new_row, new_col
            '''
            self.empty_row, self.empty_col = new_row, new_col
            for i in range(len(self.snake)-1):
                el = self.snake[i]
                self.body[el] = self.body[self.snake[i+1]]

            self.body[self.snake[15]] = [new_row, new_col]

            self.clear()

            for t in self.snake:
                self.board[self.body[t][0]][self.body[t][1]] = t 
                
        else:
            return

    def reset(self):
        self.clear()
        
        #self.board = [[i + j * NUM_TILES for i in range(1, NUM_TILES + 1)] for j in range(0, NUM_TILES)]
        #print(self.board)
        self.empty_row, self.empty_col = NUM_TILES - 2, NUM_TILES - 2
        self.history = []
        self.body = {}
        for i in range(1, NUM_TILES - 1):
            for j in range(1, NUM_TILES - 1):
                x = 4*(i-1) + j 
                self.board[i][j] = x
                self.body[x] = [i, j]
        

    def undo(self):
        #print(self.history)
        l = len(self.history)
        self.rev = True
        if(l > 0):
            self.move(dxn[3 - dnum[self.history[l-1]]])
            self.history.pop()
        self.rev = False

    def new_snake(self):
        for i in range(4):
            for j in range(4):
                if(self.board[i+1][j+1] == 0):
                    return False

        return True

    def play(self):
        self.draw_board()
        while True:

            if(self.new_snake()):
                self.snake = []
                for i in range(4, 0, -1):
                    for j in range(4, 0, -1):
                        if i%2 == 1:
                            self.snake.append(self.board[i][5-j])
                        else:
                            self.snake.append(self.board[i][j])
                 
                
                self.snake = self.snake[::-1]
                self.empty_row, self.empty_col = self.body[self.snake[15]][0], self.body[self.snake[15]][1]
                #print(self.snake)

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

                    '''
                    elif event.key == pygame.K_z:
                        self.undo()
                    '''
                    self.draw_board()


if __name__ == "__main__":
    puzzle = Puzzle15()
    puzzle.play()
