import pygame
import time
from sudoku2 import  solve_sudoku,find_empty,valid
pygame.font.init()  
from copy import deepcopy


def solve(grid,pos,value):
    new_grid = deepcopy(grid)
    new_grid[pos[0]][pos[1]] = value
    a,b = valid(new_grid,value,pos),solve_sudoku(new_grid)

    if a and b:
        return True

    return False



class Cell:
    def __init__(self,window,id,height,width,value):
        self.window =window
        self.id = id
        self.x =None
        self.y = None
        self.height = height
        self.width = width
        self.value = value
        self.temp = None
        self.pos_in_grid= None  #list storing x and y coordinate in the grid(not actual position in the window)
        self.calculate_pos()
    def calculate_pos(self):
        i = self.id
        x_pos = (self.id%9)*self.width
        y_pos = (self.id//9)*self.height
        self.x = x_pos
        self.y = y_pos
        #------------------------------
        y_pos = i%9
        x_pos = i//9
        self.pos_in_grid =[x_pos,y_pos] 

    def draw(self,selected = False):
        fnt = pygame.font.SysFont("comicsans", 40)
        x,y = self.x,self.y
        if self.value:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            self.window.blit(text, (x + (self.width / 2 - text.get_width() / 2), y + (self.height / 2 - text.get_height() / 2)))


        if selected and not self.value:
            color = (255,0,0)
            pygame.draw.rect(self.window,color,(x,y,self.width,self.height),3)
    
    def temporary_draw(self,temp_value):
        if self.value !=0:
            return
        fnt = pygame.font.SysFont("comicsans", 40)
        self.temp = temp_value
        text = fnt.render(str(self.temp), 1, (155, 155, 155))
        self.window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def automate_draw(self,color):
        fnt = pygame.font.SysFont("comicsans", 40)
        x,y = self.x,self.y
        pygame.draw.rect(self.window, (255, 255, 255), (x, y, self.width,self.height), 0)
        if self.value:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            self.window.blit(text, (x + (self.width / 2 - text.get_width() / 2), y + (self.height / 2 - text.get_height() / 2)))
        if color == "green":
            pygame.draw.rect(self.window, (0, 255, 0), (x, y, self.width, self.height), 3)
        if color == "red":
            pygame.draw.rect(self.window, (255,0, 0), (x, y, self.width, self.height), 3)





class Grid:
    reset = [[3,0,6,5,0,8,4,0,0], 
        [5,2,0,0,0,0,0,0,0], 
        [0,8,7,0,0,0,0,3,1], 
        [0,0,3,0,1,0,0,8,0], 
        [9,0,0,8,6,3,0,0,5], 
        [0,5,0,0,9,0,6,0,0], 
        [1,3,0,0,0,0,2,5,0], 
        [0,0,0,0,0,0,0,7,4], 
        [0,0,5,2,0,6,3,0,0]]
        
    def __init__(self,rows,cols,width,height,window):
        # self.board =[[3,0,6,5,0,8,4,0,0], 
        # [5,2,0,0,0,0,0,0,0], 
        # [0,8,7,0,0,0,0,3,1], 
        # [0,0,3,0,1,0,0,8,0], 
        # [9,0,0,8,6,3,0,0,5], 
        # [0,5,0,0,9,0,6,0,0], 
        # [1,3,0,0,0,0,2,5,0], 
        # [0,0,0,0,0,0,0,7,4], 
        # [0,0,5,2,0,6,3,0,0]] 
        self.board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
        self.row = rows
        self.col = cols
        self.width = width
        self.height = height
        self.cells = dict()
        self.selected = None
        self.window = window
        self.create_cells()
    def create_cells(self):
        cell_width = self.width//9
        cell_height = self.height//9
        cnt = -1
        for i in range(9):
            for j in range(9):
                cnt+=1
                self.cells[cnt] = Cell(self.window,cnt,cell_height,cell_width,self.board[i][j])

        
    def clear(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j] = self.reset[i][j]
        self.create_cells()

        pass
    def self_solve(self):
        empty = find_empty(self.board)
        if not empty:
            return True
        r,c = empty
        i = (r*9)+(c%9)
        for value in range(1,10):
            if valid(self.board,value,[r,c]):
                self.update(i,value)
                self.cells[i].automate_draw("green")
                pygame.display.update()
                pygame.time.delay(100)    
                if self.self_solve():
                    return True
                self.update(i,0)
                self.cells[i].automate_draw("red")
                pygame.display.update()
                pygame.time.delay(100)
        return False



        
    def draw(self):
        cell_width = self.width//9
        cell_height = self.height//9
        #drawing vertical lines
        for i in range(8):
            x1 = (i+1)*cell_width
            y1 = 0
            x2 = x1
            y2 = self.height
            if (i+1)%3 ==0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.window, (0,0,0), (x1,y1), (x2,y2), thick)

        #drawing horizontal lines
        for i in range(9):
            x1 = 0  
            y1 = (i+1)*cell_height
            x2 = self.width
            y2 = y1
            if (i+1)%3 ==0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.window, (0,0,0), (x1,y1), (x2,y2), thick)
        for i in self.cells:
            if i ==self.selected:
                self.cells[i].draw(True)
            else:
                self.cells[i].draw()

    def temporary_draw(self,cell_id,temp_value):
        self.cells[cell_id].temporary_draw(temp_value)
    
    def check(self,cell_id):
        cell = self.cells[cell_id]
        if cell.value != 0:
            return False
        if not cell.temp:
            return False
        else:
            return solve(self.board,cell.pos_in_grid,cell.temp)

    def select(self,pos):
        x,y =pos
        i = 0
        if x<0 or x>self.width or y<0 or y>self.height:
            return
        cell_width,cell_height = self.width//9,self.height//9
        x_ = x//cell_width
        y_ = y//cell_height
        i = y_*9+x_
        self.selected = i
        return i
    
    def update(self,cell_id,value):
        cell = self.cells[cell_id]
        pos = cell.pos_in_grid
        self.board[pos[0]][pos[1]] = value
        cell.value = value

    
    def game_over(self):
        r,c = len(self.board),len(self.board[0])
        for i in range(r):
            for j in  range(c):
                if self.board[i][j] == 0:
                    return False
        return True

    def final_draw(self):
        print(self.width,self.height)
        pygame.draw.rect(self.window, (0,0,200), (0, 0, self.width, self.height),0)
        fnt = pygame.font.SysFont("comicsans", 100)
        text = fnt.render(str("Game Over !!!"), 1, (255, 0, 0))
        self.window.blit(text, (0+(self.width / 2 - text.get_width() / 2), 0 + (self.height / 2 - text.get_height() / 2)))


        pygame.display.update()
        



def format_time(time):
    sec = time%60
    minute = time//60
    hour = minute//60
    return str(hour) + ":" + str(minute)+":"+str(sec)
def window_update(window,board,play_time,steps,win_width,win_height):
    window.fill((220,210,255))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Timer : "+format_time(play_time),1,(0,0,0)) 
    window.blit(text,(win_width-200,win_height-40)) #select height and width for text adjustment
    text2 = font.render("Steps: "+str(steps),1,(0,0,0))
    window.blit(text2,(5,win_height-40))
    board.draw()
def main():
    win_width,win_height=540,600 
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Sudoku")
    board = Grid(9,9,540,540,window)
    key = None
    run = True
    start = time.time()
    cell_selected = None
    steps = 0
    while run:
        play_time = round(time.time()-start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    key = None
                    board.clear()
                    steps = 0
                    start = time.time()
                    
                if event.key == pygame.K_SPACE:
                    key = None
                    start_time = time.time()
                    if board.self_solve():
                        print("Game over but you cheated")

                    else:
                        print("No solution Possible")
                    end_time = time.time()
                    print("time_taken =",end_time-start_time)
                if event.key == pygame.K_RETURN:
                    cell_id = board.selected
     
                    temp = board.cells[cell_id].temp
                    if board.check(cell_id):
                        board.update(cell_id,temp)
                        key =None
                        steps+=1
                        if board.game_over():
                            print("Game Over")
                            board.final_draw()
                            pygame.time.delay(4000)
                    else:
                        print("Wrong Solution")
                            
                    key = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell_selected = board.select(pos)
                if cell_selected:
                    key = None

        window_update(window,board,play_time,steps,win_width,win_height)
        if cell_selected and key!=None:
            board.temporary_draw(cell_selected,key)
        pygame.display.update()
main()
