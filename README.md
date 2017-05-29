# soccer-player-stats
Web-site to collect and report soccer team and player's stats.

###Statistics tracked
 * by team
  * matches
  * players
  * campaigns (tournaments, seasons)
 * by player
  * started
  * minutes played
  * cards
  * corners
  * shots
   * goals
   * assists
  * goal
  * assist


## Deploying
To setup and run get repo, then do
```python
pip install -r requirements

# loads toy data to play with
python scripts\load_data.py

# run flask local server
python manage.py server

```


## Stack
 * client side: TBD (reactjs, vue ?), Bootstrap
 * server side: python, flask, sqlalchemy, marshmallow, flask-restful

### Code foundation
 * [JackStouffer/Flask-Foundation](https://github.com/JackStouffer/Flask-Foundation)
 * [Leo-G/Flask-Scaffold](https://github.com/Leo-G/Flask-Scaffold)