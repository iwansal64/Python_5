


S = " " # ? PATH
P = "P" # ? PLAYER
T = "T" # ? TARGET
O = "X" # ? OBSTACLE

x = [
    [T, S, S, S],
    [O, O, S, S],
    [S, S, S, S],
    [P, S, S, S]
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
                    "cost":cost
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
            try:
                before_cost = self.map_info[y][x]["cost"]
            except IndexError:
                continue

            if before_cost > early_cost+1:
                self.map_info[y][x]["before"] = self.current_pos
                self.map_info[y][x]["cost"] = early_cost+1
                
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
        
        
    def track_path(self, pos) -> list[tuple[2]]:
        path = []
        current_pos = pos
        while current_pos != self.start_pos:
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

        track_path = self.track_path(self.target_pos)

        return track_path, iteration

        
        

world = World(x)

print(world.route())







