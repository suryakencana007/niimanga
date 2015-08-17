# makefile automate
VENV := venv/
PY := $(VENV)bin/python
PIP := $(VENV)bin/pip
PASTER := $(VENV)bin/pserve
GUNICORN := $(VENV)bin/gunicorn
CELERY := $(VENV)bin/celery
ALEMBIC := $(VENV)bin/alembic

CLOSURE_BUILD := scripts/closure/
PUBLIC_DIR := moori/public/

PROD_INI = production.ini
DEV_INI = development.ini

# untuk production live
.PHONY: run_app
run_app:
	$(GUNICORN) --paster $(PROD_INI) --worker-class gevent &
.PHONY: run_celery
run_celery:
	$(CELERY) worker -A pyramid_celery.celery_app --ini $(DEV_INI) -B &
.PHONY: run
run: run_celery run_app

.PHONY: stop
stop: stop_app stop_celery
.PHONY: stop_celery
stop_celery:
	pkill celery
.PHONY: stop_app
stop_app:
	pkill gunicorn

# untuk alembic stage
.PHONY: alembic_init alembic_push alembic_pull alembic_migrate
alembic_init:
	$(ALEMBIC) -c $(DEV_INI) init migrations
alembic_push:
	$(ALEMBIC) -c $(DEV_INI) upgrade head
alembic_commit:
	$(ALEMBIC) -c $(DEV_INI) revision --autogenerate -m "${MSG}"
alembic_migrate:
	$(ALEMBIC) -c $(DEV_INI) revision -m "${MSG}"


# untuk development stage
.PHONY: run_app_dev closure-compile closure-serve run_sass
run_app_dev:
	$(PASTER) $(DEV_INI) --reload
closure-compile:
	java -jar $(CLOSURE_BUILD)plovr.jar build $(CLOSURE_BUILD)plovr.json > $(PUBLIC_DIR)js/app.min.js
closure-serve:
	java -jar $(CLOSURE_BUILD)plovr.jar serve $(CLOSURE_BUILD)plovr.json

.PHONY: run_dev
run_dev: run_app_dev