from tkinter import *
from typing import Union
from PIL import Image, ImageTk

root = Tk("Chess", "chess")
root.geometry("1000x1000+450+50")
root.title("Chess")
root.config(bg="#282c34")

pawn_size = (70, 70)
cell_size = 100
off_set_x = 50
off_set_y = 50

def key_press(event):
    key = event.char
    if key == 'q':
        root.destroy()

root.bind("<KeyPress>", key_press)

canvas = Canvas(root, width=900, height=900)

def rect(canvas: Canvas, pos: tuple[Union[int, None]], size: tuple[Union[int, None]], **kwargs):
    canvas.create_rectangle(pos[0], pos[1], pos[0] + size[0], pos[1] + size[1], **kwargs)

def resize_image(image_path, new_width, new_height):
    # Buka gambar dengan Pillow
    original_image = Image.open(image_path)

    # Resize gambar dengan antialiasing menggunakan thumbnail
    original_image.thumbnail((new_width, new_height))

    # Ubah gambar Pillow ke format Tkinter
    tk_image = ImageTk.PhotoImage(original_image)

    return tk_image



images_url = {
    "black": {
        "pawn":"./assets/BlackPawns/Pawn.png",
        "bishop":"./assets/BlackPawns/Bishop.png",
        "knight":"./assets/BlackPawns/Knight.png",
        "king":"./assets/BlackPawns/King.png",
        "queen":"./assets/BlackPawns/Queen.png",
        "rook":"./assets/BlackPawns/Rook.png"
    },
    "white": {
        "pawn":"./assets/WhitePawns/Pawn.png",
        "bishop":"./assets/WhitePawns/Bishop.png",
        "knight":"./assets/WhitePawns/Knight.png",
        "king":"./assets/WhitePawns/King.png",
        "queen":"./assets/WhitePawns/Queen.png",
        "rook":"./assets/WhitePawns/Rook.png"
    }
}

pawn = ["black_pawn", "white_pawn"]
bishop = ["black_bishop", "white_bishop"]
knight = ["black_knight", "white_knight"]
king = ["black_king", "white_king"]
queen = ["black_queen", "white_queen"]
rook = ["black_rook", "white_rook"]
empty = " "

chess_board = [
    [rook[0], knight[0], bishop[0], king[0], queen[0], bishop[0], knight[0], rook[0]],
    [pawn[0], pawn[0], pawn[0], pawn[0], pawn[0], pawn[0], pawn[0], pawn[0]],
    [empty, empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty, empty],
    [pawn[1], pawn[1], pawn[1], pawn[1], pawn[1], pawn[1], pawn[1], pawn[1]],
    [rook[1], knight[1], bishop[1], king[1], queen[1], bishop[1], knight[1], rook[1]]
]

for i in range(8):
    for j in range(8):
        pos = (off_set_x+j*cell_size+10, off_set_y+i*cell_size+10)
        rect(canvas, pos, (cell_size, cell_size), outline="black", fill=("white" if (i+j) % 2 == 0 else "black"))

        if chess_board[i][j] == empty:
            continue

        pos = (off_set_x+j*cell_size+10+(pawn_size[0]/2), off_set_y+i*cell_size+10+(pawn_size[1]/2))

        pawn_code = chess_board[i][j]
        color = pawn_code.split("_")[0]
        pawn_name = pawn_code.split("_")[1]
        pawn_image_url = images_url[color][pawn_name]

        pawn_image = resize_image(pawn_image_url, pawn_size[0], pawn_size[1])
        
        pawn = Label(image=pawn_image)
        pawn.image = pawn_image
        pawn.place(x=pos[0], y=pos[1])


canvas.pack()


root.mainloop()




