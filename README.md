# soccer-player-stats
Web-app to capture and report a team and player's stats.


### Statistics
 * by team
   * players
   * matches
   * opponent
   * competitions (tournaments & seasons)
 * by player
   * starts
   * minutes played
   * shots
   * goals
   * assists
   * yellow and red cards
   * corners
   * injury


## Deploying app

### Python
Install requirements
```
virtualenv env --python=python3.6
source env/bin/activate
pip3 install -r backend/requirements.txt
```

### run flask local server
```
python manage.py server
```

### Javascript
Using webpack to compile js & vue files

```
cd client
npm install
npm run serve
npm build serve
```

### Tests
To run backend tests
```
py.test -s test
```

### Toy data
Data is included to play/dev with. To load it

```
python scripts\load_data.py
```


## Stack
 * client side: VueJS, webpack
 * server side: python, flask, sqlalchemy, marshmallow, flask-restful

### Code foundation
 * vue-cli3
 * [JackStouffer/Flask-Foundation](https://github.com/JackStouffer/Flask-Foundation)
 * [Leo-G/Flask-Scaffold](https://github.com/Leo-G/Flask-Scaffold)
