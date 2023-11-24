import pygame
import copy
from random import randint


WIDTH = 800
HEIGHT = 800
WIDTH_HALF = WIDTH//2
HEIGHT_HALF = HEIGHT//2

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

random_at_reset = True

#? ========== RANDOM DATA SETTINGS ========== ?#
rds = {
    "min_pos_x": 100,
    "max_pos_x": WIDTH-100,
    "min_pos_y": 100,
    "max_pos_y": HEIGHT-100,
    "min_dir_x": -1,
    "max_dir_x": 1,
    "min_dir_y": -1,
    "max_dir_y": 1,
    "min_speed_x": -5,
    "max_speed_x": 5,
    "min_speed_y": -5,
    "max_speed_y": 5,
    "min_color_r": 0,
    "max_color_r": 150,
    "min_color_g": 0,
    "max_color_g": 150,
    "min_color_b": 255,
    "max_color_b": 255
}

gravitation_force = 1
gravitation_radius = 150
sim_speed = 1

object_mass = 1
frame = 0

max_trail = 10
frame_per_trail = 1
trail_color = (255, 255, 255)

center_color = (100, 100, 100)
small_center_color = (0, 0, 0)
center_border_color = (255, 255, 255)

number_of_balls = 15

def get_ball_random_data():
    global rds
    global number_of_balls
    return [
    {
        "pos":[randint(rds["min_pos_x"], rds["max_pos_x"]), randint(rds["min_pos_y"], rds["max_pos_y"])],
        "dir":[randint(rds["min_dir_x"], rds["max_dir_x"]), randint(rds["min_dir_y"], rds["max_dir_y"])],
        "speed":[randint(rds["min_speed_x"], rds["max_speed_x"]), randint(rds["min_speed_y"], rds["max_speed_y"])],
        "last_pos":[],
        "color":(randint(rds["min_color_r"], rds["max_color_r"]), randint(rds["min_color_g"], rds["max_color_g"]), randint(rds["min_color_b"], rds["max_color_b"]))
    }
    for i in range(number_of_balls)]

first_pos_balls = get_ball_random_data()

# first_pos_balls = [
#     {
#         "pos": [260, 0],
#         "dir":[0, 1],
#         "speed":[0, 2],
#         "last_pos":[]
#     },
#     {
#         "pos": [500, 0],
#         "dir":[0, 1],
#         "speed":[0, 5],
#         "last_pos":[]
#     },
#     {
#         "pos": [450, 0],
#         "dir":[0, 1],
#         "speed":[0, 3],
#         "last_pos":[]
#     },
#     {
#         "pos": [250, 0],
#         "dir":[0, 1],
#         "speed":[0, 8],
#         "last_pos":[]
#     },
#     {
#         "pos": [150, 0],
#         "dir":[0, 1],
#         "speed":[0, 3],
#         "last_pos":[]
#     },
#     {
#         "pos": [650, 20],
#         "dir":[0, 1],
#         "speed":[0, 4],
#         "last_pos":[]
#     },
#     {
#         "pos": [350, 50],
#         "dir":[0, 1],
#         "speed":[0, 3],
#         "last_pos":[]
#     },
#     {
#         "pos": [500, 60],
#         "dir":[0, 1],
#         "speed":[0, 2],
#         "last_pos":[]
#     }
# ]

def sign(x:int) -> int:
    return 1 if x >= 0 else -1

balls = copy.deepcopy(first_pos_balls)

running = True
while running:
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, center_border_color, (WIDTH_HALF, HEIGHT_HALF), 100, 5)
    pygame.draw.circle(screen, center_color, (WIDTH_HALF, HEIGHT_HALF), 95)
    pygame.draw.circle(screen, small_center_color, (WIDTH_HALF, HEIGHT_HALF), 15, 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if random_at_reset:
                    balls = get_ball_random_data()
                else:
                    balls = copy.deepcopy(first_pos_balls)


    for index, i in enumerate(balls):
        pos = i["pos"]
        dir = i["dir"]
        speed = i["speed"]
        last_pos = i["last_pos"]
        color = i["color"]
        
        #? =========== TRAIL =========== #
        for p in last_pos:
            print(p[0])
            # pygame.draw.circle(screen, (200, 200, 200), (p[0], p[1]), 10)
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(p[0]-5, p[1]-5, 10, 10))
            
        print()
        pygame.draw.circle(screen, color, (pos[0], pos[1]), 10)

        #? =========== MOVE ========== #
        balls[index]["pos"][1] += speed[1]*sim_speed
        balls[index]["pos"][0] += speed[0]*sim_speed
        
        distance_from_center = [(WIDTH_HALF-balls[index]["pos"][0]), (HEIGHT_HALF-balls[index]["pos"][1])]
        
        if abs(distance_from_center[0]) <= gravitation_radius and abs(distance_from_center[1]) <= gravitation_radius:
            balls[index]["dir"][0] = round((sign(distance_from_center[0])-round(distance_from_center[0]/gravitation_radius, 2))*gravitation_force, 2)
            balls[index]["dir"][1] = round((sign(distance_from_center[1])-round(distance_from_center[1]/gravitation_radius, 2))*gravitation_force, 2)
            balls[index]["speed"][0] = (speed[0]+balls[index]["dir"][0])
            balls[index]["speed"][1] = (speed[1]+balls[index]["dir"][1])


            # print(distance_from_center)
            # print(balls[index]["dir"])
            # print(balls[index]["speed"])
            # print()
            
        if frame % frame_per_trail == 0:
            print("FRAME")
            balls[index]["last_pos"].append(copy.deepcopy(pos))
            if(len(balls[index]["last_pos"]) > max_trail):
                del balls[index]["last_pos"][0]
            
            # print(pos)
            # print()
            # print(balls[index]["last_pos"])
            
    
    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60
    frame+=1

pygame.quit()


