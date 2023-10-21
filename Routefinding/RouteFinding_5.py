import pygame
from time import time
from math import ceil, floor
import string




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
    def __init__(self, map:dict[str,dict[str, int]], start_vertex:str=False, blocked_verticies:list[str]=[]):
        self.map = map
        if not start_vertex:
            self.current_vertex = list(map.keys())[0]
        else:
            self.current_vertex = start_vertex

        self.start_vertex = start_vertex
        self.blocked_verticies = blocked_verticies

        self.vertex_info = {}   # ? [TIME CONSUMED, VERTEX BEFORE, EXPLORED]
        self.vertex_info[self.current_vertex] = [0, self.current_vertex, True]
        for i in list(map.keys()):
            if i == self.current_vertex:
                continue
            if i in blocked_verticies:
                print(i+" was blocked!")
                self.vertex_info[i] = [float('inf'), False, True]
                continue

            self.vertex_info[i] = [float('inf'), False, False]
            
        # ! DEBUGGING ONLY
        # print(self.vertex_info)

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
            
        # ! DEBUGGING ONLY
        # print(f"vertex {vertex} info : {self.vertex_info[vertex]}")
        
        if log_message:
            return f"Explore {vertex}! Time Consumed: {travel_time}, Total Travel Time: {total_time} minutes"
        else:
            return None
        
    def avaliable_vertex(self) -> list[str]:
        return list(self.map[self.current_vertex].keys())
    
    def time_consumed(self, vertex:str) -> int:
        return self.vertex_info[vertex][0]
    
    def reset(self, start_vertex:str=False, blocked_verticies:list[str]=[]):
        if start_vertex:
            self.start_vertex = start_vertex

        self.current_vertex = self.start_vertex
        self.blocked_verticies = blocked_verticies
        
        self.vertex_info = {}   # ? [TIME CONSUMED, VERTEX BEFORE, EXPLORED]
        self.vertex_info[self.current_vertex] = [0, self.current_vertex, True]
        for i in list(self.map.keys()):
            if i == self.current_vertex:
                continue
            
            if i in self.blocked_verticies:
                self.vertex_info[i] = [float('inf'), False, True]
                continue
            
            self.vertex_info[i] = [float('inf'), False, False]
        
    def route(self, vertex:str):
        route_str = vertex
        route = [vertex]

        current_vertex = vertex
        while current_vertex != self.start_vertex:
            if self.vertex_info[current_vertex][2] == False:
                break
            
            route_str = self.vertex_info[current_vertex][1] + " > " + route_str
            route.append(self.vertex_info[current_vertex][1])
            current_vertex = self.vertex_info[current_vertex][1]
            
        return [route_str, route]
    
    def verticies(self) -> list[str]:
        return list(self.map.keys())
    


world = World(info)

max_iteration = 30
def find_route(world:World, target:str, start:str=False, blocked_verticies:list[str]=[]) -> list[3]:
    print(f" {"_"*38} ")
    print(f"|{"Data":^38}|")
    print(f"|{"-"*38}|")
    for [i, j] in map_formatter(world.map).items():
        print(f"|{f"{i}":<19}:{f"{j} Minutes":<18}|")
    print(f"|{"_"*38}|")
    
    if start or len(blocked_verticies) > 0:
        world.reset(start, blocked_verticies)

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
                    # ! DEBUGGING ONLY
                    # print(i+" : ", end="")
                    # print(world.vertex_info[i])
                    choosen_route = i
                    fastest_route = time_consumed

        if choosen_route == "":
            print("Out of route!")
            return [False, False, False]

        print(world.goto(choosen_route))
        
        if world.current_vertex == target:
            time_traveled = world.vertex_info[target][0]
            route = world.route(target)
            algo_time = ceil(((time()-clock)*10000000))/10000000
            print(f"\nDONE! Algorithm Time : {algo_time} seconds, Time Traveled : {time_traveled} minutes, Iteration : {index}, Route : {route[0]}")
            return [route[1], time_traveled, algo_time]
        
        index+=1


# find_route(world, start="G", target="B", blocked_verticies=["E", "D", "F"])
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

buttons_info:dict[str, list] = {}

def is_a_friend_of_element(arr:list, element_1, element_2):
    for index, i in enumerate(arr):
        if i == element_1:
            try:
                if arr[index+1] == element_2:
                    return True
            except IndexError:
                pass
            
            try:
                if arr[index-1] == element_2:
                    return True
            except IndexError:
                pass
            
    return False

def set_text(string, coordx, coordy, fontSize:int=36, color:tuple[3]=[0, 0, 0]): #Function to set text
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def draw_line(screen, start_pos:tuple[2], end_pos:tuple[2], line_width:int=5, color:tuple[3]=(0, 0, 0)):
    pygame.draw.line(screen, color, start_pos, end_pos, line_width)


def set_button(screen, x:int, y:int, width:int, height:int, button_id:str, text:str="", font:int=36, button_color:tuple[3]=(220, 220, 220), text_color:tuple[3]=(50, 50, 50), hover_button_color:tuple[3]=False, hover_text_color:tuple[3]=False):

    if not hover_button_color:
        hover_button_color = button_color
        
    if not hover_text_color:
        hover_text_color = text_color

    if button_id in buttons_info:
        if buttons_info[button_id]["hovered"]:
            button_color = hover_button_color
            text_color = hover_text_color
            
    draw_rect = lambda: pygame.draw.rect(screen, button_color, (x, y, width, height))


    font = pygame.font.Font(None, font)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width / 2, y + height / 2)

    if button_id not in buttons_info:
        buttons_info[button_id] = {
            "bound_x":[x, (x+width)],
            "bound_y":[y, (y+height)],
            "hovered":False
        }

    return (text_surface, text_rect, draw_rect)


def draw_circle(surface, center:tuple[2], text:str, color:tuple[3]=(220, 220, 220), radius:int=80, text_color:tuple[3]=(0, 0, 0), button_id:str=False, hover_button_color:tuple[3]=False, hover_text_color:tuple[3]=False, ):
    if not hover_button_color:
        hover_button_color = color
        
    if not hover_text_color:
        hover_text_color = text_color
    
    if button_id:
        
        if button_id in buttons_info:
            if buttons_info[button_id]["hovered"]:
                color = hover_button_color
                text_color = hover_text_color

        if button_id not in buttons_info:
            buttons_info[button_id] = {
                "bound_x":[(center[0]-floor(radius/2)), (center[0]+ceil(radius/2))],
                "bound_y":[(center[1]-floor(radius/2)), (center[1]+ceil(radius/2))],
                "hovered":False
            }
        
    
    pygame.draw.circle(surface, color, center, radius)
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = center
    surface.blit(text_surface, text_rect)


# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

grab_a_vertex = False
get_vertex_name = False
current_vertex_name = ""
current_vertex_info = {}
verticies_info = {}


draw_a_connection = False
start_connection_pos = ()
start_connection_vertex = ""
end_connection_vertex = ""
connections = {}
get_connection_edge = False
connection_edge = 0
connections_info = {}

state_message = ""
message = ""
message_delay = 0

target_vertex = False
start_vertex = False
find_route_state = False

block_a_vertex_state = False
blocked_verticies = []

click_start = time()
delay_click = 0.5

vertex_rad = 70

route = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                pygame.quit()
                break
            
            if event.key == pygame.K_SPACE:
                print("Conenctions : ")
                for connection in connections:
                    start_current_connection_vertex = connection.split("-")[0]
                    end_current_connection_vertex = connection.split("-")[1]
                    print(start_current_connection_vertex)
                    print(end_current_connection_vertex)
                    print(start_current_connection_vertex in route and end_current_connection_vertex in route)
                print("--------------")
                print(route)
                print("--------------")
            
            if get_vertex_name:
                del verticies_info[current_vertex_name]
                # print(current_vertex_name)
                
                if event.key == pygame.K_BACKSPACE:
                    current_vertex_name = current_vertex_name[:-1]
                elif event.unicode in string.ascii_letters:
                    current_vertex_name += event.unicode

                verticies_info[current_vertex_name] = current_vertex_info # ! IMPORTANT TO ESCAPE VERTEX
                if event.key == pygame.K_RETURN:
                    get_vertex_name = False
                    current_vertex_name = ""
                    
            
            elif get_connection_edge:
                # print("Get Connection Edge : ", connection_edge)
                if event.key == pygame.K_ESCAPE:
                    del connections_info[f"{start_connection_vertex}-{end_connection_vertex}"]
                    del connections[f"{start_connection_vertex}-{end_connection_vertex}"]
                    get_connection_edge = False
                    state_message = ""
                    connection_edge = 0
                    
                elif event.unicode in string.digits:
                    connection_edge *= 10
                    connection_edge += int(event.unicode)
                    
                if event.key == pygame.K_BACKSPACE:
                    connection_edge = floor(connection_edge / 10)

                connections_info[f"{start_connection_vertex}-{end_connection_vertex}"] = connection_edge
                # print(connections_info)

                if event.key == pygame.K_RETURN:
                    state_message = ""
                    get_connection_edge = False
                    connection_edge = 0

            
        elif event.type == pygame.MOUSEBUTTONDOWN and (time()-click_start) > delay_click:
            if event.button == 1:
                # print("CLICK!")
                x, y = event.pos[0], event.pos[1]

                its_a_button = False
                for key in buttons_info:
                    value = buttons_info[key]
                    if value["bound_x"][0] < x < value["bound_x"][1] and value["bound_y"][0] < y < value["bound_y"][1]: 
                        its_a_button = True

                        if key == "add_vertex":
                            block_a_vertex_state = False
                            find_route_state = False
                            state_message = ""
                            if get_vertex_name:
                                verticies_info[current_vertex_name] = current_vertex_info
                                get_vertex_name = False
                                current_vertex_name = ""
                                
                            
                            grab_a_vertex = True
                            if "" in verticies_info:
                                del verticies_info[""]
                        
                        elif key == "find_route":
                            if len(connections_info) < 2:
                                message = "Berikan Koneksi Minimal 2!"
                                message_delay = time() + 2
                                continue
                            
                            find_route_state = True
                            state_message = "Pilih posisi awal!"
                            
                            if block_a_vertex_state:
                                block_a_vertex_state = False
                            
                        elif key == "reset_sim":
                            start_vertex = ""
                            target_vertex = ""
                            block_a_vertex_state = False
                            find_route_state = False
                            state_message = ""
                            route = []
                            for i in verticies_info:
                                if verticies_info[i]["tags"] != "blocked":
                                    verticies_info[i]["state"] = "unexplored"
                                    verticies_info[i]["tags"] = "city"

                        elif key == "reset_tags":
                            start_vertex = ""
                            target_vertex = ""
                            blocked_verticies = []
                            block_a_vertex_state = False
                            find_route_state = False
                            state_message = ""
                            route = []
                            for i in verticies_info:
                                verticies_info[i]["state"] = "unexplored"
                                verticies_info[i]["tags"] = "city"
                                
                        elif key == "block_vertex":
                            block_a_vertex_state = True
                            state_message = "Block tempat!"
                            if find_route_state:
                                find_route_state = False

                                if start_vertex:
                                    verticies_info[start_vertex]["state"] = "unexplored"
                                    verticies_info[start_vertex]["tags"] = "city"
                                    start_vertex = ""
                                    
                                if target_vertex:
                                    verticies_info[target_vertex]["state"] = "unexplored"
                                    verticies_info[target_vertex]["tags"] = "city"
                                    target_vertex = ""
                                
                                

                        elif key == "reset_all":

                            grab_a_vertex = False
                            get_vertex_name = False
                            current_vertex_name = ""
                            current_vertex_info = {}

                            draw_a_connection = False
                            start_connection_pos = ()
                            start_connection_vertex = ""
                            end_connection_vertex = ""
                            connections = {}
                            get_connection_edge = False
                            connection_edge = 0
                            connections_info = {}
                            verticies_info = {}
                            buttons_info = {}

                            state_message = ""
                            message = ""
                            message_delay = 0

                            target_vertex = False
                            start_vertex = False
                            find_route_state = False

                            block_a_vertex_state = False
                            blocked_verticies = []
                            
                            verticies_info = {}
                            route = []
                            break
                        
                        elif key.startswith("vertex_") and not grab_a_vertex:
                            # print("KEY : ", key)
                            vertex = key.split("_", 2)[1]


                            if block_a_vertex_state:
                                if vertex in blocked_verticies:
                                    del blocked_verticies[vertex]
                                    verticies_info[vertex]["tags"] = "city"
                                else:
                                    blocked_verticies.append(vertex)
                                    verticies_info[vertex]["tags"] = "blocked"

                            elif find_route_state:
                                if not start_vertex:
                                    verticies_info[vertex]["state"] = "explored"
                                    verticies_info[vertex]["tags"] = "start"
                                    start_vertex = vertex
                                    state_message = "Pilih posisi target!"

                                elif not target_vertex:
                                    if start_vertex == vertex:
                                        continue
                                    verticies_info[vertex]["tags"] = "target"
                                    target_vertex = vertex
                                    state_message = ""
                                    
                                    world = World(map_deformatter(connections_info))
                                    route, time_traveled, time_algo = find_route(world, start=start_vertex, target=target_vertex, blocked_verticies=blocked_verticies)
                                    message = "Path Consume : "+str(time_traveled)
                                    message_delay = 0
                                    
                                    if not route:
                                        message = "Tidak ada jalan!"
                                        message_delay = time()+10
                                        
                                    else:
                                        for i in verticies_info:
                                            if i in route:
                                                verticies_info[i]["tags"] = "route"

                                    
                            elif draw_a_connection:
                                if f"{vertex}-{start_connection_vertex}" in connections:
                                    del connections[f"{vertex}-{start_connection_vertex}"]
                                    
                                connections[(start_connection_vertex+"-"+vertex)] = [start_connection_pos, (x,y)]
                                connections_info[(start_connection_vertex+"-"+vertex)] = 0
                                print("CONNECT!")
                                end_connection_vertex = vertex
                                draw_a_connection = False
                                get_connection_edge = True
                                state_message = "Masukkan berat!"
                                connection_edge = 0
                                print("CONNECTION_EDGE : ", connection_edge)
                            else:
                                print("CONNECTING. . .")
                                start_connection_vertex = vertex
                                draw_a_connection = True
                                start_connection_pos = (x, y)
                
                if its_a_button:
                    if get_vertex_name == True:
                        verticies_info[current_vertex_name] = current_vertex_info # ! IMPORTANT TO ESCAPE GETTING VERTEX NAME
                        get_vertex_name = False
                        current_vertex_name = ""
                        state_message = ""
                            
                            
                        
                if not its_a_button:
                    if grab_a_vertex:
                        get_vertex_name = True
                        state_message = "Masukkan nama!"
                        mouse_pos = pygame.mouse.get_pos()
                        current_vertex_info = {
                            "pos":mouse_pos,
                            "state":"unexplored",
                            "tags":"city"
                        }
                        verticies_info[""] = current_vertex_info
                        grab_a_vertex = False
                            

    mouse_pos = pygame.mouse.get_pos()
    for key in buttons_info:
        x = mouse_pos[0]
        y = mouse_pos[1]
        value = buttons_info[key]
        if value["bound_x"][0] < x < value["bound_x"][1] and value["bound_y"][0] < y < value["bound_y"][1]: 
            buttons_info[key]["hovered"] = True
        else:
            buttons_info[key]["hovered"] = False

    if not running:
        break
    
    # fill the screen with a color to wipe away anything from last frame
    title = set_text("Route Finding", 250, 50, 40, (55, 55, 55))
    add_vertex_button = set_button(screen, text="Add", x=(WIDTH-250), y=(HEIGHT-150), width=230, height=50, button_id="add_vertex", button_color=(40, 40, 40), text_color=(200, 200, 200), hover_button_color=(100, 100, 100))
    find_route_button = set_button(screen, text="Find Route!", x=(WIDTH-250), y=(HEIGHT-250), width=230, height=50, button_id="find_route", button_color=(40, 100, 200), text_color=(200, 200, 200), hover_button_color=(60, 150, 250))
    reset_all_button = set_button(screen, text="Reset All", x=(WIDTH-250), y=(HEIGHT-350), width=230, height=50, button_id="reset_all", button_color=(200, 40, 40), text_color=(200, 200, 200), hover_button_color=(250, 100, 60))
    reset_tags_button = set_button(screen, text="Reset Tags", x=(WIDTH-250), y=(HEIGHT-450), width=230, height=50, button_id="reset_tags", button_color=(200, 40, 40), text_color=(200, 200, 200), hover_button_color=(250, 100, 60))
    reset_sim_button = set_button(screen, text="Reset Simulation", x=(WIDTH-250), y=(HEIGHT-550), width=230, height=50, button_id="reset_sim", button_color=(200, 40, 40), text_color=(200, 200, 200), hover_button_color=(250, 100, 60))
    block_button = set_button(screen, text="Block Vertex", x=(WIDTH-250), y=(HEIGHT-650), width=230, height=50, button_id="block_vertex", button_color=(255, 0, 0), text_color=(0, 0, 0), hover_button_color=(255, 100, 100))

    screen.fill("gray")
    screen.blit(title[0], title[1]) # ? Title
    draw_line(screen, (100, 80), (420, 80), color=(55, 55, 55)) # ? Line

    # ? Add Vertex Button
    add_vertex_button[2]() # ? Add Vertex Button Rect
    screen.blit(add_vertex_button[0], add_vertex_button[1]) # ? Add Vertex Button Text

    # ? Add Find Route Button
    find_route_button[2]() # ? Add Find Route Rect
    screen.blit(find_route_button[0], find_route_button[1]) # ? Add Find Route Text
    
    # ? Add Reset Tags Button
    reset_tags_button[2]() # ? Add Vertex Button Rect
    screen.blit(reset_tags_button[0], reset_tags_button[1]) # ? Add Vertex Button Text

    # ? Add Reset Tags Button
    reset_sim_button[2]() # ? Add Vertex Button Rect
    screen.blit(reset_sim_button[0], reset_sim_button[1]) # ? Add Vertex Button Text

    # ? Add Reset All Button
    reset_all_button[2]() # ? Add Vertex Button Rect
    screen.blit(reset_all_button[0], reset_all_button[1]) # ? Add Vertex Button Text

    # ? Add Block Button
    block_button[2]() # ? Add Vertex Button Rect
    screen.blit(block_button[0], block_button[1]) # ? Add Vertex Button Text
    

    if grab_a_vertex:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (20, 20, 20), mouse_pos, vertex_rad)

    # ? ========== DRAW CONNECTIONS ============ ? #
    for connection in connections:
        start = connections[connection][0]
        end = connections[connection][1]

        start_current_connection_vertex = connection.split("-")[0]
        end_current_connection_vertex = connection.split("-")[1]

        line_color = (10, 10, 10)
        

        if route:
            if start_current_connection_vertex in route and end_current_connection_vertex in route:
                if is_a_friend_of_element(route, start_current_connection_vertex, end_current_connection_vertex):
                    # print(start_current_connection_vertex, " - ", end_current_connection_vertex)
                    line_color = (10, 150, 200)
                
        pygame.draw.line(screen, line_color, start, end, 4)
             
        
        current_connection_edge = connections_info[connection]
        text_coord = [(start[0]+(end[0] - start[0]) // 2), (start[1]+(end[1] - start[1]) // 2)]
        text = set_text(str(current_connection_edge), text_coord[0], text_coord[1])
        screen.blit(text[0], text[1])

    if draw_a_connection:
        # print("LINING. . .")
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (10, 10, 10), start_connection_pos, mouse_pos, 4)
        
    # ? ========== DRAW VERTICIES ============ ? #
    for vertex in verticies_info:
        position = verticies_info[vertex]["pos"]
        vertex_color = (60, 60, 60)
        vertex_hover_color = (80, 80, 80)
        if vertex == start_vertex:
            vertex_color = (0, 200, 10)
            vertex_hover_color = (10, 250, 40)
        elif vertex == target_vertex:
            vertex_color = (181, 103, 0)
            vertex_hover_color = (250, 103, 0)
        elif verticies_info[vertex]["tags"] == "route":
            vertex_color = (0, 91, 94)
            vertex_hover_color = (0, 91, 94)
        elif verticies_info[vertex]["tags"] == "blocked":
            vertex_color = (100, 0, 0)
            vertex_hover_color = (120, 20, 20)
            
        draw_circle(screen, text=vertex, color=vertex_color, text_color=(220, 220, 220), center=position, radius=vertex_rad, button_id=("vertex_"+vertex if vertex != "" else False), hover_button_color=vertex_hover_color)
        
        
    if message:
        msg = set_text(message, (WIDTH//2), HEIGHT-25, 24)
        screen.blit(msg[0], msg[1])

        if time() - message_delay >= 0 and message_delay != 0:
            message = ""
            
    if state_message:
        msg = set_text(str(state_message), (WIDTH//2), 25, 24, (20, 20, 20))
        screen.blit(msg[0], msg[1])
        

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()