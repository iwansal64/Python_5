# VERSION 3 : ADDING ANTI-DEAD-END AND MAKE THIS CODE READABLE

import numpy as np
from time import sleep
from os import system
import math

T = "T" # Target
P = "P" # Player
S = " " # Space
W = "-" # Walked
O = "X" # Obstacle
BLOCKED_PATH = "*" # Obstacle
BORDER = " "
DELAY_BETWEEN_FRAME = 0.5

class World:
    def __init__(self, matrix:list):
        if(len(np.array(matrix).shape) != 2):
            raise NotImplementedError("Cannot create an instance of this class")
        
        markup = [False, False, False]
        for i in matrix:
            for j in i:
                if j == P:
                    markup[0] = True
                elif j == T:
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

# ! ====== ANTI-DEAD-END ====== ! #
# # * ---- First Case ----
# world = World([
#     [O, O, T, O, O, S],
#     [O, S, S, O, S, O],
#     [O, S, S, O, S, P],
#     [O, O, O, S, S, S]
# ])

# # * --- Second Case ----
# world = World([
#     [O, O, T, O, S, O],
#     [O, S, S, O, S, O],
#     [O, S, S, O, S, S],
#     [O, O, O, S, O, P]
# ])


pos = [0, 0]
max_iteration = 10
path_history = [] # (V.3)

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
        if(current_object == S or current_object == T):                                             # ? Cek objek apakah dia bisa dilewati atau gak
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
    try:
        world = move_player(world, path_history[index], player_pos, BLOCKED_PATH)
    except IndexError:
        return False
    player_pos = find_pos(world)
    if True not in ([i[1] for i in check_surround(world, player_pos)]):
        return rewind(world, player_pos, index-1)

    return world
    

def find_path(world:World):
    '''Finding Closest Path! : FUNGSI UTAMA DARI PATHFINDING'''
    global path_history
    
    current_position = []                                                           # ? Berisi informasi mengenai posisi dari Player
    target_pos = find_pos(world, T)                                                 # ? Berisi informasi mengenai posisi dari Target
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
            
            distance = [abs(pos[0]-target_pos[0]), abs(pos[1]-target_pos[1])]       # ? Jarak antara posisi yang boleh ditempati di iterasi sekarang dengan posisi target
            sum_distance = distance[0]+distance[1]                                  # ? Jumlah jarak antara jauhnya posisi y dan jauhnya posisi x
            
            if(min_distance > sum_distance):                                        # ? Jika 'flags' lebih besar dari jarak sekarang
                min_distance = sum_distance                                         # ? Maka jarak sekarang akan menjadi 'flags'
                next_position = pos                                                 # ? dan posisi sekarang akan menjadi calon next_position

        # ===========================================
                
        if min_distance == float('inf'):                                            # ? jika 'flags' tidak ada perubahan sama sekali
            world = rewind(world, current_position)                                 # ? itu berarti tidak ada jalan sama sekali maka gunakan fungsi rewind karena dalam posisi terjebak
            if not world:                                                           # ? jika fungsi Rewind mengembalikan FALSE yang artinya tidak ada jalan
                print("KAMU MENJEBAK SAYA KOCAK!")                                  # ? Maka selesai karena tidak ada jalan sama sekali
                break                                                               # ? Keluar loop
            continue
                
        world = move_player(world, next_position, current_position)
        print(world.show_clean())                                           # ? Menampilkan gambar map dalam WORLD
        path_history.append(current_position)
        
        
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




