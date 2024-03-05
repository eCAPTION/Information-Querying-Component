start-docker:
	docker compose -f ./docker-compose.yaml --env-file .env.docker up --build -d

stop-docker:
	docker compose -f ./docker-compose.yaml --env-file .env.docker down
