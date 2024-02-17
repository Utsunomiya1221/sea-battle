from tkinter import *
from tkinter import messagebox
import time
import random

# ------ Флаги ------
apprunning = True
in_gamemode = False
step_player = True # Если True - ходит игрок №1, иначе - ходит игрок №2
ai_player = False
flazhok = False
flazhok_dobiv = False
# -------------------

# ---- Константы ----
center_x = 900
menu_offset = 200
size_x = 800
size_y = 800
s_x = s_y = 10
step_x = (size_x // s_x) - 20
step_y = (size_y // s_y) - 20
# -------------------

button_back = None
button_single = None
button_multiple = None

enemy_ships1 = [[0 for x in range(s_x + 1)] for y in range(s_x + 1)]
enemy_ships2 = [[0 for x in range(s_x + 1)] for y in range(s_x + 1)]

points1 = [[-1 for x in range(s_x)] for y in range(s_x)]
points2 = [[-1 for x in range(s_x)] for y in range(s_x)]

print_ships = []
print_figur = []

array_it_coords = [-1, -1]
pred_coords = [-1, -1]

def show_enemy_button(enemy_ships, points, offset=0):
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                ship_x = i + 2
                ship_y = j + 2
                color = "#%02x%02x%02x" % (27, 206, 224)
                if points[j][i] != -1:
                    color = "green"
                ship = canvas.create_rectangle(ship_x * step_x - 20 + offset, ship_y * step_y - 20, ship_x * step_x + step_x - 20 + offset, ship_y * step_y + step_y - 20 , fill=color, width= 5)

                print_ships.append(ship)

def begin_again_button():
    global enemy_ships1, enemy_ships2
    global print_ships, print_figur, points1, points2
    for ship in print_ships:
        canvas.delete(ship)
    for figur in print_figur:
        canvas.delete(figur)
    print_figur = []
    print_ships = []
    points1 = [[-1 for x in range(s_x)] for y in range(s_x)]
    points2 = [[-1 for x in range(s_x)] for y in range(s_x)]
    
    enemy_ships2 = generate_enemy_ships()
    enemy_ships1 = generate_enemy_ships()

def generate_enemy_ships():
    enemy_ships = []
    ships_list = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    sum_all_ships = sum(ships_list)
    sum_curr_ships = 0
    while sum_curr_ships != sum_all_ships:
        enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_x + 1)]

        for i in range(0, 10):
            len = ships_list[i]
            direct = random.randrange(1, 3) # 1 - горизонтальное, 2 - вертикальное
            
            ship_x = random.randrange(0, s_x) # получаем x
            if ship_x + len > s_x:
                ship_x -= len
            
            ship_y = random.randrange(0, s_y) # получаем y
            if ship_y + len > s_y:
                ship_y -= len
            
            if direct == 1:
                for j in range(0, len):
                    try:
                        check_ships = 0
                        check_ships = enemy_ships[ship_y][ship_x - 1] + \
                                    enemy_ships[ship_y][ship_x + j] + \
                                    enemy_ships[ship_y][ship_x + j + 1] + \
                                    enemy_ships[ship_y + 1][ship_x + j + 1] + \
                                    enemy_ships[ship_y - 1][ship_x + j + 1] + \
                                    enemy_ships[ship_y + 1][ship_x + j] + \
                                    enemy_ships[ship_y - 1][ship_x + j]
                        if check_ships == 0:
                            enemy_ships[ship_y][ship_x + j] = i + 1
                    except Exception:
                        pass
            elif direct == 2:
                if ship_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_ships = 0
                            check_ships = enemy_ships[ship_y - 1][ship_x] + \
                                        enemy_ships[ship_y + j][ship_x] + \
                                        enemy_ships[ship_y + j + 1][ship_x] + \
                                        enemy_ships[ship_y + j + 1][ship_x + 1] + \
                                        enemy_ships[ship_y + j + 1][ship_x - 1] + \
                                        enemy_ships[ship_y + j][ship_x + 1] + \
                                        enemy_ships[ship_y + j][ship_x - 1]
                            if check_ships == 0:
                                enemy_ships[ship_y + j][ship_x] = i + 1
                        except Exception:
                            pass
        
        sum_curr_ships = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[i][j] > 0:
                    sum_curr_ships += 1
    return enemy_ships

def exit_button():
    global apprunning
    apprunning = False
    root.destroy()

def draw_place(offset=0):
    for i in range(1, s_x + 2):
        canvas.create_line(offset + step_x * (i + 1) - 20, 100, offset + step_x * (i + 1) - 20, 700, width= 5)

    for i in range(1, s_y + 2):
        canvas.create_line(offset + 100, step_y * i + 40, offset + 700, step_y * i + 40, width= 5)

def multiple_btn():
    global points1, points2
    global enemy_ships1, enemy_ships2
    global in_gamemode, ai_player

    ai_player = False
    in_gamemode = True

    button_single.destroy()
    button_multiple.destroy()
    button_back.destroy()

    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()

    button_player1 = Button(root,text="Показать корабли игрока 1", command= lambda: show_enemy_button(enemy_ships1, points1))
    button_player1.place(x= size_x + 20, y= size_y // 2 - 300)
    
    button_player2 = Button(root,text="Показать корабли игрока 2", command= lambda: show_enemy_button(enemy_ships2, points2, offset=1000))
    button_player2.place(x= size_x + 20, y= size_y // 2 - 260)

    button_backid = Button(root,text="Начать заново", command= begin_again_button)
    button_backid.place(x= size_x + 55, y= size_y // 2 - 220)

    player1 = canvas.create_text(size_x // 2, size_y // 2 + 315, text="игрок под номером 1", fill= "white",font=("Verdana 10 bold"))
    print_figur.append(player1)

    player2 = canvas.create_text(size_x // 2 + 1000, size_y // 2 + 315, text="игрок под номером 2", fill= "white", font=("Verdana 10 bold"))
    print_figur.append(player2)


    draw_place()
    draw_place(size_x + menu_offset)
 
def single_btn():
    global ai_player
    multiple_btn()
    ai_player = True
    
def draw_click(x, y, enemy_ships, offset=0):
    if enemy_ships[y][x] == 0:
        x += 2
        y += 2
        crug1 = canvas.create_oval(x * step_x - 20 + offset, y * step_y - 20, x * step_x + step_x - 20 + offset, y * step_y + step_y - 20, fill="#80CBC4", outline="#004D40", width=5)
        crug2 = canvas.create_oval(x * step_x - 10 + offset, y * step_y - 10, x * step_x + step_x - 30 + offset, y * step_y + step_y - 30, fill="#1BCBE8", outline="#004D40", width=5)
        print_figur.append(crug1)
        print_figur.append(crug2)
    else:
        x += 2
        y += 2
        kvad1 = canvas.create_rectangle(x * step_x - 20 + offset, y * step_y - 20, x * step_x + step_x - 20 + offset, y * step_y + step_y - 20, fill="green", width=5)
        print_figur.append(kvad1)

def checkwin(points):
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points[j][i] == -1:
                    win = False
                    break
    return win

def click_handler(mouse_x, mouse_y, points_player, points_ai, ememy_ships, offset=0):
    global win_text
    if checkwin(points_player):
        return False
    cell_x = mouse_x // step_x
    cell_y = mouse_y // step_y
    if points_player[cell_y][cell_x] == -1:
        points_player[cell_y][cell_x] = 0
        draw_click(cell_x, cell_y, ememy_ships, offset)
        if checkwin(points_player):
            print("ура, победа")
            win_text = canvas.create_text(size_x // 2 + 500, size_y // 2 - 265, text="ура, победа!", fill= "green", font=("default 10 bold"))
            print_figur.append(win_text)
            points_ai = [[0 for x in range(s_x)] for y in range(s_x)]
            points_player = [[0 for x in range(s_x)] for y in range(s_x)]
        return True
    return False 
    
test_x_y = []

def fill_coords():
    x = array_it_coords[0]
    y = array_it_coords[1]
    if y != 9:
        test_x_y.append([x, y + 1])
    if x != 9:
        test_x_y.append([x + 1, y])
    if y != 0:
        test_x_y.append([x, y - 1])
    if x != 0:
        test_x_y.append([x - 1, y])

def random_click(cell_x, cell_y, flazhok, flazhok_dobiv, points_ai):
    flazhok = False
    flazhok_dobiv = False 
    cell_x = random.randint(0, s_x - 1)
    cell_y = random.randint(0, s_y - 1)
    while points_ai[cell_y][cell_x] != -1:
        cell_x = random.randint(0, s_x - 1)
        cell_y = random.randint(0, s_y - 1)

def ai_clicker(points_ai, points_player, ememy_ships, offset=0):
    global win_text, array_it_coords, test_x_y, flazhok, flazhok_dobiv, pred_coords
    if checkwin(points_ai):
        return
    root.update()
    time.sleep(0.5)
    if flazhok_dobiv == True:
        cell_x = array_it_coords[0]
        cell_y = array_it_coords[1]
        pred_x = pred_coords[0]
        pred_y = pred_coords[1]
        if cell_x > pred_x and cell_x < 9:
            cell_x += 1
        elif cell_x < pred_x and cell_x > 0:
            cell_x -= 1
        elif cell_y > pred_y and cell_y < 9:
            cell_y += 1
        elif cell_y < pred_y and cell_y > 0:
            cell_y -= 1
        else:
            random_click(cell_x, cell_y, flazhok, flazhok_dobiv, points_ai)

    elif flazhok == True:
        if not test_x_y:
            fill_coords()
        cell_x = test_x_y[len(test_x_y) - 1][0]
        cell_y = test_x_y[len(test_x_y) - 1][1]
    else:
        cell_x = random.randint(0, s_x - 1)
        cell_y = random.randint(0, s_y - 1)
        while points_ai[cell_y][cell_x] != -1:
            cell_x = random.randint(0, s_x - 1)
            cell_y = random.randint(0, s_y - 1)
    
    if ememy_ships[cell_y][cell_x] != 0:
        if flazhok == False:
            flazhok = True
            pred_coords[0] = cell_x
            pred_coords[1] = cell_y
        else:
            flazhok_dobiv = True
        array_it_coords[0] = cell_x
        array_it_coords[1] = cell_y
    
    else: 
        if flazhok == True and test_x_y and flazhok_dobiv == False:
            test_x_y.pop()
            if not test_x_y:
                flazhok = False
        else:
            flazhok = False
            flazhok_dobiv = False
            array_it_coords[0] = -1
            array_it_coords[1] = -1
            pred_coords[0] = -1
            pred_coords[1] = -1
            test_x_y.clear()
    print(test_x_y)
    print(cell_y, cell_x)
    points_ai[cell_y][cell_x] = 0
    draw_click(cell_x, cell_y, ememy_ships, offset)
    if checkwin(points_ai):
        print("ура, победа")
        win_text = canvas.create_text(size_x // 2 + 500, size_y // 2 - 265, text="ура, победа!", fill= "green", font=("default 10 bold"))
        print_figur.append(win_text)
        points_ai = [[0 for x in range(s_x)] for y in range(s_x)]
        points_player = [[0 for x in range(s_x)] for y in range(s_x)]
    
def action_bts(event):
    global step_player
    global points1, points2
    global enemy_ships1, enemy_ships2
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    if in_gamemode == True:
        if (mouse_x > 100 and mouse_x < 700) and (mouse_y > 100 and mouse_y < 700) and step_player == True:
            mouse_x -= 100
            mouse_y -= 100
            if click_handler(mouse_x, mouse_y, points1, points2, enemy_ships1) == True:
                step_player = False
                if ai_player == True:
                    ai_clicker(points2, points1, enemy_ships2, 1000)
                    step_player = True

        elif step_player == False:
            if (mouse_x > 1100 and mouse_x < 1700) and (mouse_y > 100 and mouse_y < 700) and ai_player == False:
                mouse_x -= 1100
                mouse_y -= 100
                click_handler(mouse_x, mouse_y, points2, enemy_ships2, 1000)
                step_player = True
        
def play_btn():
    global button_back, button_single, button_multiple 
    global img_multiple, img_single

    button_play.destroy()
    button_opt.destroy()
    button_quit.destroy()

    img_single = PhotoImage(file='singleplayer.png')
    button_single = Button(root, image= img_single, relief=FLAT, command= single_btn)
    button_single.place(width=300, height= 80, x= center_x - 325, y= size_y // 2 - 100)

    img_multiple = PhotoImage(file='multiplayer.png')
    button_multiple = Button(root, image= img_multiple, relief=FLAT, command= multiple_btn)
    button_multiple.place(width=300, height= 80, x= center_x + 25, y= size_y // 2 - 100)

    button_back = Button(root, image= img_quit, relief=FLAT, command= menu)
    button_back.place(width=300, height= 80, x= center_x - 150, y= size_y // 2)

def menu():
    global img_menu, img_options, img_play, img_quit
    global button_play,button_opt, button_quit

    img_menu = PhotoImage(file='море море 2.png')
    canvas.create_image(0, 0, image= img_menu, anchor= 'nw')

    img_play = PhotoImage(file='play.png')
    button_play = Button(root, image= img_play, relief=FLAT, command= play_btn)
    button_play.place(width=300, height= 80, x= center_x - 150, y= size_y // 2 - 100)

    img_options = PhotoImage(file='options.png')
    button_opt = Button(root, image= img_options, relief=FLAT)
    button_opt.place(width=300, height= 80, x= center_x - 150, y= size_y // 2)

    img_quit = PhotoImage(file='quit.png')
    button_quit = Button(root, image= img_quit, relief=FLAT, command= exit_button)
    button_quit.place(width=300, height= 80, x= center_x - 150, y= size_y // 2 + 100)

    if button_back != None:
        button_back.destroy()
    if button_single != None:
        button_single.destroy()
    if button_multiple != None:
        button_multiple.destroy()
    
root = Tk()

root.title('Морской бой')
root.protocol('WM_DELETE_WINDOW', exit_button)
root.resizable(False, False)

canvas = Canvas(root, width= size_x + menu_offset + size_x, height= size_y, bd= 0, highlightthickness=0)
canvas.pack(fill='both')

canvas.bind_all("<Button-1>", action_bts)
canvas.bind_all("<Button-3>", action_bts)
 
menu()

while (apprunning):
    root.update_idletasks()
    root.update()
    time.sleep(0.05)
