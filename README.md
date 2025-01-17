# KPI - OPI indicators API

This is an API project for Stone's backend developer challenge.  
It's **nearly** a full-featured API, with the following features:
- Create an atendimento record.
- List all atendimento records.
- Update an atendimento record.
- Import a CSV file with atendimento records.

For all **creational** operations, the app creates the related entities (Client, Polo, and Angel) if they don't exist.  
Of course, this isn't optimal. But for simplicity and time constraints, I consider it a good solution.

For the **import** operation, the app uses Celery to process the CSV file in the background,  
with an asynchronous operation using `asyncpg` to insert the records in the database.

It's, by time-constraints, missing:
- A more robust error handling.
- A more robust input validation (with Pydantic or Marshmallow, for example).
- A more robust logging system.
- Swagger documentation.


# Table of contents
- [KPI - OPI indicators API](#kpi---opi-indicators-api)
- [Table of contents](#table-of-contents)
- [Main architecture](#main-architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Migrations](#migrations)
- [Running the API](#running-the-api)
- [Testing the API](#testing-the-api)
- [Code coverage](#code-coverage)


# Main architecture

In a nutshell, the app is divided into the following parts.
- `src/app.py`: The main module, where the app is created.
- `src/api/`: The API routes.
- `src/domain/`: The domain entities, mainly for abstracting data format.
- `src/models/`: The database models, using SQLAlchemy.
- `src/repositories/`: The database repositories, for querying the database.
- `src/services/`: The business logic services, for handling the business rules.
- `src/tasks/`: The Celery tasks, for background processing.

It uses Celery for background processing, with Redis as the broker, for running the CSV import operation.

# Requirements
- Python 3.13 or greater.
- pip.
- (Optional) dmypy for type checking.

# Installation
Run the following command to install the required dependencies:
```bash
$ pip install -r requirements.txt
```

# Migrations
By default, the API uses a PostgreSQL database.  
This app uses Alembic (with Flask-Alembic) to manage the database migrations.  
For this app, however, there is a hook that creates the database and the tables automatically, if they not exists.
(may change to use explicit migrations, perhaps?)

But, it's easy to create new migrations/or apply the most recent ones.

Apply the most recent migrations:
```bash
$ flask --app src.app db upgrade
```


# Running the API
You can run the API in three ways:
1. Using the `flask` command.
2. Using the `python` command, running the main module directly.
3. Using `docker-compose`.

See:
```bash
$ flask --app src.app run --port 7012
```
or
```bash
$ python -m src.app
```

For the third method, you can use the following command:
```bash
$ docker-compose up -d
```

The following containers will be created:
- `web`: The API container.
- `database`: The database container (PostgreSQL).
- `redis`: The Redis container (Celery broker).
- `celery_worker`: The Celery worker container.
- `nginx`: The Nginx container (reverse proxy/load balancer).

These containers will be available at the following ports:
- `web`: 7012
- `database`: 5432
- `redis`: 6379
- `nginx`: 80 (redirects to port 7012)

# Testing the API
You can test the API using the following methods.
- Manually, using a tool like `curl` or `Postman`.
- Running automated tests using the `pytest` command.
- Using `Insomnia` with the provided workspace.

For the first method, you can use the following command:
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"data": "Hello, World!"}' http://localhost:7012/echo
# with httpie
$ http POST http://localhost:7012/echo data="Hello, World!"
```

For the second method, you can use the following command:
```bash
$ pytest
```
For the third method, you can import the provided workspace in `Insomnia`.  
You may found the following requests already created:

- `GET http://localhost/api/v1/atendimento` to list all records.
- `POST http://localhost/api/v1/atendimento` to create a new record.
- `POST http://localhost:7012/api/v1/atendimento/import_csv` to import the CSV file provided with the challenge.
- `PUT http://localhost:7012/api/v1/atendimento/1` to update the first record.

# Code coverage
Running pytest allows you to see the code coverage of the tests.  
Below, the most recent coverage report.
```txt
---------- coverage: platform win32, python 3.13.1-final-0 -----------
Name                                         Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------------------
src\__init__.py                                 32      2      0      0    94%   18, 25
src\api\__init__.py                              2      0      0      0   100%
src\api\atendimento_routes.py                   81     24     20      1    63%   24-25, 100-101, 111, 121-138, 143-154
src\api\base_routes.py                           2      0      0      0   100%
src\app.py                                       6      0      0      0   100%
src\celery_utils.py                              9      0      0      0   100%
src\config.py                                   16      0      0      0   100%
src\database.py                                 35     11      2      0    65%   34-38, 42-43, 47-50, 66-67
src\domain\__init__.py                           4      0      0      0   100%
src\domain\angel.py                             18      6      4      0    55%   14, 22-28
src\domain\atendimento.py                       47      2      4      1    94%   17->16, 44, 77
src\domain\client.py                            18      1      4      0    95%   14
src\domain\polo.py                              18      6      4      0    55%   16, 24-30
src\models\__init__.py                           5      0      0      0   100%
src\models\angel.py                              9      0      0      0   100%
src\models\atendimento.py                       17      0      0      0   100%
src\models\base_model.py                        10      0      0      0   100%
src\models\client.py                             7      0      0      0   100%
src\models\polo.py                               8      0      0      0   100%
src\repositories\__init__.py                     4      0      0      0   100%
src\repositories\angel_repository.py            37      5      0      0    86%   42-44, 84, 87
src\repositories\atendimento_repository.py      82     32      4      1    62%   81-83, 91-111, 116-137, 140-161, 166, 176-178
src\repositories\base.py                         4      0      0      0   100%
src\repositories\client_repository.py           58     26      0      0    55%   25-27, 30-32, 41-43, 51-64, 67-79
src\repositories\polo_repository.py             65     32      0      0    51%   25-27, 30-32, 41-43, 51-64, 67-79, 85-90
src\services\atendimento_service.py             40      3      6      3    87%   26, 45->47, 47->49, 49->53, 64, 72
src\tasks\__init__.py                            1      0      0      0   100%
src\tasks\csv_processor.py                      15      0      0      0   100%
----------------------------------------------------------------------------------------
TOTAL                                          650    150     48      6    74%
Coverage HTML written to dir htmlcov
```
