from time import time
from math import ceil



# ? ======== First Case ======== #
# info = {
#     "Bandung":{
#         "Bekasi":20,
#         "Jogjakarta":30
#     },
#     "Bekasi":{
#         "Bandung":20,
#         "Jogjakarta":45,
#         "Semarang":60
#     },
#     "Jogjakarta":{
#         "Bandung":30,
#         "Bekasi":45,
#         "Semarang":25
#     },
#     "Semarang":{
#         "Bekasi":60,
#         "Jogjakarta":25
#     }
# }

# ? ======== Second Case ======== #
# info = {
#     "A-B":4,
#     "A-C":2,
#     "C-B":3,
#     "C-D":6,
#     "B-D":5,
#     "D-E":3,
#     "B-E":5
# }

# # ? ======= Third Case ======= #
# info = {
#     "A-C":2,
#     "A-E":3,
#     "C-E":4,
#     "G-E":5,
#     "G-B":4,
#     "C-B":6,
#     "B-D":6,
#     "C-D":4,
#     "H-D":7,
#     "H-F":4,
#     "G-F":4,
# }

# ? ======= Third Case ======= #
info = {
    "A-C":5,
    "A-B":4,
    "B-C":2,
    "B-E":3,
    "B-D":4,
    "C-D":3,
    "C-F":4,
    "D-E":2,
    "D-F":2,
    "D-H":3,
    "D-G":6,
    "D-I":4,
    "E-G":4,
    "E-H":5,
    "F-H":4,
    "F-I":2,
    "H-I":2,
    "H-G":2,
}


def map_deformatter(formatted_info:dict[str, int]) -> dict[str, dict[str, int]]:
    retval = {}
    for i in list(formatted_info.keys()):
        vertex = i.split("-")[0]
        retval[vertex] = {}
        for j in list(formatted_info.keys()):
            vertex_2 = j.split("-")[0]
            if vertex_2 != vertex:
                retval[vertex][vertex_2] = 0

    for i in list(formatted_info.keys()):
        vertex = i.split("-")[1]
        retval[vertex] = {}
        for j in list(formatted_info.keys()):
            vertex_2 = j.split("-")[1]
            if vertex_2 != vertex:
                retval[vertex][vertex_2] = 0
                
                

    for i in list(formatted_info.keys()):
        i_splitted = i.split("-")
        retval[i_splitted[0]][i_splitted[1]] = formatted_info[i]
        retval[i_splitted[1]][i_splitted[0]] = formatted_info[i]
        
    deleted_row_column = []
    for i in retval:
        for j in retval[i]:
            if retval[i][j] == 0:
                deleted_row_column.append([i, j])

    for [i, j] in deleted_row_column:
        del retval[i][j]
        
    return retval

def map_formatter(info:dict[str, dict[str, int]]) -> dict[str, int]:
    retval = {}
    for i in info:
        for j in info[i]:
            if str(j)+"-"+str(i) in retval:
                continue
            retval[str(i)+"-"+str(j)] = info[i][j]

    return retval
    

info = map_deformatter(info)

    

#   A - 2 - B - 3 - D
#     \     |      /
#       4   2    2
#         \ |  /
#           C
#
 

class World:
    def __init__(self, map:dict[str,dict[str, int]], start_vertex:str=False):
        self.map = map
        if not start_vertex:
            self.current_vertex = list(map.keys())[0]
        else:
            self.current_vertex = start_vertex

        self.start_vertex = start_vertex

        self.vertex_info = {}   # ? [TIME CONSUMED, VERTEX BEFORE, EXPLORED]
        self.vertex_info[self.current_vertex] = [0, self.current_vertex, True]
        for i in list(map.keys()):
            if i == self.current_vertex:
                continue
            self.vertex_info[i] = [float('inf'), False, False]

    def goto(self, vertex:str, log_message:bool=True) -> str:
        self.vertex_info[vertex] = [self.vertex_info[vertex][0], self.vertex_info[vertex][1], True]
        self.current_vertex = vertex
        
        if log_message:
            return f"Go to {vertex}! Total Travel Time: {self.vertex_info[vertex][0]} minutes"
        else:
            return None
        
    def explore(self, vertex:str, log_message:bool=True):
        travel_time = self.map[self.current_vertex][vertex]
        total_time = self.vertex_info[self.current_vertex][0] + travel_time
        if self.vertex_info[vertex][0] > total_time:
            self.vertex_info[vertex] = [total_time, self.current_vertex, self.vertex_info[vertex][2]]
            
        # ? | DEBUGGING |
        # print(f"vertex {vertex} info : {self.vertex_info[vertex]}")
        
        if log_message:
            return f"Explore {vertex}! Time Consumed: {travel_time}, Total Travel Time: {total_time} minutes"
        else:
            return None
        
    def avaliable_vertex(self) -> list[str]:
        return list(self.map[self.current_vertex].keys())
    
    def time_consumed(self, vertex:str) -> int:
        return self.vertex_info[vertex][0]
    
    def reset(self, start_vertex:str=False):
        if start_vertex:
            self.start_vertex = start_vertex

        self.current_vertex = self.start_vertex
        
        self.vertex_info = {}   # ? [TIME CONSUMED, VERTEX BEFORE, EXPLORED]
        self.vertex_info[self.current_vertex] = [0, self.current_vertex, True]
        for i in list(self.map.keys()):
            if i == self.current_vertex:
                continue
            self.vertex_info[i] = [float('inf'), False, False]
        
    def route(self, vertex:str):
        route_str = vertex

        current_vertex = vertex
        while current_vertex != self.start_vertex:
            if self.vertex_info[current_vertex][2] == False:
                break
            
            route_str = self.vertex_info[current_vertex][1] + " > " + route_str
            current_vertex = self.vertex_info[current_vertex][1]
            
        return route_str
    
    def verticies(self) -> list[str]:
        return list(self.map.keys())
    


world = World(info)

max_iteration = 30
def find_route(world:World, target:str, start:str=False):
    print(f" {"_"*38} ")
    print(f"|{"Data":^38}|")
    print(f"|{"-"*38}|")
    for [i, j] in map_formatter(world.map).items():
        print(f"|{f"{i}":<19}:{f"{j} Minutes":<18}|")
    print(f"|{"_"*38}|")
    
    if start:
        world.reset(start)

    index = 0

    clock = time()
    while(index < max_iteration):

        fastest_route = float('inf')
        choosen_route = ""
        current_avaliable_vertex = world.avaliable_vertex()
        # print(current_avaliable_vertex)
        for i in current_avaliable_vertex:
            world.explore(i)

        for i in world.verticies():
            time_consumed = world.time_consumed(i)
            # print("info "+i+" : ", end="")
            # print(world.vertex_info[i])
            if world.vertex_info[i][2] == False:
                if fastest_route > time_consumed:
                    choosen_route = i
                    fastest_route = time_consumed

        print(world.goto(choosen_route))
        
        if world.current_vertex == target:
            print(f"\nDONE! Algorithm Time : {ceil(((time()-clock)*10000000))/10000000} seconds, Time Traveled : {world.vertex_info[target][0]} minutes, Iteration : {index}, Route : {world.route(target)}")
            break
        
        index+=1


print(info)
find_route(world, start="A", target="H")
# av_vertex = world.avaliable_vertex()
# print(av_vertex)
# print(world.explore(av_vertex[0]))
# print(world.explore(av_vertex[1]))
# print(world.goto(av_vertex[0]))
# av_vertex = world.avaliable_vertex()
# print(av_vertex)
# print(world.explore(av_vertex[0]))
# print(world.explore(av_vertex[1]))
# print(world.explore(av_vertex[2]))
# print(world.goto(av_vertex[1]))
# av_vertex = world.avaliable_vertex()
# print(av_vertex)
# print(world.explore(av_vertex[2]))
# print(world.goto(av_vertex[2]))




