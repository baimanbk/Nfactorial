import pygame as pg
from dataclasses import dataclass
import random as rnd 
import time
from button import Button

pg.init()

RED = (255, 0, 0)
BLACK = (0, 0, 0)
length = 800
width = 800
net = 20
amount_mines = 30
distance = length // net

font = pg.font.SysFont("Verdana", 60)
font_small = pg.font.SysFont("Verdana", 20)

SCREEN = pg.display.set_mode([length, width])
pg.display.set_caption("Menu")

bkg = pg.image.load("assets/BACKGROUND.jpg")
BG = pg.transform.scale(bkg, (width, length))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("assets/font.ttf", size)

def ladeBild(dateiname):
  return pg.transform.scale(pg.image.load(dateiname), (abstand, abstand))


def gültig(y, x):
  return y > -1 and y < net and x > -1 and x < net


cell_normal = pg.transform.scale(pg.image.load('assets//TileUnknown.png'),(distance, distance))
cell_marked = pg.transform.scale(pg.image.load('assets//TileFlag.png'),(distance, distance))
cell_mine = pg.transform.scale(pg.image.load('assets//TileMine.png'),(distance, distance))
cell_selected = []
for i in range(9):
    cell_selected.append(pg.transform.scale(pg.image.load(f'assets//Tile{i}.png'),(distance, distance)))


matrix = []
around_current = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

@dataclass
class Cell():
    rows : int
    cols : int
    mine : bool = False
    selected : bool = False
    flagged : bool = False
    around_mines = int = 0

    def show(self):
        pos = (self.rows*distance, self.cols*distance)
        if self.selected:
            if self.mine:
                SCREEN.blit(cell_mine, pos)
            else:
                SCREEN.blit(cell_selected[self.around_mines], pos)
        else:
            if self.flagged:
                SCREEN.blit(cell_marked, pos)
            else:
                SCREEN.blit(cell_normal, pos)
    def detect_mines(self):
        for pos in around_current:
            new_row = self.rows + pos[0]
            new_col = self.cols + pos[1]
            if new_row >= 0 and new_row < net and new_col >= 0 and new_col < net:
                if matrix[new_row*net+new_col].mine:
                    self.around_mines += 1

def floodFill(rows, cols):
    for pos in around_current:
        new_row = rows + pos[0]
        new_col = cols + pos[1]
        if new_row >= 0 and new_row < net and new_col >= 0 and new_col < net:
            cell = matrix[new_row*net+new_col]
            if cell.around_mines == 0 and not cell.selected:
                cell.selected = True
                floodFill(new_row, new_col)
            else:
                cell.selected = True

for i in range(net*net):
    matrix.append(Cell(i // net, i % net))

while amount_mines > 0:
    x = rnd.randrange(net*net)
    if not matrix[x].mine:
        matrix[x].mine = True
        amount_mines -= 1
for object in matrix:
    object.detect_mines()

def play():

    clock = pg.time.Clock()
    running = True
    while running:
        clock.tick(20)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                rows = mouseX // distance
                cols = mouseY // distance
                i = rows*net+cols
                cell = matrix[i]
                if pg.mouse.get_pressed()[2]:
                    cell.flagged = not cell.flagged
                if pg.mouse.get_pressed()[0]:
                    cell.selected = True
                    if cell.around_mines == 0 and not cell.mine:
                        floodFill(rows, cols)
                    if cell.mine:
                        for object in matrix:
                            object.selected = True
                            #if object.selected == True:
                                #pg.time.delay(3000)
                                #text = "Came Over"
                                #WINNER_FONT = pg.font.SysFont('arial', 80)
                                #draw_text=WINNER_FONT.render(text,1,(255, 255, 255))
                                #SCREEN.fill(BLACK)
                                #SCREEN.blit(draw_text,(width//2-draw_text.get_width()/2,length//2-draw_text.get_height()/2))
                                #pg.display.update()
                            main_menu()
                            


        for object in matrix:
            #object.selected = True
            object.show()
        pg.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(30).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(420, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(440, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pg.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(420, 80))

        PLAY_BUTTON = Button(image=pg.image.load("assets/Play Rect.png"), pos=(440, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pg.image.load("assets/Options Rect.png"), pos=(440, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pg.image.load("assets/Quit Rect.png"), pos=(440, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    for object in matrix:
                        object.selected = False
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        pg.display.update()

main_menu()