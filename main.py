import bottle
import os
import random
import json

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
        'tail_type': 'fat-rattle',
        'secondary_color': '#ed7309'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    print(json.dumps(data, indent=4))
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    return {
        'move': direction,
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
