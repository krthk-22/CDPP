import pygame
import random
import sys
import math

pygame.init()

# Constants
NUM_TILES = int(input("Enter the size of the grid: "))
WINDOW_SIZE = NUM_TILES * 100

TILE_SIZE = 100
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Initialize the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("15 Puzzle Variant")
3
font = pygame.font.Font(None, 36)

dxn = ['up', 'right', 'left', 'down']
move_num = {'up': 0, 'right': 1, 'left': 2, 'down': 3}
key_binds = "asdfghjkl"
custom = {}

'''
i, j on grid => 4*i + j + 1
cell no c => c/4, c%4 - 1
graph[c] = list of cell nos blank can move to from c  
'''

def to_num(i, j):
    return NUM_TILES*i + j + 1 # changed 4 to NUM_TILES

def to_rc(c):
    c = int(c)
    i = int((c-1)/NUM_TILES) #changed 4 to NUM_TILES
    j = (c-1)%NUM_TILES #changed 4 to NUM_TILES
    return i, j

def dir(i, j): #dir of j wrt i (cell nos)
    if i == j:
        return "same"
    elif j == i+NUM_TILES: #changed 4 to NUM_TILES
        return "down"
    elif j == i-NUM_TILES: # changed 4 to NUM_TILES
        return "up"
    elif j == i-1:
        return "left"
    elif j == i+1:
        return "right"

    return "invalid"

def draw_arrow(startX, startY, endX, endY, line_color):
    pygame.draw.line(screen, line_color, (startX, startY), (endX, endY))
    dx = endX - startX
    dy = endY - startY
    l = math.sqrt(dx**2 + dy**2)
    ux = 10*dx/l
    uy = 10*dy/l
    px = -1*uy
    py = ux
    lx = endX + px
    ly = endY + py
    rx = endX - px
    ry = endY - py
    tx = endX + ux
    ty = endY + uy
    pygame.draw.polygon(screen, (0, 0, 255), [(lx, ly), (rx, ry), (tx, ty)])

class Puzzle15:
    def __init__(self):
        self.board = [[i + j * NUM_TILES for i in range(1, NUM_TILES + 1)] for j in range(0, NUM_TILES)]
        self.empty_row, self.empty_col = NUM_TILES - 1, NUM_TILES - 1
        self.solved_state = self.board
        self.history = []
        self.graph = {} #tile connections for movement
        self.rev = False
        self.curr_bind = 0
        #custom['a'] = [16, 15, 14, 13, 9, 5, 1, 2, 3, 4, 8, 12, 16]
        
        
        #self.shuffle()

    def shuffle(self):
        for _ in range(1000):
            possible_moves = self.get_possible_moves()
            direction = random.choice(possible_moves)
            self.move(direction)

    def get_possible_moves(self):
        possible_moves = []
        curr_cell = to_num(self.empty_row, self.empty_col)
        if curr_cell + NUM_TILES in self.graph[curr_cell]: # changed 4 to NUM_TILES
                possible_moves.append('down')
        if curr_cell - NUM_TILES in self.graph[curr_cell]: # changed 4 to NUM_TILES
                possible_moves.append('up')
        if curr_cell + 1 in self.graph[curr_cell]:
                possible_moves.append('right')
        if curr_cell - 1 in self.graph[curr_cell]:
                possible_moves.append('left')
        return possible_moves

    def get_state(self):
        l = [i for i in range(1, NUM_TILES**2 + 1)] #changed from 17 to NUM_TILES**2 + 1
        perm = []
        isVisit = [0 for i in range(NUM_TILES**2)] #changed from 16 to NUM_TILES**2
        for c in range(1, NUM_TILES*NUM_TILES + 1):
            i, j = to_rc(c)
            l[c-1] = self.board[i][j]

        for i in range(NUM_TILES**2): #changed from 16 to NUM_TILES**2
            if l[i] == i+1:
                isVisit[i] = 1
        
        for i in range(NUM_TILES**2): #changed from 16 to NUM_TILES**2
            x = l[i]
            y = 0
            if isVisit[x-1] == 0:
                perm.append([])
                y = 1

            while isVisit[x-1] == 0:
                perm[-1].append(x)
                isVisit[x-1] = 1
                x = l[x-1]

            if y:
                perm[-1] = perm[-1][::-1]
                
        return perm 

    def draw_board(self):
        for row in range(NUM_TILES):
            for col in range(NUM_TILES):
                num = self.board[row][col]
                if num == NUM_TILES**2 and (row + col) % 2 == 0: #changed from 16 to NUM_TILES**2
                    pygame.draw.rect(screen, ORANGE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif num == NUM_TILES**2 and (row + col) % 2 == 1: #changed from 16 to NUM_TILES**2
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
        for cell in range(1, 1+NUM_TILES**2): #changed from 17 to NUM_TILES**2 + 1
            i, j = to_rc(cell)
            startX = j * TILE_SIZE + TILE_SIZE // 2
            startY = i * TILE_SIZE + TILE_SIZE // 2
            for adj in self.graph[cell]:
                u, v = to_rc(adj)
                endX = v * TILE_SIZE + TILE_SIZE // 2
                endY = u * TILE_SIZE + TILE_SIZE // 2
                dx = endX - startX
                dy = endY - startY
                #l = math.sqrt(dx**2 + dy**2)
                #ux = dx/l
                #uy = dy/l
                endX -= dx/NUM_TILES #changed from 4 to NUM_TILES
                endY -= dy/NUM_TILES # changed from 4 to NUM_TILES
                draw_arrow(startX + dx/NUM_TILES, startY + dy/NUM_TILES, endX, endY, (255, 0, 0)) # changed from 4 to NUM_TILES
                
        pygame.display.flip()

    def move(self, direction):
        if direction in self.get_possible_moves() or self.rev == True:

            if not self.rev:
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

            self.board[self.empty_row][self.empty_col], self.board[new_row][new_col] = \
                self.board[new_row][new_col], self.board[self.empty_row][self.empty_col]
            self.empty_row, self.empty_col = new_row, new_col

        elif direction in key_binds and direction in custom:
            mov = direction
            path = custom[mov]
            tot = len(path)
            curr_cell = to_num(self.empty_row, self.empty_col)
            if curr_cell != path[0]:
                print("Invalid move")
                return
            for nxt in path: #curr_cell maybe not required
                if str(nxt) in key_binds:
                   self.move(nxt)
                else:
                  d = dir(curr_cell, nxt)
                  if d not in self.get_possible_moves() and d != "same":
                     print("Invalid Entry")
                     break
                  self.move(d)

                curr_cell = to_num(self.empty_row, self.empty_col)                                        

        else:
            return

    def set_bind(self):
        if self.curr_bind == len(key_binds):
            print("No slots available")
            return
        
        curr_key = key_binds[self.curr_bind]
        custom[curr_key] = [NUM_TILES**2] # changed from 16 to NUM_TILES**2
        for mov in self.history:
            el = custom[curr_key][-1]
            new = el
            if mov == 'left':
                new = el-1
            elif mov == 'right':
                new = el+1
            elif mov == 'up':
                new = el-NUM_TILES # changed from 4 to NUM_TILES
            elif mov == 'down':
                new = el+NUM_TILES # changed from 4 to NUM_TILES
            custom[curr_key].append(new)
        
        self.curr_bind += 1
        print(f'{curr_key} is bound to an action')
        
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

    def graph_init(self):
        for cell in range(1, 1+NUM_TILES**2): #changed from 17 to NUM_TILES**2 + 1
            self.graph[cell] = []
        
    def play(self):

        #Enter graph input
        self.graph_init()
        num = int(input("Num of chains: "))
        for j in range(num):
            l = input("Enter chain")
            vals = [int(i) for i in l.split()]
            n = len(vals)
            #self.graph[vals[n-1]].append(vals[0])
            for k in range(n-1):
                self.graph[vals[k]].append(vals[k+1])
        print(self.graph) 
        
        print(vals)
        self.draw_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    name = pygame.key.name(event.key)
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

                    elif event.key == pygame.K_q:
                        self.set_bind()

                    elif name in key_binds:
                        self.move(name)
                        

                    elif event.key == pygame.K_SPACE:
                        state = self.get_state()
                        print(f'Board State: {state}')
                    '''
                    elif event.key == pygame.K_a: # transfer to move
                        curr_cell = to_num(self.empty_row, self.empty_col)
                        if curr_cell == custom['a'][0]:
                            for nxt in custom['a']:
                                if nxt == curr_cell:
                                    continue
                                d = dir(curr_cell, nxt)
                                if d not in self.get_possible_moves():
                                    print("Invalid Entry")
                                    break
                                self.move(d)
                                curr_cell = nxt
                        else:
                            print("Not applicable at current position")
                    '''
                    
                    self.draw_board()


if __name__ == "__main__":
    puzzle = Puzzle15()
    puzzle.play()
