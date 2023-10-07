# VERSION 1 : FIRST VERSION

import numpy as np
from time import sleep
from os import system

T = "T" # Target
P = "P" # Player
S = " " # Space
W = "-" # Walked
O = "X" # Obstacle
BORDER = "W"
DELAY_BETWEEN_FRAME = 0.2

class World:
    def __init__(self, matrix:list):
        if(len(np.array(matrix).shape) != 2):
            raise NotImplementedError("Cannot create an instance of this class")

        self.matrix = matrix
        self.index = 0

    def __len__(self):
        return len(self.matrix)

    def __iter__(self):
        self.index = 0
        return self  # Return the object itself as the iterator.

    def __next__(self):
        if self.index < len(self.matrix):
            result = self.matrix[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration  # Raise StopIteration to signal the end of iteration.

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, index, value):
            self.matrix[index] = value

    def __contains__(self, item):
        return item in self.matrix
    
    def __repr__(self):
        return (str) (np.array(self.matrix))
    
    def show_clean(self):
        mat = (self.__repr__()).replace("[", " ").replace("]", " ").replace("'", " ")
        retval = ((BORDER+"   ")*(2+len(self.matrix[0]))) + "\n"
        
        # Create a list to store each line of the final output
        lines = []

        mats = enumerate(mat.split("\n"))
        for index, i in mats:
            if(index != len(mat.split("\n"))-1):
                lines.append(BORDER + i + " " + BORDER)
                continue

            lines.append(BORDER + i + BORDER)
                

        # Join the lines with newlines to create the final output
        retval += "\n".join(lines)
        
        retval += "\n" + ((BORDER+"   ")*(2+len(self.matrix[0])))
        
        return retval



# # 3x3
# world = World([
#     [S, S, T],
#     [S, O, O],
#     [S, P, S]
# ])

# # 4x4 World
# world = World([
#     [O, T, O, S],
#     [S, S, O, O],
#     [O, O, S, O],
#     [P, S, S, S]
# ])

# 4x6 World
world = World([
    [O, O, T, O, O, S],
    [O, S, S, O, S, S],
    [O, S, S, O, S, P],
    [O, O, O, S, S, S]
])

pos = [0, 0]
max_iteration = 10

def check_surround(world:World, player_pos:list[2]) -> list[8]:
    '''Check Around Player'''
    object_list = []
    check_coordinate = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    for i in check_coordinate:
        current_object = ""

        y_object = player_pos[0]+i[0]
        x_object = player_pos[1]+i[1]
        

        
        if(y_object < 0 or y_object >= len(world) or x_object < 0 or x_object >= len(world[0])):
            object_list.append([[y_object, x_object], False])
            continue

        current_object = world[y_object][x_object]
        if(current_object == S or current_object == T):
            object_list.append([[y_object, x_object], True])
        else:
            object_list.append([[y_object, x_object], False])
            
    return object_list
        
    

def move_player(world:World, move_to:list[2:int], player_pos:list[2:int]):
    '''Moving Player to A Point'''
    clone_world = world

    clone_world[player_pos[0]][player_pos[1]] = W
    clone_world[move_to[0]][move_to[1]] = P

    return clone_world



def find_pos(world:World, target:str=P) -> list[2]:
    '''Find Something in World'''
    for index, i in enumerate(world):
        for index2, j in enumerate(i):
            if j == target:
                return [index, index2]
                

def find_path(world:World):
    '''Finding Closest Path!'''
    system("cls")

    print(world.show_clean())
    current_pos = []
    target_pos = find_pos(world, T)
    index = 0

    sleep(DELAY_BETWEEN_FRAME+0.5)
    while True:
        system("cls")
        current_pos = find_pos(world)
        
        checked_positions = check_surround(world, current_pos)
        
        min_distance = 1000
        next_position = []
        for [pos, state] in checked_positions:
            if state == False:
                continue
            
            distance = [abs(pos[0]-target_pos[0]), abs(pos[1]-target_pos[1])]
            sum_distance = distance[0]+distance[1]
            
            if(min_distance > sum_distance):
                min_distance = sum_distance
                next_position = pos
                
        world = move_player(world, next_position, current_pos)
        
        
        print(world.show_clean())
        if find_pos(world) == target_pos:
            print("GOTCU!")
            break
        
        if index >= max_iteration:
            print(":(")
            break
        
        index+=1
        print("\n\n")
        sleep(DELAY_BETWEEN_FRAME)


# print(np.array(check_surround(world, find_pos(world)), dtype=object))
find_path(world)
# print(world.show_clean())
# move_player(world, [1, 2], find_pos(world))
# print(world)
# move_player(world, [0, 1], find_pos(world))
# print(world)
# move_player(world, [0, 0], find_pos(world))
# print(world)









