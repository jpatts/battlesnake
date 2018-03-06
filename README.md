# Description

[BattleSnake AI](http://battlesnake.io) written in Python, using weighted graphs and A* pathfinding to reach points of maximum entropy.

Visit [battlesnake.io/readme](http://battlesnake.io/readme) for API documentation.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### Requirements

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1) [Fork this repo](https://github.com/jpatts/battlesnake).

2) Clone repo to your development environment:
```
git clone git@github.com:username/battlesnake.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server (make sure to specify your hostname to be your IP):
```
python app/main.py
```
   
5) Run the game server locally with Docker:
```
sudo docker run -it --rm -p 3000:3000 sendwithus/battlesnake-server
```

## Deploying to Heroku

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```
