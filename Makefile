mig:
	python3 manage.py makemigrations && python3 manage.py migrate

celery:
	celery -A root worker -l INFO

beat:
	celery -A root beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

flower:
	celery -A root.celery.app flower --port=5001