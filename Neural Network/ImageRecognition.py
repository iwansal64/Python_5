import pygame
from math import ceil
from time import time

def set_text(string, coordx, coordy, fontSize:int=36, color:tuple[3]=[0, 0, 0]): #Function to set text
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def removed_duplicate(arr:list):
    retval = []
    for i in arr:
        if i not in retval : retval.append(i)

    return retval

image_keys = {
    "line straight": {
        "key":[
            ["-", "-"]
        ],
        "index": [0, 0],
        "last_map_index": 0,
        "next_row":False
    },
    "line down": {
        "key":[
            ["-"],
            ["-"]
        ],
        "index": [0, 0],
        "last_map_index": 0,
        "next_row":False
    },
    "square": {
        "key":[
            ["-", "-"],
            ["-", "-"]
        ],
        "index": [0, 0],
        "last_map_index": 0,
        "next_row":False
    }
}


def recognize_image(mat:list[list[str]]):
    recognized_images = []
    for i in range(len(mat)):
        for j in image_keys:
            image_keys[j]["next_row"] = False
            
        iteration = 0
        for j in mat[i]:
            for image_key in image_keys:
                index = image_keys[image_key]["index"]
                key = image_keys[image_key]["key"]
                if index[0] <= len(key[index[1]])-1 and key[index[1]][index[0]] == j and not image_keys[image_key]["next_row"]:
                    print("MAYAN!")
                    image_keys[image_key]["index"][0] += 1
                    if(image_keys[image_key]["index"][0] == len(key[image_keys[image_key]["index"][1]]) and image_keys[image_key]["index"][1] == len(key)-1):
                        recognized_images.append(image_key)
                else:
                    # image_keys[image_key]["index"][0] = 0
                    if index[1] < len(key)-1 and index[0] > 0:
                        print("NEXT")
                        image_keys[image_key]["index"][1] += 1
                        image_keys[image_key]["index"][0] = 0
                        image_keys[image_key]["next_row"] = True
                        image_keys[image_key]["last_map_index"] = iteration
                    elif not image_keys[image_key]["next_row"] and image_keys[image_key]["last_map_index"] == iteration:
                        print("TIDAK GACOR")
                        image_keys[image_key]["index"][0] = 0
                        image_keys[image_key]["index"][1] = 0
            
            iteration += 1
                        
                
    return recognized_images



matrix = [
    [" ", " ", " ", " ", " "],
    ["-", "-", " ", " ", " "],
    ["-", "-", " ", " ", " "],
    ["-", "-", " ", " ", " "],
    ["-", "-", " ", " ", " "],
]

print(recognize_image(matrix))

pygame.init()


CELL_WIDTH = 50
CELL_HEIGHT = 50
CELL_GAP = 10
WIDTH = 900
HEIGHT = 900

grid_width = len(matrix[0])*(CELL_WIDTH+CELL_GAP)
grid_height = len(matrix)*(CELL_HEIGHT+CELL_GAP)
grid_start_x = (WIDTH//2)-(grid_width//2)
grid_start_y = (HEIGHT//2)-(grid_height//2)


message = ""
message_time = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
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
                        matrix[x_index][y_index] = "-"
                    elif event.button == 3:
                        matrix[x_index][y_index] = " "

                    show_path = False
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                break
            elif event.key == pygame.K_SPACE:
                recognized_image = recognize_image(matrix)
                print(recognized_image)
                for i in removed_duplicate(recognized_image):
                    message = i+" "
                    message_time = time()+2



    if not running:
        break

    screen.fill("gray")
    
    # ? Grid Creation
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            color = (255, 255, 255)
            if matrix[i][j] == "-":
                color = (0, 0, 0)

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
    
    
            
            
            
            