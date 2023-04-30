.PHONY: clean_db
clean_db:
	rm app.db

.PHONY: init_db
init_db:
	flask db upgrade

.PHONY: build docker_tag
build: ## Create docker image with dependencies needed for development.
	docker-compose build --build-arg COMMIT_HASH=$(git rev-parse HEAD)

.PHONY: run
run:
	docker-compose --env-file=.env up -d

.PHONY: stop
stop:
	docker-compose stop

.PHONY: restart
restart: stop build run

.PHONY: docker_tag
docker_tag:
	docker tag <image-name>:<docker-compose-build-label> <image-name>:<commit-hash>
