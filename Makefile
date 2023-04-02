.PHONY: clean_db
clean_db:
	rm app.db
	rm -rf migrations

.PHONY: init_db
init_db:
	flask db init
	flask db migrate
	flask db upgrade

.PHONY: run
run:
	flask run --host=0.0.0.0 --port=8000
