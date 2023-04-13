.PHONY: clean_db
clean_db:
	rm app.db
	rm -rf migrations

.PHONY: init_db
init_db:
	flask db init
	flask db migrate
	flask db upgrade

.PHONY: build docker_tag
build: ## Create docker image with dependencies needed for development.
	docker-compose build --build-arg COMMIT_HASH=$(git rev-parse HEAD)

.PHONY: run
run: ## Execute www docker container.
	docker-compose --env-file=.env up -d

.PHONY: stop
stop:
	docker-compose stop

.PHONY: restart
restart: down build up

.PHONY: docker_tag
docker_tag:
	docker tag <image-name>:<docker-compose-build-label> <image-name>:<commit-hash>
