.PHONY: clean_db
clean_db:
	rm app.db
	rm -rf migrations

.PHONY: init_db
init_db:
	flask db init
	flask db migrate
	flask db upgrade

.PHONY: build
build:
	docker build -t microblog:latest .

.PHONY: run
run:
	docker-compose --env-file .env up -d --build

.PHONY: stop
stop:
	docker-compose stop

.PHONY: restart
restart: down build up

