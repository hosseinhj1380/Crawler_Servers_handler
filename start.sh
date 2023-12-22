
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

uvicorn config:app --host 0.0.0.0 --port 8000 --reload

cd ./app/graph

uvicorn.run schema:app  --host=127.0.0.1 --port 7000 --reload 