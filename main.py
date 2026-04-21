import tkinter as tk
from PIL import Image, ImageTk
from random import randint
from ai import MinesweeperAI

root = tk.Tk()
root.geometry("1920x1080")
root.title("Minesweeper AI")
root.iconbitmap("sprites/icon.ico")

mainframe = tk.Frame(root, bg="lightblue", width=1920, height=1080) # lol

mainframe.place(x=0, y=0)
minesweeper_grid = ""
you_suck_text = ""  # setting up dumb global declarations for later
you_win_text = ""

size_entry_stringvar = tk.StringVar(value="Enter board size with format 'WIDTHxHEIGHT'")
size_entry_object = tk.Entry(mainframe, textvariable=size_entry_stringvar, font=("minesweeper", 20), justify="center")
size_entry_object.place(x=240, y=100, width=1000, height=50)
size_entry_button = tk.Button(mainframe, command=lambda: acquire_size(), text="start", font=("minesweeper", 20), justify="center")
size_entry_button.place(x=1340, y=100, width=200, height=50)

scam_detection = tk.Text(mainframe, font=("minesweeper", 20))
scam_detection.place(x=240, y=200, width=600, height=80)
scam_detection.insert(tk.END, chars="this is an error message space if you type something dumb")

board_width, board_height = 0, 0

cells_dict = {}  # believe it or not, this stores all the cells
ai_code = MinesweeperAI(cells_dict)
winnable = True

home_pil = Image.open("sprites/home.png").resize((25, 25))
home_image = ImageTk.PhotoImage(home_pil)

def acquire_size():
    global board_width, board_height
    size = acquire_size_func()
    if size == False:
        pass
    else:
        board_width, board_height = size
        size_entry_object.destroy()
        size_entry_button.destroy()
        scam_detection.destroy()
        create_board()

def acquire_size_func():
    try:
        board_width, board_height = size_entry_object.get().split(sep="x")
    except ValueError:
        scam_detection.delete("1.0", tk.END)
        scam_detection.insert(tk.END, chars="this game is indeed 2d. please use the format widthxheight")
        return False

    # check if i'm being scammed
    while True:
        try:
            board_width = int(board_width)
            board_height = int(board_height)
            working = True
            break
        except ValueError:
            scam_detection.delete("1.0", tk.END)
            scam_detection.insert(tk.END, chars="yeah base 10 numerals please")
            working = False
            break
    
    if working == False:
        return False
    elif board_width >= 41 or board_height >= 41 or board_width <= 0 or board_height <= 0:
        scam_detection.delete("1.0", tk.END)
        scam_detection.insert(tk.END, chars="this guy's trynna break his pc dude")
        return False
    else:
        return (board_width, board_height)


def all_configure(grid):
    for row in range(board_height):
        grid.grid_rowconfigure(row)
    for column in range(board_width):
        grid.grid_columnconfigure(column)

class Cell:

    def __init__(self, row, column, grid):
        
        self.adjacent_bombs = 0
        self.clicked = 0
        self.flagged = False
        
        if randint(1,5) == 1:
            self.bomb = True
        else: self.bomb = False

        self.grid = grid
        def min(a, b):
            if a==b: return a
            if a<b: return a
            if b<a: return b
        self.cell_dimensions = min(1200 // board_width, 650 // board_height)  # IF IT WORKS IT WORKS
        flag_pil = Image.open("sprites/flag.png").resize((self.cell_dimensions, self.cell_dimensions))
        self.flag_image = ImageTk.PhotoImage(flag_pil)
        bomb_pil = Image.open("sprites/bomb.png").resize((self.cell_dimensions, self.cell_dimensions))
        self.bomb_image = ImageTk.PhotoImage(bomb_pil)
        
        self.tkbutton = tk.Button(master=grid, bg="white", width=self.cell_dimensions, height=self.cell_dimensions // 2,
                                  command=lambda: self.onClick())
        self.row, self.column = row, column
    
    def onClick(self):
        
        if self.flagged == True:
            self.tkbutton.config(image="")
            self.flagged = False

        self.clicked = 1

        if self.bomb == True:
            display_all_bombs()
        else:
            self.tkbutton.config(text=self.adjacent_bombs, font=("minesweeper", 8))
            all_configure(self.grid)
        
        check_for_win()
            
    def count_bombs(self):
        count = 0
        invalid_cells = []
        adjacent_cells = [(self.row + 1, self.column + 1),
                          (self.row + 1, self.column),
                          (self.row + 1, self.column - 1),
                          (self.row, self.column + 1),
                          (self.row, self.column - 1),
                          (self.row - 1, self.column + 1),
                          (self.row - 1, self.column),
                          (self.row - 1, self.column - 1)]

        for item in adjacent_cells:
            try:
                cells_dict[item]
            except KeyError:
                invalid_cells.append(item)
        adjacent_cells = [x for x in adjacent_cells if x not in invalid_cells]

        for cell in adjacent_cells:
            if cells_dict[cell].bomb == True:
                count += 1

        return count

    def display_bomb(self):
        if self.bomb == True:
            self.tkbutton.config(image=self.bomb_image)
            all_configure(self.grid)

    def flag_cell(self, event):
        if self.flagged == True:
            self.tkbutton.config(image="")
            self.flagged = False
        else:
            self.tkbutton.config(image=self.flag_image)
            self.flagged = True
        all_configure(self.grid)

def create_board():
    global cells_dict, ai_code, minesweeper_grid, winnable
    winnable = True

    minesweeper_grid = tk.Frame(mainframe, borderwidth=2, width=1200, height=675)
    minesweeper_grid.grid_propagate(False)

    for row in range(board_width):
        for column in range(board_height):
            cells_dict.update({(row, column) : Cell(row, column, grid=minesweeper_grid)})  # a tuple of row and column will map to its cell
            cells_dict[(row, column)].tkbutton.place(x=row * cells_dict[(row, column)].cell_dimensions,
                    y=column * cells_dict[(row, column)].cell_dimensions,
                    width=cells_dict[(row, column)].cell_dimensions,
                    height=cells_dict[(row, column)].cell_dimensions)
            cells_dict[(row, column)].tkbutton.bind("<Button-3>", cells_dict[(row, column)].flag_cell)
            minesweeper_grid.grid_columnconfigure(column)
        minesweeper_grid.grid_rowconfigure(row)

    minesweeper_grid.place(x=50, y=50, width=1200, height=675)
    for cell in cells_dict.values():
        cell.adjacent_bombs = cell.count_bombs()  # count bombs AFTER board is created, not during initialisation of cell
    ai_code = MinesweeperAI(cells_dict)

    # ai run button
    run_safe_button = tk.Button(mainframe, command=lambda: ai_code.run_ai(0), text="find a safe spot", font=("minesweeper", 20), justify="center")
    run_safe_button.place(x=900, y=450, width=200, height=50)
    run_bomb_button = tk.Button(mainframe, command=lambda: ai_code.run_ai(1), text="find a bomb", font=("minesweeper", 20), justify="center")
    run_bomb_button.place(x=900, y=500, width=200, height=50)

def display_all_bombs():
    global you_suck_text, winnable
    winnable = False

    for cell in cells_dict.values():
        cell.display_bomb()

    you_suck_text = tk.Label(mainframe, bg="red", text="you're so bad L. you can still click on squares if you feel like it. this is not buggy at all",
                             font=("minesweeper", 20))
    you_suck_text.place(x=50, y=600, width=1400, height=60)

def set_all_white(event):
    for cell in cells_dict.values():
        cell.tkbutton.config(bg="white")

def restart_fully():
    try:
        minesweeper_grid.destroy()
        you_suck_text.destroy()
        you_win_text.destroy()
    except AttributeError:
        pass
    ai_code.clear_ai()
    create_board()

def check_for_win():
    global you_win_text
    success = 1
    for cell in cells_dict.values():
        if not ((cell.clicked == 1 and cell.bomb == False) or (cell.clicked == 0 and cell.bomb == True)):
            success = 0
    
    if success == 1 and winnable == True:

        you_win_text = tk.Label(mainframe, bg="lightgreen", text="you're literally the greatest minesweeper. save some skill for the rest of us",
                             font=("minesweeper", 20))
        you_win_text.place(x=50, y=600, width=1400, height=60)


restart_button = tk.Button(mainframe, image=home_image, command=lambda: restart_fully())
restart_button.place(x=1420, y=30, width=50, height=50)

root.bind_all("<Button-1>", set_all_white)
root.bind_all("<Button-3>", set_all_white)

root.mainloop()