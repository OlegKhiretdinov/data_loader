storage:
	poetry run flask --app file_storage.app run --port 5001

start_app:
	poetry run flask --app web_app.app run --debug

lint:
	 flake8 web_app utils file_storage
