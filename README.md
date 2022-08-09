# Run

> uvicorn sql_app.main:app --reload

to test

default database is sqlite, if wanna switch to postgres than change settings
under sql_app folder/ database.py's SQLALCHEMY_DATABASE_URL
From

> SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

To

> SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost/ash999"

BTW need to create schemas on postgresql first
