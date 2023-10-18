# VERSION 3 : IMPROVE ALGORITHM

import numpy as np
from time import sleep
from os import system
import math

MT = "T" # Main Target
T = "S"  # Target
P = "P"  # Player
S = " "  # Space
W = "-"  # Walked
O = "X"  # Obstacle

CURSED_PATH = "*" # Obstacle
BORDER = " "
DELAY_BETWEEN_FRAME = 0.5
MAX_ITERATION = 30

class World:
    def __init__(self, matrix:list):
        if(len(np.array(matrix).shape) != 2):
            raise NotImplementedError("Cannot create an instance of this class")
        
        markup = [False, False, False]
        for i in matrix:
            for j in i:
                if j == P:
                    markup[0] = True
                elif j == MT:
                    markup[1] = True
                elif j == S:
                    markup[2] = True

        if False in markup:
            raise NotImplementedError("Ada yang ga beres nih matrix : Ada yang kureng")

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
    
    def replace(self, before:str, after:str):
        for index1, i in enumerate(self.matrix):
            for index2, j in enumerate(i):
                if j == before:
                    self.matrix[index1][index2] = after
                    
    



# # 3x3
# world = World([
#     [S, S, MT],
#     [S, O, O],
#     [S, P, S]
# ])

# # 4x4 World
# world = World([
#     [O, MT, O, S],
#     [S, S, O, O],
#     [O, O, S, O],
#     [P, S, S, S]
# ])

# ! ====== ANTI-DEAD-END ====== ! #
# # * ---- First Case ----
# world = World([
#     [O, O, MT, O, O, S],
#     [O, S, S, O, S, O],
#     [O, S, S, O, S, P],
#     [O, O, O, S, S, S]
# ])

# # * --- Second Case ----
# world = World([
#     [O, O, MT, O, S, O],
#     [O, S, S, O, S, O],
#     [O, S, S, O, S, S],
#     [O, O, O, S, O, P]
# ])

# ! ====== ANTI-INEFFICIENT ====== ! #
# # # * ----- First Case -----
# world = World([
#     [O, O, S, O, S, O],
#     [O, S, S, S, S, P],
#     [O, S, S, O, S, S],
#     [O, O, MT, O, S, S]
# ])

# # # * ----- Second Case -----
# world = World([
#     [O, O, S, O, S, O],
#     [O, S, S, S, S, P],
#     [O, S, S, O, S, S],
#     [O, S, S, O, S, S],
#     [O, O, MT, O, S, S]
# ])

# # # * ----- Third Case -----
# world = World([
#     [O, O, S, O, S, O],
#     [O, S, MT, O, S, P],
#     [O, S, S, O, S, O],
#     [O, S, S, O, S, S],
#     [O, O, S, S, S, S]
# ])

# # * ----- Fourth Case -----
world = World([
    [S, S, S, S, S, O],
    [S, O, O, O, S, O],
    [S, O, S, P, S, O],
    [S, O, S, S, S, O],
    [MT, O, O, O, O, O]
])


pos = [0, 0]
path_history = [] # (V.3)
last_distance_to_start_pos = 0 # (V.4)
start_pos = [] # (V.4)

def check_surround(world:World, player_pos:list[2]) -> list[8]:
    '''Check Around Player : Fungsi yang bertugas untuk mengecek sekeliling nya. Mengembalikan array yang berisi posisi dan bisa atau tidaknya'''
    object_list = []                                                                                # ? ISI NYA : [POSISI, BOLEH DILEWATI ATAU GAK]. CONTOH : [[[3, 2], True], [[3, 3], False]]
    check_coordinate = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]       # ? arah dari posisi yang mau dicek
    for i in check_coordinate:
        current_object = ""                                                                         # ? liat object nya apa.. apakah Player atau Target atau Space atau Obstacle

        y_object = player_pos[0]+i[0]                                                               # ? kordinat dari posisi yang ingin dicek setelah dijumlahkan dengan vektor arah
        x_object = player_pos[1]+i[1]                                                               # ? sama aja kordinat dari posisi yang ingin di cek di x axis
        

        
        if(y_object < 0 or y_object >= len(world) or x_object < 0 or x_object >= len(world[0])):    # ? Cek apakah posisi nya diluar batas dari matrix atau ga
            object_list.append([[y_object, x_object], False])                                       # ? Jika iya maka langsung tidak diperbolehkan lewat situ!
            continue                                                                                # ? Balik lagi ke atas

        current_object = world[y_object][x_object]                                                  # ? Ambil objek yang sedang berada di posisi tertentu dalam iterasi sekarang x_object dan y_object
        if(current_object == S or current_object == MT or current_object == T):                                             # ? Cek objek apakah dia bisa dilewati atau gak
            object_list.append([[y_object, x_object], True])                                        # ? Jika iya maka TRUE
        else:
            object_list.append([[y_object, x_object], False])                                       # ? Jika tidak maka FALSE

    return object_list                                                                              # ? Mengembalikan info yang kita dapatkan
        
    

def move_player(world:World, move_to:list[2:int], player_pos:list[2:int], swapped_object:str=W):
    '''Moving Player to A Point : Memindahkan posisi player ke posisi yang diinginkan'''

    world[player_pos[0]][player_pos[1]] = swapped_object    # ? Ubah objek di posisi player dari tadinya player menjadi path yang sudah dijelajahi
    world[move_to[0]][move_to[1]] = P                       # ? Ubah objek di posisi yang di tentukan dari tadinya path kosong jadi player

    return world                                            # ? Mengembalikan world yang sudah diubah



def find_pos(world:World, target:str=P) -> list[2]:
    '''Find Something in World : Mengecek apakah di world ada suatu objek tertentu'''
    for index, i in enumerate(world):   # ? Loop pertama adalah ROW (Y) berisi banyak COLUMN (X)
        for index2, j in enumerate(i):  # ? Loop kedua adalah COLUMN (X) berisi banyak objek
            if j == target:             # ? Memeriksa apakah objek sesuai dengan objek yang ditentukan
                return [index, index2]  # ? Mengembalikan posisi dari objek
            
    return False                        # ? Jika tidak ketemu mengembalikan FALSE

def rewind(world:World, player_pos:list, index:int=-1):
    '''(V.3) Rewind if stucked!'''
    global path_history
    
    try:
        world = move_player(world, path_history[index], player_pos, CURSED_PATH)
    except IndexError:
        return [world, False]
    player_pos = find_pos(world)
    if True not in ([i[1] for i in check_surround(world, player_pos)]):
        return rewind(world, player_pos, index-1)

    print("REWINDED")
    sleep(0.5)
    return world

def put_target(world:World, position:list, start_pos:list, goto_start_pos:bool=True):
    '''(V.4) Put current target'''
    global path_history
    
    if goto_start_pos:
        player_pos = find_pos(world)
        world = move_player(world, start_pos, player_pos)
        path_history = []
        world[player_pos[0]][player_pos[1]] = CURSED_PATH
        

    world[position[0]][position[1]] = T

    print("PUT_TARGET")
    return world
    
def operate_two_list(a:list, b:list, operation):
    '''(V.4) Merging two list.. '''
    z = [i for i in range(len(a))]
    for i in range(len(a)):
        z[i] = operation(a[i], b[i])
        
    return z

def find_path(world:World):
    '''Finding Closest Path! : FUNGSI UTAMA DARI PATHFINDING'''
    global path_history, last_distance_to_start_pos
    
    start_pos = find_pos(world)
    
    current_position = []                                                           # ? Berisi informasi mengenai posisi dari Player
    target_pos = find_pos(world, MT)                                                 # ? Berisi informasi mengenai posisi dari Target
    index = 0                                                                       # ? Index yang akan dijumlahkan tiap pengulangan (iterasi)
    print(world.show_clean())                                                       # ? Menampilkan gambar map dalam WORLD

    while True:
        if index == 0:                                                              # ? Jika ini adalah iterasi pertama
            sleep(DELAY_BETWEEN_FRAME+0.5)                                          # ? Maka delay sebesar variable DELAY_BETWEEN_FRAME ditambahkan 0.5 (jadi lebih lama 0.5 detik) 
        system("cls")                                                               # ? Membersihkan layar yang dimana ini penting untuk membuat seolah world nya berjalan

        current_position = find_pos(world)                                          # ? Meng-update posisi dari Player

        checked_positions = check_surround(world, current_position)                 # ? Memeriksa objek sekitar player
        
        min_distance = float('inf')                                                 # ? Sebagai 'FLAGS' untuk mencari jarak terdekat
        next_position = []                                                          # ? Variable yang menyimpan posisi selajutnya

        # ========== PENGAMBILAN KEPUTUSAN ===========
        for [pos, state] in checked_positions:                                      # ? Mengambil satu satu elemen checked_position yang berisi posisi dan boleh ditempati atau ga
            if state == False:                                                      # ? Cek apakah boleh ditempati atau tidak
                continue                                                            # ? Jika tidak skip ke iterasi selanjutnya
            
            try:
                distance = [abs(pos[0]-target_pos[0]), abs(pos[1]-target_pos[1])]       # ? Jarak antara posisi yang boleh ditempati di iterasi sekarang dengan posisi target
            except:
                print(target_pos)
                raise Exception("BREAK")
            
            sum_distance = distance[0]+distance[1]                                  # ? Jumlah jarak antara jauhnya posisi y dan jauhnya posisi x
            
            if(min_distance > sum_distance):                                        # ? Jika 'flags' lebih besar dari jarak sekarang
                min_distance = sum_distance                                         # ? Maka jarak sekarang akan menjadi 'flags'
                next_position = pos                                                 # ? dan posisi sekarang akan menjadi calon next_position

        # ===========================================


        if min_distance == float('inf'):                                            # ? jika 'flags' tidak ada perubahan sama sekali
            world = rewind(world, current_position)                                 # ? itu berarti tidak ada jalan sama sekali maka gunakan fungsi rewind karena dalam posisi terjebak
            last_distance_to_start_pos = 0
            distance_to_start_pos = 0
            if world[1] == False:                                                           # ? jika fungsi Rewind mengembalikan FALSE yang artinya tidak ada jalan
                print("KAMU MENJEBAK SAYA KOCAK!")                                  # ? Maka selesai karena tidak ada jalan sama sekali
                print(world[0].show_clean())
                break                                                               # ? Keluar loop
            continue                                                                # ? Skip loop
        
        distance_to_start_pos = operate_two_list(next_position, start_pos, lambda x,y:abs(x-y))
        distance_to_start_pos = distance_to_start_pos[0]+distance_to_start_pos[1]
        
        # ! ================ (V4 Inefficient-Improvement) ================== ! #
        if(distance_to_start_pos <= last_distance_to_start_pos):
            target_pos = next_position
            put_target(world, next_position, start_pos)
            world.replace("-", " ")
            last_distance_to_start_pos = 0
        else:
            world = move_player(world, next_position, current_position)
            last_distance_to_start_pos = distance_to_start_pos
            
            
                
        print(world.show_clean())                                           # ? Menampilkan gambar map dalam WORLD
        print(distance_to_start_pos <= last_distance_to_start_pos)
        path_history.append(current_position)
        
        
        if find_pos(world) == target_pos:
            if find_pos(world, MT):
                target_pos = find_pos(world, MT)
                print("Got target!")
            else:
                print("GOTCU!")
                break
        
        if index >= MAX_ITERATION:
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




