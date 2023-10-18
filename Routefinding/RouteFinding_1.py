


# info = {
#     "A":{
#         "B":2,
#         "C":4
#     },
#     "B":{
#         "A":2,
#         "C":2,
#         "D":3
#     },
#     "C":{
#         "A":4,
#         "B":2,
#         "D":2
#     },
#     "D":{
#         "B":3,
#         "C":2
#     }
# }

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

info = {
    "A-B":4,
    "A-C":2,
    "C-B":3,
    "C-D":6,
    "B-D":5,
    "D-E":3,
    "B-E":5
}

def map_formatter(formatted_info:dict[str, int]):
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

info = map_formatter(info)
    

#   A - 2 - B - 3 - D
#     \     |      /
#       4   2    2
#         \ |  /
#           C
#
 

class World:
    def __init__(self, map:dict[str,dict[str, int]],):
        self.map = map
        self.current_vertex = list(map.keys())[0]

        self.vertex_info = {}   # ? [TIME CONSUMED, VERTEX BEFORE, EXPLORED]
        self.vertex_info[self.current_vertex] = [0, self.current_vertex, True]
        for i in list(map.keys())[1:]:
            self.vertex_info[i] = [float('inf'), False, False]

    def goto(self, vertex:str, log_message:bool=True) -> str:
        travel_time = self.map[self.current_vertex][vertex]
        self.vertex_info[vertex] = [self.vertex_info[vertex][0], self.vertex_info[vertex][1], True]
        self.current_vertex = vertex
        
        if log_message:
            return f"Go to {vertex}! Time Consumed: {travel_time}, Total Travel Time: {self.vertex_info[vertex][0]} minutes"
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
    
    def reset(self):
        self.current_vertex = list(self.map.keys())[0]
        
    def route(self, vertex:str):
        route_str = vertex

        current_vertex = vertex
        while current_vertex != list(self.map.keys())[0]:
            if self.vertex_info[current_vertex][2] == False:
                break
            
            route_str = self.vertex_info[current_vertex][1] + " > " + route_str
            current_vertex = self.vertex_info[current_vertex][1]
            
        return route_str
    


world = World(info)

max_iteration = 30
def find_route(world:World, target:str):

    index = 0
    while(index < max_iteration):

        fastest_route = float('inf')
        choosen_route = ""
        current_avaliable_vertex = world.avaliable_vertex()
        for i in current_avaliable_vertex:
            world.explore(i)

        for i in current_avaliable_vertex:
            time_consumed = world.time_consumed(i)
            if world.vertex_info[i][2] == False:
                if fastest_route > time_consumed:
                    choosen_route = i
                    fastest_route = time_consumed

        print(world.goto(choosen_route))
        
        if world.current_vertex == target:
            world.reset()
            print(f"\nDONE! Time Traveled : {world.vertex_info[target][0]}, Iteration : {index}, Route : {world.route(target)}")
            break
         
        index+=1


find_route(world, "E")
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




