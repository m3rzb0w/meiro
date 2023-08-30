#!/usr/bin/env python
import pygame
import sys
#DFS
#BFS
#Dijkstra
#AStar

###--MOUSE EVENT MAPPING--###
mouse_buttons_event = {"LEFT": 1, "MIDDLE": 2, "RIGHT": 3}
####

window_width = 800
window_height = 800

columns = 25
rows = 25

grid = []
queue = []
path = []

square_width = window_width // columns
square_height = window_height // rows

class Square:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
    
    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * square_width, self.y * square_height, square_width - 2, square_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Square(i, j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()



class Maze:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('meiro')
        self.display = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
    
    def render_fps(self, display):
        self.text = self.font.render('FPS: ' + str(round(self.clock.get_fps(),2)), True, 'Cyan')
        display.blit(self.text, (window_width - 100, 0))

    def draw_grid(self, grid):
        for i in range(columns):
            for j in range(rows):
                square = grid[i][j]
                square.draw(self.display, (20, 20, 20))
                if square.start:
                    square.draw(self.display, (0, 200, 200))
                if square.wall:
                    square.draw(self.display, (90, 90, 90))
                if square.target:
                    square.draw(self.display, (200, 200, 0))
                if square.queued and not square.start and not square.target:
                    square.draw(self.display, (200, 0, 0))
                if square.visited and not square.start and not square.target:
                    square.draw(self.display, (0, 200, 0))
                if square in path:
                    square.draw(self.display, (255, 20, 147))

    def run(self):

        start_square = grid[0][0]
        start_square.start = True
        start_square.visited = True
        queue.append(start_square)

        begin_search = False
        target_box_set = False
        searching = True
        target_box = None

        while True:
            self.display.fill((0, 0, 0))

            self.draw_grid(grid)
           

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #mouse
                elif event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    if event.buttons[0]:
                        i = x // square_width
                        j = y // square_height
                        grid[i][j].wall = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == mouse_buttons_event["LEFT"]:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    i = x // square_width
                    j = y // square_height
                    if grid[i][j].wall:
                        grid[i][j].wall = False
                        grid[i][j].target = False
                    else:
                        grid[i][j].wall = True
                        grid[i][j].target = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == mouse_buttons_event["MIDDLE"]:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    i = x // square_width
                    j = y // square_height
                    if grid[i][j].start:
                        grid[i][j].start = False
                        grid[i][j].visited = False
                        queue.pop(0)
                    else:
                        if start_square:
                            start_square.start = False
                            start_square.visited = False
                            queue.pop(0)
                        start_square = grid[i][j]
                        start_square.start = True
                        start_square.visited = True
                        queue.append(start_square)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == mouse_buttons_event["RIGHT"]:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    i = x // square_width
                    j = y // square_height
                    if grid[i][j].target:
                        grid[i][j].target = False
                        grid[i][j].wall = False
                        target_box_set = False
                    else:
                        if target_box:
                            target_box.target = False
                        grid[i][j].target = True
                        grid[i][j].wall = False
                        target_box = grid[i][j]
                        target_box_set = True
                #start algo
                if event.type == pygame.KEYDOWN and target_box_set:
                    begin_search = True
                
            
            if begin_search:
                if len(queue) > 0 and searching:
                    current_square = queue.pop(0)
                    current_square.visited = True
                    if current_square == target_box:
                        searching = False
                        while current_square.prior != start_square:
                            path.append(current_square.prior)
                            current_square = current_square.prior
                        print(len(path) + 2)
                    else:
                        for neighbour in current_square.neighbours:
                            if not neighbour.queued and not neighbour.wall:
                                neighbour.queued = True
                                neighbour.prior = current_square
                                queue.append(neighbour)
                else:
                    if searching:
                        print("no solution")
                        searching = False

            
            self.render_fps(self.display)
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":
    Maze().run()