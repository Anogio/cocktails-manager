run:
	uvicorn app:app --reload

run_prod:
	ENVIRONMENT=production uvicorn app:app

migrate:
	alembic upgrade head

migrate_prod:
	ENVIRONMENT=production env $(cat db_secrets_prod | xargs) alembic upgrade head

seed:
	python -m db.seed.cocktails_seed

format:
	black . && isort .

install:
	pip install -r requirements.txt -r requirements-dev.txt
