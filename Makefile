# Reference: https://cs.colby.edu/maxwell/courses/tutorials/maketutor/
# Reference: https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects
PACKAGE_NAME = concrete
VSCODE_BIN = /home/vscode/.local/bin
RUN_TEST = python -m pytest -v

start:
	pip install -r requirements.txt -r yolov3/requirements.txt
	# Include dataset downloading

build:
	python setup.py sdist

develop:
	pip install --editable .

clean:
	pip uninstall -y $(PACKAGE_NAME)
	rm -dfr $(PACKAGE_NAME).egg*
	rm -dfr .pytest_cache .neptune
	rm $(VSCODE_BIN)/concrete

test: $(PACKAGE_NAME)/tests/test_*.py
	for file in $^ ; do $(RUN_TEST) "$${file}"; done
