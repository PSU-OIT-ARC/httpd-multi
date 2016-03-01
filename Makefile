venv = .env
venv_python = python3.3

init: venv install

venv: $(venv)
$(venv):
	virtualenv -p $(venv_python) $(venv)

install:
	pip install -r requirements.txt

.PHONY = init venv
