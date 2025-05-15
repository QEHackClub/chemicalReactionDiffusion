#imports
import math
import pygame
import random


#initialise screen 
pygame.init()

#display settings
width=900
height=900
size = (width, height)
screen = pygame.display.set_mode(size)
rows = 100
collumns = 100
pygame.display.set_caption("Turing Patterns")

#sim Settings
board = []
newBoard=[]
chemA=1
chemB=1
chemANext=1
chemBNext=1
feedRate=0.055 #standard feed rate to sustain lesser chem (found by solving differential equtns)
killRate=0.062 #same deal

diffusionConstantA=1
diffusionConstantB=0.5


feedRate=0.055 #stripes.
killRate=0.062 #
#diffusionConstantA=2
#diffusionConstantB=1

#Gray Scott kernel
mask=[
    [0.05,0.2,0.05],
    [0.2,-1,0.2],
    [0.05,0.2,0.05]]

#initialise the cell array
for i in range(collumns):
    board.append([])
    newBoard.append([])
    for j in range(rows):
        x=random.random()
        newBoard[i].append([0,0])
        if x<0.89: #stripy
        #if x<0.5:#spotty 
            board[i].append([1,0])
        else:
            board[i].append([0,1])

    

#matrix multiplication function
def matMul(mask,grid):
    result=[[0,0,0],[0,0,0],[0,0,0]] #create a result matrix
    for row in range(len(grid)):#standard matrix multiplication stuff
        for coll in range(len(mask[0])):
            total=0
            for iterator in range(len(mask[0])):
                total+=mask[row][iterator]*grid[iterator][coll]#ewww i hate this fidly stuff
            result[row][coll]=total
    return result

def wrapR(Row):
    rows=100
    if Row > rows-1:
        return 0
    elif Row < 0:
        return rows-1
    else:
        return Row
def wrapC(collumn):
    collumns=100
    if collumn > collumns-1:
        return 0
    elif collumn < 0:
        return collumns-1
    else:
        return collumn
    
#trapdoor
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Main Loop
time=0
while not done:
    #Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            pass
            #repeat for every cell
        
    for row in range(0,rows):
        for coll in range(0,collumns):

            chemA=board[row][coll][0]
            chemB=board[row][coll][1]
            chemANext=0
            chemBNext=0
            #+laplacian function including D_a
            chemANext+=board[wrapR(row-1)][wrapC(coll-1)][0]*diffusionConstantA*0.05+board[wrapR(row-1)][wrapC(coll)][0]*diffusionConstantA*0.2+board[wrapR(row-1)][wrapC(coll+1)][0]*diffusionConstantA*0.05
            chemANext+=board[wrapR(row)][wrapC(coll-1)][0]*diffusionConstantA*0.2+board[wrapR(row)][wrapC(coll)][0]*-1*diffusionConstantA+board[wrapR(row)][wrapC(coll+1)][0]*diffusionConstantA*0.2
            chemANext+=board[wrapR(row+1)][wrapC(coll-1)][0]*diffusionConstantA*0.05+board[wrapR(row+1)][wrapC(coll)][0]*diffusionConstantA*0.2+board[wrapR(row+1)][wrapC(coll+1)][0]*diffusionConstantA*0.05
            #+laplacian of b
            chemBNext+=board[wrapR(row-1)][wrapC(coll-1)][1]*diffusionConstantB*0.05+board[wrapR(row-1)][wrapC(coll)][1]*diffusionConstantB*0.2+board[wrapR(row-1)][wrapC(coll+1)][1]*diffusionConstantB*0.05
            chemBNext+=board[wrapR(row)][wrapC(coll-1)][1]*diffusionConstantB*0.2+board[wrapR(row)][wrapC(coll)][1]*-1*diffusionConstantB+board[wrapR(row)][wrapC(coll+1)][1]*diffusionConstantB*0.2
            chemBNext+=board[wrapR(row+1)][wrapC(coll-1)][1]*diffusionConstantB*0.05+board[wrapR(row+1)][wrapC(coll)][1]*diffusionConstantB*0.2+board[wrapR(row+1)][wrapC(coll+1)][1]*diffusionConstantB*0.05
            
            #reaction diffusion equation (Gray Scott implementation)
            chemANext-=(chemA*chemB*chemB)
            chemANext+=(feedRate*(1-chemA))
            chemANext=chemANext*1
            chemANext+=chemA
            if chemANext<0:
                chemANext=0.1
            if chemANext>1:
                chemANext=0.9
            chemBNext+=(chemA*chemB*chemB)
            chemBNext-=((feedRate+killRate)*(chemB))
            chemBNext=chemBNext*1
            chemBNext+=chemB
            if chemBNext<0:
                chemBNext=0
            if chemBNext>1:
                chemBNext=0.9
            
            #after entire canvas has been iterated we update values.
            newBoard[row][coll]=[chemANext,chemBNext]
    board=newBoard   
    #and blit to the renderd canvas.
    for row in range(rows):
        for coll in range(collumns):
            # Drawing Rectangle
            pygame.draw.rect(screen, (board[row][coll][0]*255,0,board[row][coll][1]*255), pygame.Rect(coll*width/collumns, row*height/rows, width/collumns, height/rows))


    pygame.display.flip()
    #Limit to 30 frames per second
    clock.tick(30)
 
# Close the window and quit when main loop exits
pygame.quit()
