storage:
	poetry run gunicorn -w 5 -b 0.0.0.0:5001 file_storage:app

dev_app:
	poetry run flask --app web_app.app run --debug

lint:
	poetry run flake8 web_app utils file_storage db

start_app:
	poetry run gunicorn -w 5 -b 0.0.0.0:5000 web_app:app
