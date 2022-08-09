run
uvicorn sql_app.main:app --reload
to test

default database is sqlite, if wanna switch to postgres than change settings
under

> > sql_app
> > database.py's SQLALCHEMY_DATABASE_URL
