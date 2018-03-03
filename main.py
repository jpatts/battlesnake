import bottle
import os
import random
import json
import numpy as np

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
        'name': 'jordan',
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

    # add players location to board
    playerLocation = data['you']['body']['data']
    for i in range(len(playerLocation)):
        x = playerLocation[i]['x'] + 1
        y = playerLocation[i]['y'] + 1
        board[x, y] = 0

    # add enemies location to board
    enemiesLocation = data['snakes']['data']
    for i in range(len(enemiesLocation)):
        snake = data['snakes']['data'][i]['body']['data']
        for j in range(len(snake)):
            x = snake[j]['x'] + 1
            y = snake[j]['y'] + 1
            board[x, y] = 0

    # add food to board
    food = []
    for i in range(len(data['food']['data'])):
        x = data['food']['data'][i]['x'] + 1
        y = data['food']['data'][i]['y'] + 1
        food.append([x, y])
        board[x, y] = 2
    
    return board, food

def getDirection(data, board, food):
    # get player snakes head
    x = data['you']['body']['data'][0]['x'] + 1
    y = data['you']['body']['data'][0]['y'] + 1
    head = [x, y]

    # find closest food
    for i in range(len(food)):
        x = food[i][0] - head[0]
        y = food[i][1] - head[1]
        food[i] = [x, y]
    closest = np.amin(food, axis=0)
    
    # choose best directions based on nearest food available
    directions = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
    if(abs(closest[0] + 1) < abs(closest[0])):
        directions['left'] = -1
    if(abs(closest[0] - 1) < abs(closest[0])):
        directions['right'] = 1
    if(abs(closest[1] + 1) < abs(closest[1])):
        directions['up'] = -1
    if(abs(closest[1] - 1) < abs(closest[1])):
        directions['down'] = 1

    # choose an available direction close to food
    if(board[head[0] + directions['left'], head[1]] >= 1):
        return 'left'
    elif(board[head[0] + directions['right'], head[1]] >= 1):
        return 'right'
    elif(board[head[0], head[1] + directions['up']] >= 1):
        return 'up'
    elif(board[head[0], head[1] + directions['down']] >= 1):
        return 'down'

    # if no available direction exists closer to food, choose an arbitrary direction
    if(board[head[0] - 1, head[1]] >= 1):
        return 'left'
    elif(board[head[0] + 1, head[1]] >= 1):
        return 'right'
    elif(board[head[0], head[1] - 1] >= 1):
        return 'up'
    else:
        return 'down'

@bottle.post('/move')
def move():
    data = bottle.request.json
    #print(json.dumps(data, indent=4))

    board, food = getBoard(data)

    return {
        'move': getDirection(data, board, food),
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
