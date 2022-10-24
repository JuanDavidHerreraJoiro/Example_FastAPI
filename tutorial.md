# Tutorial

pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv

py –m venv venv
.\venv\Scripts\activate

docker-compose build

docker-compose up

docker-compose run app alembic revision --autogenerate -m "New Migration"

docker-compose run app alembic upgrade head

docker-compose build

docker-compose up
