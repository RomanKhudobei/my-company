makemigrations:
	docker exec -it backend flask db migrate -m "$(message)"

migrate:
	docker exec -it backend flask db upgrade

chmod_migrations:
	find ../migrations -type f -print0 | xargs -0 sudo chmod 666 && sudo chmod 777 ../migrations/versions && find ../migrations/versions -type f -print0 | xargs -0 sudo chmod 666

test:
	docker exec -it backend pytest tests/$(tests) $(args)
