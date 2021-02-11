# Pocket Mine 3 Hack
A website based on Flask and Vue which provides tools of the game, Pocket Mine 3.

## Backend Framework
* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/)
* [psycopg2](https://pypi.org/project/psycopg2/)

## Frontend Framework
* [Vue.js](https://vuejs.org/)

## Application Setup
* Start the server
  * Refer to [Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/#run-the-application)
  * Windows
    * Execute "**scripts/run_server.bat**"
* Initialize the database
  * Refer to [Flask-Migrate tutorial](https://flask-migrate.readthedocs.io/en/latest/#example)
  * Windows
    * Execute "**scripts/db/init.bat**"
    * Execute "**scripts/db/migrate.bat**"
    * Execute "**scripts/db/upgrade.bat**"
* Load defautl database data
  * Execute command line "**flask load_default**"
    * <span style="color:red">Note: Do not execute multiple times!</span>
  * Windows
    * Execute "**scripts/db/load_default.bat**"