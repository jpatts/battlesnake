import bottle
import os
import random
import json
import numpy as np
from heapq import *

@bottle.route('/')
def static():
    return "the server is running"

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    return {
        'color': '#9604DB',
        'taunt': 'I wont bite',
        'head_url': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/63/Feels_good_man.jpg/200px-Feels_good_man.jpg',
        'name': 'spare me',
        'head_type': 'smile',
        'tail_type': 'regular',
        'secondary_color': '#ed7309'
    }

def getBoard(data):
    # create game board filled with ones
    height = data['height']
    width = data['width']
    board = np.ones((width, height))

    # set boundary as zeroes around board
    # this means we have to add 1 to every x,y reference because we changed the shape from (N, N) to (N+1, N+1)
    board = np.pad(board, 1, 'constant', constant_values=0)

    # add snakes location to board
    enemiesLocation = data['snakes']['data']
    for i in range(len(enemiesLocation)):
        snake = data['snakes']['data'][i]['body']['data']
        for j in range(len(snake)):
            x = snake[j]['y'] + 1
            y = snake[j]['x'] + 1
            board[x, y] = 0

    # add food to board
    for i in range(len(data['food']['data'])):
        x = data['food']['data'][i]['y'] + 1
        y = data['food']['data'][i]['x'] + 1
        board[x, y] *= np.exp(1 / (data['you']['health'] / 100))

    # add weight to board
    goal = [0, 0]
    for x in range(width + 2):
        for y in range(height + 2):
            board[x, y] = getWeight(board, x, y)
            if board[x, y] > board[goal[0], goal[1]]:
                goal = [x, y]
    
    return board, goal

def getWeight(board, x, y):
    weight = 0
    value = board[x, y]
    while(True):
        if board[x + weight, y] == 0:
            value *= (weight + 1)
            break
        weight += 1
    weight = 0
    while(True):
        if board[x - weight, y] == 0:
            value *= (weight + 1)
            break
        weight += 1
    weight = 0
    while(True):
        if board[x, y + weight] == 0:
            value *= (weight + 1)
            break
        weight += 1
    weight = 0
    while(True):
        if board[x, y - weight] == 0:
            value *= (weight + 1)
            break
        weight += 1
    
    return value

from heapq import *


def heuristic(a, b):
    return abs(b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(board, head, goal):

    # directions we are looking in
    neighbours = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    # locations we have checked
    closed = set()

    # locations we have previously moved to
    visited = {}

    # cost of moving from start cell to given cell
    G = { head: 0 }

    # estimated cost of moving from given cell (head) to goal
    H = { head: heuristic(head, goal) }
    
    heap = []

    heappush(heap, (H[head], head))

    while heap:

        current = heappop(heap)[1]

        if current == goal:
            data = []
            
            # return best path using current
            while current in visited:
                data.append(current)
                current = visited[current]
            
            newData = []
            for i in reversed(data):
                newData.append(i)
                
            return newData

        closed.add(current)
        for i, j in neighbours:
            neighbour = current[0] + i, current[1] + j
            tentative_G = G[current] + heuristic(current, neighbour)

            if 1 <= neighbour[0] < board.shape[0] - 1:
                if 1 <= neighbour[1] < board.shape[1] - 1: 
                    # make sure no snakes in path
                    if board[neighbour[0], neighbour[1]] == 0:
                        continue
                else:
                    continue
            else:
                continue

            if neighbour in closed and tentative_G >= G.get(neighbour, 0):
                continue
                
            if  tentative_G < G.get(neighbour, 0) or neighbour not in [i[1]for i in heap]:
                visited[neighbour] = current
                G[neighbour] = tentative_G
                H[neighbour] = tentative_G + heuristic(neighbour, goal)
                heappush(heap, (H[neighbour], neighbour))
                
    return False

def getDirection(board, head, goal):

    shortestPath = astar(board, (head[0], head[1]), (goal[0], goal[1]))

    if len(shortestPath) > 1:
        shortestPath = shortestPath[0]
    else:
        shortestPath = shortestPath[0]

    nextMove = [shortestPath[0] - head[0], shortestPath[1] - head[1]]

    if nextMove == [0, 0]:
        nextMove = [goal[0] - head[0], goal[1] - head[1]]
    if nextMove == [1, 0]:
        return 'down'
    if nextMove == [0, 1]:
        return 'right'
    if nextMove == [-1, 0]:
        return 'up'
    if nextMove == [0, -1]:
        return 'left'
    else:
        if board[head[0] + nextMove[0], head[1]] > board[head[0], head[1] + nextMove[1]]:
            if nextMove[0] == 1:
                return 'down'
            else:
                return 'up'
        else:
            if nextMove[1] == 1:
                return 'right'
            else:
                return 'left'

@bottle.post('/move')
def move():
    data = bottle.request.json
    #print(json.dumps(data, indent=4))
    np.set_printoptions(suppress=True)

    # get player snakes head
    x = data['you']['body']['data'][0]['y'] + 1
    y = data['you']['body']['data'][0]['x'] + 1
    head = [x, y]

    board, goal = getBoard(data)

    return {
        'move': getDirection(board, head, goal),
        'taunt': 'I wont bite'
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '10.0.2.15'),
        port=os.getenv('PORT', '8080'),
        debug = True)
