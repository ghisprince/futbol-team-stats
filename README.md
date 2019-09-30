# soccer-player-stats
Web-app to store and report a soccer team and player's stats.


### Statistics stored
 * by team
   * players
   * matches
   * opponent
   * competitions (tournaments & seasons)
 * by player
   * start
   * minutes played
   * shots (with location)
   * goals
   * assists
   * yellow and red cards
   * corners
   * substituted due to injury

## Deploying app
Backend rest api written in python.  Uses flask, sqlalchemy, marshmallow, flask-restful.

### Python
Create env using conda
```
conda create -n futbol python=3.6
conda activate futbol
```

Create env using virtualenv
```
virtualenv env --python=python3.6
source env/bin/activate

```

Install requirements
```
pip3 install -r requirements.txt
```

### run flask server
```
python manage.py server
```

Frontend/client SPA.  Uses:  in vuejs, vuetify, Vue CLI 3.

### Javascript

```
cd client
npm install
npm run serve
npm build serve
```

## Additional stuff

### tests
Running backend tests

```
py.test -s test
```
