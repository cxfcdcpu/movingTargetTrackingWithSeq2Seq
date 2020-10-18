from collections import deque
import numpy as np
import visLib as vb
import random as rd
import os
import sys

HER_GRID = 20
VER_GRID = 20
HER_LEN = 1800
VER_LEN = 1200

COL= HER_LEN//HER_GRID
questions = []
answers = []
questionStrokeRange = [int(sys.argv[1]),int(sys.argv[2])]
datas=[]

def findDirection(dx,dy):
    
    if dx >= 0 and dy >= 0:
        if dx >= dy:
            return [[1,0],[0,1],[0,-1],[-1,0]]
        else:
            return [[0,1],[1,0],[-1,0],[0,-1]]
    elif dx<0 and dy<0:
        if dx >= dy:
            return [[-1,0],[0,-1],[0,1],[1,0]]
        else:
            return [[0,-1],[-1,0],[1,0],[0,1]]
    elif dx>=0 and dy <0:
        if abs(dx) >= abs(dy):
            return [[1,0],[0,-1],[0,1],[-1,0]]
        else:
            return [[0,-1],[1,0],[-1,0],[0,1]]
    else:
        if abs(dx) >= abs(dy):
            return [[-1,0],[0,1],[0,-1],[1,0]]
        else:
            return [[0,1],[-1,0],[1,0],[0,-1]]
            
def onTrajectory(p1,p2, cur):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    x0 = cur[0]
    y0 = cur[1]
    if x1==x2 and y1 == y2:
        return (x0-x1)**2+(y0-y1)**2 <=3
    dis = abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1)) / np.sqrt(np.square(x2-x1) + np.square(y2-y1))
    return dis<=1.5

def grid_anchors(rowCells,colCells,row=5,col=8):
    st_w=colCells//(col+1)
    st_h=rowCells//(row+1)
    #print(st_w,st_h)
    ini_w=0
    ini_h=0
    anchors = []
    for i in range(row):
        ini_h+=st_h
        ini_w=0
        for j in range(col):
            ini_w+=st_w
            anchors.append([ini_w,ini_h])
    return anchors
    
def getGridlizedTrajectory(strokes):
    hhalf = HER_LEN//2
    vhalf = VER_LEN//2
    gridTrajectory = [[round((strokes[0][0]+hhalf)//HER_GRID),round(-((strokes[0][1]-vhalf)//VER_GRID))]]
    ret=[]
    visited={}
    prePoint = gridTrajectory[-1]
    ret.append(prePoint)
    for i in range(1,len(strokes)):
        prePoint = gridTrajectory[-1]
        curPoint = [round((strokes[i][0]+hhalf)//HER_GRID),round(-((strokes[i][1]-vhalf)//VER_GRID))]
        gridTrajectory.append(curPoint)
        xmin= min(prePoint[0],curPoint[0])
        xmax = max(prePoint[0],curPoint[0])
        ymin= min(prePoint[1],curPoint[1])
        ymax = max(prePoint[1],curPoint[1])
        
        dx = curPoint[0] - prePoint[0]
        dy = curPoint[1] - prePoint[1]

        direction = findDirection(dx,dy)
        nodeQueue = deque()
        nodeQueue.append((prePoint[0],prePoint[1]))
        while nodeQueue:
            curNode = nodeQueue.popleft()
            visited[curNode]=1
            for d in direction:
                nextNode = (curNode[0]+d[0],curNode[1]+d[1])
                if nextNode not in visited and xmin<=nextNode[0]<=xmax and ymin<=nextNode[1]<=ymax:
                    visited[nextNode]=1
                    if onTrajectory(prePoint,curPoint,nextNode):
                        nodeQueue.append(nextNode)
                        ret.append([nextNode[0],nextNode[1]])
    return ret

def to1DTraj(gridTrajectory, col):
    ret=[]
    for point in gridTrajectory:
        ret.append(point[1]*col+point[0]+1)
        #print("X:{} Y:{}".for|mat(point[0],point[1]))
    return ret

anchors = grid_anchors(60,90)
gridAnchor1D = to1DTraj(anchors,COL)
cmd = "./experiment/getAnswer.o "
cmd += str(COL)+" "
cmd += str(questionStrokeRange[0])+ " "
cmd += str(questionStrokeRange[1])+ " "
cmd += str(len(anchors))+ " "
for anchor in gridAnchor1D:
    cmd+=str(anchor)
    cmd+=" "
print(cmd)
os.system(cmd)
