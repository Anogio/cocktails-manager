run:
	uvicorn app:app --reload

run_prod:
	ENVIRONMENT=production uvicorn app:app

migrate:
	alembic upgrade head

migrate_prod:
	ENVIRONMENT=production alembic upgrade head

seed:
	python -m db.seed.cocktails_seed

seed_prod:
	ENVIRONMENT=production python -m db.seed.cocktails_seed


format:
	black . && isort .

install:
	pip install -r requirements.txt -r requirements-dev.txt
