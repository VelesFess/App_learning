alembic upgrade head
cd app
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
