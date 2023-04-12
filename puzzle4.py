##DEBJYOTI SENGUPTA##
import os
import sys
import copy
import random
from collections import deque

#Get Pond and Hay locations
input_path=sys.argv[1]
output_path=sys.argv[2]

fin=open(input_path,'r')
size=int(fin.readline())
farm=fin.readlines()
hays=0; ponds=0; hpos_list=[]; ppos_list=[];
for i in range(size):
    hays+=farm[i].count('@')
    ponds+=farm[i].count('#')
    if (farm[i].count('@')!=0):
        nxt1=0
        for j in range(farm[i].count('@')):
            hpos=farm[i].find('@',nxt1)
            hpos_list.append((i,hpos))
            nxt1=hpos+1
    if (farm[i].count('#')!=0):
        nxt2=0
        for j in range(farm[i].count('#')):
            ppos=farm[i].find('#',nxt2)
            ppos_list.append((i,ppos))
            nxt2=ppos+1

            
fout=open(output_path,'w')
fout.write(str(size)+'\n')

#Initialize GameBoard or initial input state

GameBoard=[]
for i in range(size):
    GameBoard.append([])
for i in range(size):
    for j in range(size):
        GameBoard[i].append(0)

for i in range(size):
    for j in range(size):
        if (i,j) in hpos_list:
            GameBoard[i][j]='@'
        elif (i,j) in ppos_list:
            GameBoard[i][j]='#'
        else:
            GameBoard[i][j]='.'



#Create List of possible placements of Cows(Actions)

Actions=[]
for i in range(size):
    for j in range(size):
        if GameBoard[i][j]=='.':
            Actions.append((i,j))

#Transition Function
def PlaceCow(plan):
    flux_state=copy.deepcopy(GameBoard)
    for (i,j) in plan:
        flux_state[i][j]='C'
    return flux_state


def cowscore(i,j):
    score=0
    offsets=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    cowneigh=False; hayneigh=False; pondneigh=False;
    for temp in range(8):
        r=i+offsets[temp][0]
        c=j+offsets[temp][1]
        if (r,c) in plan:
            cowneigh=True
    for temp in [1,3,4,6]:
        r=i+offsets[temp][0]
        c=j+offsets[temp][1]
        if (r,c) in hpos_list:
            hayneigh=True
        elif (r,c) in ppos_list:
            pondneigh=True
    if cowneigh==True:
        score-=3
    if hayneigh==True:
        score+=1
    if hayneigh==True and pondneigh==True:
        score+=2
    return score


def Goal(state):
    score=0
    for i in range(size):
        for j in range(size):
            if state[i][j]=='C':
                score+=cowscore(i,j)
    if score>=12 and len(plan)==hays:
        return True,score
    else:
        return False,score

def best_index(f):
    x=-200
    for p in f:
        check_state=PlaceCow(p)
        temp_goal,check_score=Goal(check_state)
        if check_score>x:
            x=check_score
            best=p
    return f.index(best)

   

## Best Choice First Implementation

front=[]
for i in Actions:
    t=[i]
    front.append(t)


plan=front[0]

while front!=[]:
    plan=front.pop(best_index(front))
    s=PlaceCow(plan)
    goal,state_score=Goal(s)
    if goal:
        sf=s
        break;
    
    for move in Actions:
        if move not in plan:
            temp=copy.deepcopy(plan)
            temp.append(move)
            temp.sort()
            if temp not in front:
                front.append(temp)


farmwc=[]
for i in range(size):
    str1=''
    sf[i].append('\n')
    str1=str1.join(sf[i])
    farmwc.append(str1)

fout.writelines(farmwc)

totalsc=state_score
fout.write(str(totalsc))
fout.write('\n')
fin.close()
fout.close()

