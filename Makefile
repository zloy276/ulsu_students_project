SHELL := /bin/bash

SERVER=knauf_server

test:
	docker exec -i ${SERVER} poetry run coverage run --source='.' manage.py test && docker exec -i ${SERVER} poetry run coverage report

lint:
	docker exec -i ${SERVER} poetry run prospector --uses django --tool pylint

mypy:
	docker exec -i ${SERVER} poetry run mypy apps

makemirations:
	docker exec -i ${SERVER} poetry run python3 manage.py makemigrations

migrate:
	docker exec -i ${SERVER} poetry run python3 manage.py migrate

bash:
	docker exec -it ${SERVER} bash

shell:
	docker exec -it ${SERVER} poetry run python3 manage.py shell
