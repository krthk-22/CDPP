import pygame
import random
import sys
import math
import networkx as nx
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup

pygame.init()

WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (150, 200, 50) #yellow?

colors =  [BLUE, BLACK, RED, GREEN, ORANGE, YELLOW]
'''
TO DO
black edge functionality
No self loops allowed - solved for now
Rename adj and conn
Hovering over a rotator should highlight order of elements to be cycled
IMP! fixed rotators needed
May need arbitrary num of colored edges
Overlapping edges of different colors
'''

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Graph Puzzles")

def create_graph(vertices):
    G = nx.Graph()
    for node in vertices:
        for neighbor in node.adj:
            G.add_edge(node.name, neighbor.name)
    return G

def cycle(l):
    A = Permutation([range(len(l))])
    return A(l)

def list_cycles(G, node):
    cycles = nx.cycle_basis(G, node.name)  # Find all simple cycles containing the specified node
    return cycles

class Vertex:
    def __init__(self, pos, radius, name, label):
        self.pos = pos
        self.radius = radius
        self.name = name
        self.label = label
        self.neighbors = [[] for col in colors] #segregated by edge color
    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, self.radius)
        pygame.draw.circle(screen, RED, self.pos, self.radius, 2)
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.label), True, BLACK)
        text_rect = text.get_rect(center=self.pos)
        screen.blit(text, text_rect)

    def draw_edges(self):
        for col in range(len(self.neighbors)):         
            for v in self.neighbors[col]:
                pygame.draw.line(screen, colors[col], self.pos, v.pos, 7-col)

    def create_edge(self, vertex, col=0):
        if self != vertex:
            self.neighbors[col].append(vertex)
            vertex.neighbors[col].append(self)

    def is_clicked(self, click_pos):
        return (click_pos[0] - self.pos[0])**2 + (click_pos[1] - self.pos[1])**2 <= self.radius**2

    def rotate(self, col=0):
        nbrs = self.neighbors[col]
        n = len(nbrs)
        if n == 0:
            print("Empty")
            return

        currLabels = [v.label for v in nbrs]
        print(currLabels)
        newLabels = cycle(currLabels)
        for i in range(len(nbrs)):
            nbrs[i].label = newLabels[i]
            
        print([v.label for v in nbrs])

# Main loop
running = True
radius = 20  # Initial radius
vertices = []
Leftclick_queue = []
Rightclick_queue = []
numCtr = 0
editMode = True
currColor = 0 #colors[0] = BLUE

def reset():
    global vertices, Leftclick_queue, Rightclick_queue, numCtr, editMode
    vertices = []
    Leftclick_queue = []
    Rightclick_queue = []
    numCtr = 0
    editMode = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_vertex = None
            for vertex in vertices:
                if vertex.is_clicked(pos):
                    clicked_vertex = vertex
                    break
                    
            if event.button == 1:  # Left mouse button

                if clicked_vertex:
                    if clicked_vertex.label == "R" and not editMode:
                        clicked_vertex.rotate(currColor)
            
                    #print("Clicked on vertex:", clicked_vertex.label)

                    if editMode:
                        if(len(Leftclick_queue)):
                            Leftclick_queue[-1].create_edge(clicked_vertex, currColor)
                            Leftclick_queue.pop()

                        else:
                            Leftclick_queue.append(clicked_vertex)
                        
                    #print([v.name for v in vertices[-1].adj])
                    

                else:
                    if editMode:
                        name = len(vertices)  # Name with vertex index
                        label = numCtr # Labels will change with time
                        numCtr += 1
                        vertex = Vertex(pos, radius, name, label)
                        vertices.append(vertex)

            elif event.button == 3: #Create Rotator

                if editMode: 
                        name = len(vertices)  # Name with vertex index
                        label = "R" # Labels will change with time
                        vertex = Vertex(pos, radius, name, label)
                        vertices.append(vertex)
    
        elif event.type == pygame.KEYDOWN:
            
            if event.key >= ord('0') and event.key <= ord('9'):
                oldColor = currColor    
                currColor = int(chr(event.key))
                if currColor >= len(colors):
                    print("Invalid Color")
                    currColor = oldColor
                print("Current Color:", colors[currColor])


            if event.key == pygame.K_RETURN:  # Check if Enter key is pressed
                Leftclick_queue = []
                Rightclick_queue = []
                editMode = not editMode
                if editMode:
                    print("EditMode!")

                else:
                    print("Action!")

                '''                
                G = create_graph(vertices)
                cycles = list_cycles(G, vertices[0])
                print(vertices[0].name)
                print("All cycles:", cycles)
                generators = []
                for cyc in cycles:
                    generators.append(Permutation([cyc]))
                Puzzle_Group = PermutationGroup(generators)
                '''
            if event.key == pygame.K_r:
                print("Reset")
                reset()
            
                
    # Clear the screen Necessary?
    screen.fill(WHITE)

    # Draw 
    for vertex in vertices:
        vertex.draw_edges()
        
    for vertex in vertices:
        vertex.draw()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
