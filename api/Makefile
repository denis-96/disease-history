up:
	docker-compose up -d
down:
	docker-compose down && docker network prune --force
run:
	pipenv run uvicorn src.main:app --host localhost --port 8000 --reload
clear revisions:
	rm -r ./migrations/versions/*
revision:
	alembic revision --autogenerate
upgrade:
	alembic upgrade head
