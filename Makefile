PYTHON=python3
VENV=.venv
AUTOPEP8_OPTS=-i -j0 --aggressive


.NOTPARALLEL:

.PHONY: all
all:

.PHONY: clean
clean:
	rm -rf build dist *.egg-info $(VENV) .tox
	find . -name '*.py[co]' -or -name '*.so*' -or -name '*.dylib' -delete
	find . -depth -name __pycache__ -exec rm -rf {} \;

.PHONY: indent
indent:
	indent Modules/*.c Modules/*.h
	rm -f Modules/*.c~ Modules/*.h~

$(VENV)/bin/pip:
	$(PYTHON) -m venv $(VENV)
	$@ install --upgrade pip setuptools

$(VENV)/bin/autopep8: $(VENV)/bin/pip
	$< install autopep8

.PHONY: autopep8
autopep8: $(VENV)/bin/autopep8
	$< $(AUTOPEP8_OPTS) -r Demo Lib Tests setup.py
