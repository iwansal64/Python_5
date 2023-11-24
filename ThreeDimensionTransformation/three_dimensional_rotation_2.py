import copy
x = [
    [
        [0, 1, 2],      # |
        [3, 4, 5],      # v
        [6, 7, 8]
    ],
    [
        [9, 10, 11],
        [12, 13, 14],   # <--
        [15, 16, 17]
    ],
    [
        [18, 19, 20],
        [21, 22, 23],   # ^
        [24, 25, 26]    # |
    ],
]

y = [
    [
        ["A", "A", "A"],
        ["B", "B", "B"],
        ["C", "C", "C"]
    ],
    [
        ["D", "D", "D"],
        ["E", "E", "E"],
        ["F", "F", "F"]
    ],
    [
        ["G", "G", "G"],
        ["H", "H", "H"],
        ["I", "I", "I"]
    ]
]

# ? ANOTHER CASE :
#       00      01
#         04      05
#       
#       02      03
#         06      07


# ? MAIN CASE :
#         00          01           02
#           09          10           11
#             18          19           20
#         
#         03          04           05
#           12          13          14
#             21          22          23
#         
#         06          07           08
#           15          16           17
#             24          25           26


# ! ============= ROTATED BY X AXIS ============= * #
#         18          19           20
#           21          22          23
#             24          25           26
#         
#         09          10           11
#----------[12]        [13]         [14]  --------------> X AXIS
#             15           16           17
#         
#         00          01           02
#           03          04           05
#             06          07           08

# ! ============= ROTATED BY Y AXIS ============= * #

#                       |
#                       |
#                       |
#         02          11|          20
#           01         [10]          19
#             00          09           18
#         
#         05          14           23
#           04         [13]          22
#             03          12           21
#         
#         08          17           26
#           07         [16]          25
#             06          15           24
#                        
#                       |
#                       |
#                       |
#                       V
#
#                    Y AXIS

# ! ============= ROTATED BY Z AXIS ============= * #
#         01          02           05    
#           10          11           14  
#             19          20           23
#                   \                    
#         00          04           08    
#           09          13           17   
#             18          22           26
#                           \            
#         03          06     _|    07    
#           12          15   Z AXIS  16  
#             21          24           25


def show_3d_array(arr:list[list[list]]):
    z_len = len(arr)
    y_len = len(arr[0])
    x_len = len(arr[0][0])

    if x_len != z_len != y_len or x_len <= 0:
        raise NotImplementedError("Size nya harus sama... misalkan 3x3x3 / 2x2x2 / 4x4x4")

    max_length = 0
    for i in range(len(arr)):
        if len(arr[i]) != y_len:
            raise NotImplementedError("Size nya harus sama... misalkan 3x3x3 / 2x2x2 / 4x4x4")

        for j in range(len(arr[i])):
            if len(arr[i][j]) != x_len:
                raise NotImplementedError("Size nya harus sama... misalkan 3x3x3 / 2x2x2 / 4x4x4")
            
            for k in arr[i][j]:
                if len(str(k)) > max_length:
                    max_length = len(str(k))
                    
    
    for i in arr:
        for index_j, j in enumerate(i):
            print(" "*(2*index_j), end="")
            for k in j:
                if len(str(k)) < max_length:
                    print("0"*(max_length-len(str(k))), end="")
                print(k, end="        ")
            print()
        print()
        

def half_rotate_x(arr:list[list[list]], reverse:bool=False) -> list[list[list]]:
    retval = copy.deepcopy(arr)
    
    corner_arr_error=[]
    temp_arr=[[0 for i in range(len(arr))], [0 for i in range(len(arr))]]
    
    for i in range(len(arr)):
        if i != 0 and i != (len(arr)-1):
            continue

        index = 0
        for j in (range(len(arr[0]))) if (i != 0 if reverse else i == 0) else (range(len(arr[0])-1, -1, -1)):
            if index == len(arr)-2 and (i != 0 if reverse else i == 0) or index == 1 and (i == 0 if reverse else i != 0):
                corner_arr_error.append(arr[i][j])
            
            temp_arr[1 if (j % 2 == 0) else 0] = retval[i][j]
            retval[i][j] = temp_arr[j % 2]
            
            index+=1

        
    for i in range(len(arr)-1, -1, -1) if reverse else range(len(arr)):
        temp_arr[1 if (i % 2 == 0) else 0] = arr[i][2]
        retval[i][2] = temp_arr[i % 2]

    for i in range(len(arr)) if reverse else range(len(arr)-1, -1, -1):
        temp_arr[1 if (i % 2 == 0) else 0] = arr[i][0]
        retval[i][0] = temp_arr[i % 2]
        
    if reverse:
        pass
        retval[0][0] = corner_arr_error[0]
        # retval[len(arr)-1][0] = corner_arr_error[1]
    else:
        retval[0][len(arr)-1] = corner_arr_error[0]
        retval[len(arr)-1][0] = corner_arr_error[1]
    
    
    return retval
    
def half_rotate_y(arr:list[list[list]], reverse:bool=False):
    retval = copy.deepcopy(arr)


    error_value = []

    temp = ["", ""]
    temp_index = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if j != 0:
                continue

            for k in range(len(arr[0][0])) if reverse else range(len(arr[0][0])-1, -1, -1):
                if k == 1:
                    error_value.append(arr[i][j][k])

                temp[temp_index] = arr[i][j][k]
                retval[i][j][k] = temp[not temp_index]
                temp_index = 0 if temp_index else 1
                
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if j != len(arr[0])-1:
                continue

            for k in range(len(arr[0][0])-1, -1, -1) if reverse else range(len(arr[0][0])):
                if k == len(arr[0][0])-2:
                    error_value.append(arr[i][j][k])
                    
                temp[temp_index] = arr[i][j][k]
                retval[i][j][k] = temp[not temp_index]
                temp_index = 0 if temp_index else 1

    for i in range(len(arr)):
        for j in range(len(arr[0])-1, -1, -1) if reverse else range(len(arr[0])):
            for k in range(len(arr[0][0])):
                if k != 0:
                    continue

                temp[temp_index] = arr[i][j][k]
                retval[i][j][k] = temp[not temp_index]
                temp_index = 0 if temp_index else 1
                
    for i in range(len(arr)):
        for j in range(len(arr[0])) if reverse else range(len(arr[0])-1, -1, -1):
            for k in range(len(arr[0][0])):
                if k != len(arr[0][0])-1:
                    continue

                temp[temp_index] = arr[i][j][k]
                retval[i][j][k] = temp[not temp_index]
                temp_index = not temp_index
                
    
    for i in range(len(arr)):
        if reverse:
            retval[i][0][len(arr[0])-1] = error_value[i]
            retval[i][len(arr[0])-1][0] = error_value[i+len(arr)]
            continue

        retval[i][0][0] = error_value[i]
        retval[i][len(arr[0])-1][len(arr[0][0])-1] = error_value[i+len(arr)]
            
    
    return retval

def half_rotate_z(arr:list[list[list]], reverse:bool=False):
    retval = copy.deepcopy(arr)
    
    error_value = []
    temp = ["", ""]
    temp_index = 0
    for i in range(len(arr)):
        if i != 0:
            continue
        
        for j in range(len(arr[0])):
            for k in range(len(arr[0][0])):
                if k == len(arr[0][0])-2:
                    error_value.append(arr[i][j][k])

                temp[temp_index] = arr[i][j][k]
                retval[i][j][k] = temp[not temp_index]
                temp_index = not temp_index

    for i in range(len(arr)):
        if i != len(arr)-1:
            continue
        
        for j in range(len(arr[0])):
            for k in range(len(arr[0][0])-1, -1, -1):
                if k == 1:
                    error_value.append(arr[i][j][k])
                    
                temp[temp_index] = arr[i][j][k]
                retval[i][j][k] = temp[not temp_index]
                temp_index = not temp_index
                
    for j in range(len(arr[0])):
        for k in range(len(arr[0][0])-1, -1, -1):
            temp[temp_index] = arr[k][j][0]
            retval[k][j][0] = temp[not temp_index]
            temp_index = not temp_index

    for j in range(len(arr[0])):
        for k in range(len(arr[0][0])):
            temp[temp_index] = arr[k][j][len(arr)-1]
            retval[k][j][len(arr)-1] = temp[not temp_index]
            temp_index = not temp_index

    for j in range(len(arr[0])):
        retval[0][j][len(arr[0][0])-1] = error_value[j]
        retval[len(arr)-1][j][0] = error_value[j+len(arr[0])]
    
    return retval
    
    
def rotate_x(arr:list[list[list]], reverse:bool=False) -> list[list[list]]:
    retval = half_rotate_x(arr, reverse)
    retval = half_rotate_x(retval, reverse)
    
    return retval

def rotate_y(arr:list[list[list]], reverse:bool=False) -> list[list[list]]:
    retval = half_rotate_y(arr, reverse)
    retval = half_rotate_y(retval, reverse)

    return retval

def rotate_z(arr:list[list[list]], reverse:bool=False) -> list[list[list]]:
    retval = half_rotate_z(arr, reverse)
    retval = half_rotate_z(retval, reverse)

    return retval

show_3d_array(x)
print("-"*30)
show_3d_array(half_rotate_z(x, True))








