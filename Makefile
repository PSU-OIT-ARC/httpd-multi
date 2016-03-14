distribution = psu.oit.arc.httpdmulti
egg_info = $(distribution).egg-info
package = httpdmulti
script_name = $(package)
venv = .env
python_version ?= 3.3
venv_python = python$(python_version)

init: $(venv) $(egg_info)

reinit: clean init

$(venv):
	virtualenv -p $(venv_python) $(venv)

$(egg_info):
	$(venv)/bin/pip install -r requirements.txt

prefix ?= /usr/local
install: $(venv) $(egg_info)
	ln -is $(CURDIR)/$(venv)/bin/$(script_name) $(prefix)/bin/$(script_name)

clean:
	rm -rf $(venv)
	rm -rf $(egg_info)
	rm -rf build
	rm -rf dist
	find . -name __pycache__ -type d -print0 | xargs -0 rm -rf

.PHONY = init install reinit clean
