lint:
	flake8
	mypy -p server

pytest:
	pytest tests

test: lint pytest

install:
	pip install -r requirements.txt

start_server: install
	gunicorn -w 4 -b 127.0.0.1:8000 server:app&

dev_server:
	FLASK_ENV=development FLASK_APP=server:app flask run

clean:
	find . -name *.out -or -name *.log -or -name .*.swp -or -name .*.swo -or -name .DS_Store -or -name .swp -or -name *.pyc | xargs -n 1 rm
	rm -rf .mypy_cache
	rm -rf .pytest_cache
