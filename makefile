run :
	uv run manage.py runserver 0.0.0.0:7000

tailwind :
	uv run manage.py tailwind start

migrate :
	uv run manage.py migrate

makemigrations :
	uv run manage.py makemigrations