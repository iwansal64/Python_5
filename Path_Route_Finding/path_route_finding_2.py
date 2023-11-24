import pygame
from math import ceil
from time import time


S = " " # ? PATH
P = "P" # ? PLAYER
T = "T" # ? TARGET
O = "X" # ? OBSTACLE

MAP_1 = [
    [T, S, S, S, S, S, S, S],
    [O, O, O, O, S, O, O, O],
    [S, S, S, O, S, O, S, S],
    [S, O, S, O, S, S, S, O],
    [S, O, S, O, O, S, O, O],
    [S, O, S, S, S, S, O, O],
    [S, O, S, O, O, O, O, O],
    [S, S, S, S, S, S, S, P]
]

MAP_2 = [
    [T, S, S, S, S, S, S, S],
    [O, O, O, O, S, O, O, O],
    [O, O, S, O, S, O, S, S],
    [S, O, S, O, S, S, S, O],
    [S, O, S, O, S, O, O, O],
    [S, S, S, S, S, O, O, O],
    [S, O, O, O, O, O, O, O],
    [S, S, S, S, S, S, S, P]
]

MAP_3 = [
    [S, S, S, S, S, O],
    [S, O, O, O, S, O],
    [S, O, S, P, S, O],
    [S, O, S, S, S, O],
    [T, O, O, O, O, O]
]

class World:
    def __init__(self, map:list):
        self.map = map
        
        self.start_pos = (0, 0)
        self.current_pos = (0, 0)
        self.target_pos = (0, 0)
        
        self.map_info = []
        for i in range(len(map)):
            self.map_info.append([])
            for j in range(len(map[0])):
                tag = "path"
                explored = False
                cost = float('inf')

                if map[i][j] == P:
                    tag = "player"
                    explored = True
                    cost = 0
                    self.current_pos = (i, j)
                    self.start_pos = (i, j)

                elif map[i][j] == T:
                    tag = "target"
                    self.target_pos = (i, j)
                    
                elif map[i][j] == O:
                    tag = "obstacle"
                
                starting_info = {
                    "pos":(i,j),
                    "tag":tag,
                    "explored":explored,
                    "before":False,
                    "cost":cost,
                    "is_route":False
                }
                
                self.map_info[i].append(starting_info)
                
    def get_surround_pos(self, pos:tuple[2]) -> list:
        surround = []
        check_pos = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        
        for c_pos in check_pos:
            result = [0, 0]
            result[0] = c_pos[0] + pos[0]
            result[1] = c_pos[1] + pos[1]
            surround.append((result[0], result[1]))
            
        return surround, check_pos
    
    def get_cost(self, pos:tuple[2]) -> float:
        return self.map_info[pos[0]][pos[1]]["cost"]
                
    def explore(self):
        surround, check_pos = self.get_surround_pos(self.current_pos)
        after_cost = self.get_cost(self.current_pos)
        there_are_changes = False
        for i, (x, y) in enumerate(surround):
            if x > len(self.map_info) - 1 or x < 0 or y > len(self.map_info[1]) - 1 or y < 0:
                continue
            
            if self.map_info[x][y]["tag"] == "obstacle":
                continue
            
            before_cost = self.map_info[x][y]["cost"]
            if check_pos[i][0] != 0 and check_pos[i][1] != 0:
                after_cost += 1.5
            else:
                after_cost += 1

            if before_cost > after_cost+1:
                self.map_info[x][y]["before"] = self.current_pos
                self.map_info[x][y]["cost"] = after_cost+1
                there_are_changes = True

        return there_are_changes
                
                
    def get_shortest_cost(self):
        lowest_cost = float('inf')
        pos = False

        for i in range(len(self.map_info)):
            for j in range(len(self.map_info[0])):
                if self.map_info[i][j]["explored"] or self.map_info[i][j]["tag"] == "obstacle":
                    continue
                
                cost = self.map_info[i][j]["cost"]
                if cost < lowest_cost:
                    lowest_cost = cost
                    pos = (i, j)
                    
        return pos, lowest_cost
                
                
    def move(self):
        res, cost = self.get_shortest_cost()
        if not res:
            return False
        
        self.current_pos = res
        self.map_info[self.current_pos[0]][self.current_pos[1]]["explored"] = True
        return True
        
        
    def track_path(self, pos, its_a_target:bool=False) -> list[tuple[2]]:
        path = []
        current_pos = pos
        while current_pos != self.start_pos:
            if its_a_target and current_pos != pos:
                self.map_info[current_pos[0]][current_pos[1]]["is_route"] = True

            path.append(current_pos)
            current_pos = self.map_info[current_pos[0]][current_pos[1]]["before"]
            
            if current_pos == False:
                break
            
        return path
        
    def route(self):
        if not self.start_pos or not self.target_pos:
            return False, 0
            
            
        iteration = 0
        while True:
            exp = self.explore()
            move = self.move()
            
            if not exp and not move:
                return False, 1
            
            if self.map_info[self.target_pos[0]][self.target_pos[1]]["explored"] == True or iteration > 40:
                break
            
            iteration += 1

        track_path = self.track_path(self.target_pos, True)

        return track_path, iteration
    
    def check_in_map(self, something:str, tag:bool=False):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if tag:
                    if self.map_info[i][j]["tag"] == something:
                        return (i, j)
                else:
                    if self.map[i][j] == something:
                        return (i, j)
                
        return False
    
    def reset(self):
        for i in range(len(self.map_info)):
            for j in range(len(self.map_info[0])):
                if self.map_info[i][j]["tag"] == "player":
                    self.map_info[i][j]["explored"] = True
                    self.map_info[i][j]["cost"] = 0
                    self.current_pos = (i, j)
                else:
                    self.map_info[i][j]["explored"] = False
                    self.map_info[i][j]["cost"] = float('inf')

                self.map_info[i][j]["before"] = False
                self.map_info[i][j]["is_route"] = False
                
    
    def change_tag(self, pos:tuple[2], tag:str):
        if self.map_info[pos[0]][pos[1]]["tag"] == tag:
            return

        explored = False
        cost = float('inf')
        result_tag = ""
        
        if tag == P:
            player_pos = self.check_in_map("player", tag)
            if player_pos:
                self.change_tag(player_pos, S)
                
            result_tag = "player"
            explored = True
            cost = 0
            self.current_pos = pos
            self.start_pos = pos

        elif self.map[pos[0]][pos[1]] == P:
            self.start_pos = False
            print("FALSED")

        if tag == T:
            target_pos = self.check_in_map("target", tag)
            if target_pos:
                self.change_tag(target_pos, S)
                
            result_tag = "target"
            self.target_pos = pos
            
        elif self.map[pos[0]][pos[1]] == T:
            self.target_pos = False
            
        if tag == O:
            result_tag = "obstacle"
        
        elif tag == S: 
            result_tag = "path"            

        self.map[pos[0]][pos[1]] = tag

        self.map_info[pos[0]][pos[1]]["tag"] = result_tag
        self.map_info[pos[0]][pos[1]]["explored"] = explored
        self.map_info[pos[0]][pos[1]]["cost"] = cost
        self.map_info[pos[0]][pos[1]]["is_route"] = False
        
        self.reset()

        
        

world = World(MAP_3)

print(world.get_surround_pos((2, 0)))

def set_text(string, coordx, coordy, fontSize:int=36, color:tuple[3]=[0, 0, 0]): #Function to set text
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)


CELL_WIDTH = 50
CELL_HEIGHT = 50
CELL_GAP = 10

PLAYER_COLOR = (20, 100, 100)
PATH_COLOR = (80, 80, 80)
TARGET_COLOR = (200, 10, 10)
OBSTACLE_COLOR = (10, 10, 10)
ROUTE_COLOR = (34, 164, 212)

pygame.init()

WIDTH = 900
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

show_path = False
grid_width = len(world.map[0])*CELL_WIDTH+CELL_GAP*len(world.map[0])
grid_height = len(world.map)*CELL_HEIGHT+CELL_GAP*len(world.map)
grid_start_x = (WIDTH//2)-(grid_width//2)
grid_start_y = (HEIGHT//2)-(grid_height//2)

message = ""
message_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                break
            
            elif event.key == pygame.K_SPACE:
                res, code = world.route()
                if not res:
                    if code == 0:
                        message = "Ada yang kurang. . ."
                    elif code == 1:
                        message = "Tidak ada jalan . ."
                        
                    message_time = time() + 5
                else:
                    message = ""
                    
                show_path = True
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if x_mouse > grid_start_x and x_mouse < grid_start_x+grid_width and y_mouse > grid_start_y and y_mouse < grid_start_y+grid_height:
                x = (x_mouse-grid_start_x)
                y = (y_mouse-grid_start_y)
                
                x_pos = ceil(x/(CELL_WIDTH+CELL_GAP))
                y_pos = ceil(y/(CELL_HEIGHT+CELL_GAP))
                if (x < (x_pos*CELL_WIDTH+(x_pos-1)*CELL_GAP) or x > x_pos*(CELL_WIDTH+CELL_GAP)) and (y < y_pos*(CELL_HEIGHT+(y_pos-1)*CELL_GAP) or y > y_pos*(CELL_HEIGHT+CELL_GAP)):
                    y_index = x_pos-1
                    x_index = y_pos-1
                    if event.button == 1:
                        if world.start_pos:
                            world.change_tag((x_index, y_index), O)
                            # print(world.start_pos)
                        else:
                            world.change_tag((x_index, y_index), P)
                        
                    elif event.button == 3:
                        if world.target_pos:
                            world.change_tag((x_index, y_index), S)
                        else:
                            world.change_tag((x_index, y_index), T)
                            
                    show_path = False
                        

                    

                    
                    
            
    
    if not running:
        break

    screen.fill("gray")

    # ? Grid Creation
    for i in range(len(world.map)):
        for j in range(len(world.map[0])):
            color = PATH_COLOR
            tag = world.map_info[i][j]["tag"]
            if tag == "player":
                color = PLAYER_COLOR
            elif tag == "obstacle":
                color = OBSTACLE_COLOR
            elif tag == "target":
                color = TARGET_COLOR
                
            if show_path and world.map_info[i][j]["is_route"]:
                color = ROUTE_COLOR

            pygame.draw.rect(screen, color, (grid_start_x+j*CELL_HEIGHT+CELL_GAP*j, grid_start_y+i*CELL_WIDTH+CELL_GAP*i, CELL_WIDTH, CELL_HEIGHT), border_radius=5)

    # ? Message Display
    if message:
        text = set_text(message, (WIDTH//2), (HEIGHT-100), color=(20, 20, 20))
        screen.blit(text[0], text[1])

        if message_time < time():
            message = ""
            
    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60
    
    
pygame.quit()