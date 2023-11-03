# funding-service-design-fund-store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design fund store.

Built with Flask.

## Prerequisites
- python ^= 3.10

# Getting started

## Installation

Clone the repository.

### Create a Virtual environment

```bash
    python3 -m venv .venv
```

### Enter the virtual environment

...either macOS using bash:

```bash
    source .venv/bin/activate
```

...or if on Windows using Command Prompt:

```bash
    .venv\Scripts\activate.bat
```

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

```bash
    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt
```
NOTE: requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run:

```bash
    pip-compile requirements.in

    pip-compile requirements-dev.in
```

## How to use
Enter the virtual environment as described above, then:

```bash
    flask run
```
### Run with Gunicorn

In deployed environments the service is run with gunicorn. You can run the service locally with gunicorn to test

First set the FLASK_ENV environment you wish to test eg:

```bash
    export FLASK_ENV=dev
```
Then run gunicorn using the following command:

```bash
    gunicorn wsgi:app -c run/gunicorn/local.py
```
### Setting up for database development
This service is designed to use PostgreSQL as a database, via SqlAlchemy
When running the service (eg. `flask run`) you need to set the DATABASE_URL environment variable to the URL of the database you want to test with.

Initialise the database:
```bash
    flask db init
```

Then run existing migrations:
```bash
    flask db upgrade
```

Whenever you make changes to database models, please run:
```bash
    flask db migrate
```

This will create the migration files for your changes in /db/migrations.
Please then commit and push these to github so that the migrations will be run in the pipelines to correctly
upgrade the deployed db instances with your changes.

# Database on Paas
Create db service with:

```bash
    cf create-service postgres medium-13 fund-store-dev-db
```

Ensure the following elements are present in your `manifest.yml`. The `run_migrations_paas.py` is what initialises the database, and the `services` element binds the application to the database service.

```yaml
    command: scripts/run_migrations_paas.py && gunicorn wsgi:app -c run/gunicorn/devtest.py

    services:
        - fund-store-dev-db
```

# Seeding Fund Data
To seed fund & round data to db for a specific fund-round (example):

```bash
    docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.fund_round_loaders.load_cof_r2
```

To seed all fund-round data to db:

```bash
    docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.load_all_fund_rounds
```

To load on an environment via cloudfoundry (modify appropriately):

```bash
    cf run-task funding-service-design-fund-store[-dev|-test] --command "python -m scripts.load_all_fund_rounds"
```

To amend the round dates

```bash
    docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --deadline_date "2023-03-30 12:00:00"


    docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --opens_date "2022-10-04 12:00:00" --deadline_date "2022-12-14 11:59:00" --assessment_deadline_date "2023-03-30 12:00:00"
```

To truncate data before re-loading it run

```bash
    docker exec -it $(docker ps -qf "name=fund-store") inv truncate-data
```

### Create and seed local DB
- Make sure your local `DATABASE_URL` env var is set to your local postgres db (this doesn't need to actually exist yet), eg:

```bash
    # pragma: allowlist nextline secret
    DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/fsd_fund_store
```

- Create and seed using the following scripts:

```bash
        python -m scripts.fund_round_loaders.{load_config_script}
```

### Build with Paketo

[Pack](https://buildpacks.io/docs/tools/pack/cli/pack_build/)

[Paketo buildpacks](https://paketo.io/)

```bash
    pack build <name your image> --builder paketobuildpacks/builder:base
```

Example:

    [~/work/repos/funding-service-design-fund-store] pack build paketo-demofsd-app --builder paketobuildpacks/builder:base
    ***
    Successfully built image paketo-demofsd-app


You can then use that image with docker to run a container

```bash
    docker run -d -p 8080:8080 --env PORT=8080 --env FLASK_ENV=dev [envs] paketo-demofsd-app
```

`envs` needs to include values for each of:
SENTRY_DSN
GITHUB_SHA

```bash
    docker ps -a
    CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                    PORTS                    NAMES
    42633142c619   paketo-demofsd-app          "/cnb/process/web"       8 seconds ago    Up 7 seconds              0.0.0.0:8080->8080/tcp   peaceful_knuth
```

# Pipelines

Place brief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities. Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.
* Tag to Release - This is a simple pipeline that will create the tag required and push an image, built with Paketo, to the GHCR with that tag

# Testing

## Unit

To run all tests in a development environment run:
```bash
    pytest
```

# Extras

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

```bash
    pip install pre-commit black

    pre-commit install
```

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.

In deploy.yml, there are three environment variables called users, spawn-rate and run-time. These are used
to override the locust config if the performance tests need to run with different configs for fund store.

## Copilot Initialisation

Copilot is the deployment of the infrastructure configuration, which is all stored under the copilot folder. The manifest files have been pre-generated by running through various initialisation steps that create the manifest files by prompting a series of questions, but do not _deploy_ the infrastructure.

For each AWS account, these commands will need to be run _once_ to initialise the environment:

`copilot app init pre-award` - this links the pre-award app with the current service, and associates the next commands with the service. Essentially, this provides context for the service to run under

```bash
    copilot init \
    --name fsd-fund-store \
    --app pre-award \
    --type 'Backend Service' \
    --image 'ghcr.io/communitiesuk/funding-service-design-fund-store:latest' \
    --port 80
```

This will initalise this service, using the current created image
