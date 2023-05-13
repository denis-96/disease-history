up:
	docker-compose up -d
down:
	docker-compose down && docker network prune --force
run:
	uvicorn src.main:app --host localhost --port 8000 --reload
clear revisions:
	rm ./migrations/versions/*.py
revision:
	alembic revision --autogenerate
upgrade:
	alembic upgrade head
