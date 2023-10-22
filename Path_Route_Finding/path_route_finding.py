import pygame


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
        check_pos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for c_pos in check_pos:
            result = [0, 0]
            result[0] = c_pos[0] + pos[0]
            result[1] = c_pos[1] + pos[1]
            surround.append((result[0], result[1]))
            
        return surround
    
    def get_cost(self, pos:tuple[2]) -> float:
        return self.map_info[pos[0]][pos[1]]["cost"]
                
    def explore(self):
        surround = self.get_surround_pos(self.current_pos)
        early_cost = self.get_cost(self.current_pos)
        for (x, y) in surround:
            if x > len(self.map_info) - 1 or x < 0 or y > len(self.map_info[1]) - 1 or y < 0:
                continue
            
            if self.map_info[x][y]["tag"] == "obstacle":
                continue
            
            before_cost = self.map_info[x][y]["cost"]

            if before_cost > early_cost+1:
                self.map_info[x][y]["before"] = self.current_pos
                self.map_info[x][y]["cost"] = early_cost+1
                
                
    def get_shortest_cost(self):
        lowest_cost = float('inf')
        pos = (0, 0)

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
        self.current_pos = self.get_shortest_cost()[0]
        self.map_info[self.current_pos[0]][self.current_pos[1]]["explored"] = True
        
        
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
        # if start:
        #     self.map_info[self.current_pos[0]][self.current_pos[1]]["explored"] = False
        #     self.map_info[self.current_pos[0]][self.current_pos[1]]["tag"] = S
        #     self.current_pos = start
        #     self.map_info[self.current_pos[0]][self.current_pos[1]]["explored"] = True
        #     self.map_info[self.current_pos[0]][self.current_pos[1]]["tag"] = S
            
        iteration = 0
        while True:
            self.explore()
            self.move()
            
            if self.map_info[self.target_pos[0]][self.target_pos[1]]["explored"] == True:
                break
            
            iteration += 1

        track_path = self.track_path(self.target_pos, True)

        return track_path, iteration

        
        

world = World(MAP_2)

route, iteration = world.route()
print(world.get_surround_pos((2, 0)))



CELL_WIDTH = 50
CELL_HEIGHT = 50

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                break
            
            elif event.key == pygame.K_SPACE:
                show_path = False if show_path else True
    
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

            pygame.draw.rect(screen, color, (j*CELL_HEIGHT+2*j, i*CELL_WIDTH+2*i, CELL_WIDTH, CELL_HEIGHT), border_radius=5)
            
    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60
    
    
pygame.quit()