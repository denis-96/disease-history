up:
	docker-compose up -d
down:
	docker-compose down && docker network prune --force
run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload