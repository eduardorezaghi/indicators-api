# KPI - OPI indicators API


# Requirements
- Python 3.13 or greater.
- pip.
- dmypy for type checking.

# Installation
Run the following command to install the required dependencies:
```bash
$ pip install -r requirements.txt
```

# Running the API
You can run the API in two ways:
1. Using the `flask` command.
2. Using the `python` command, running the main module directly.

See:
```bash
$ flask --app src.main run --port 7012
```
or
```bash
$ python -m src.main
```

# Testing the API
You can test the API using the following methods.
- Manually, using a tool like `curl` or `Postman`.
- Running automated tests using the `pytest` command.

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