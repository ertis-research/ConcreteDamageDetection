# Reference: https://cs.colby.edu/maxwell/courses/tutorials/maketutor/
# Reference: https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects
PACKAGE_NAME = concrete
MYDIR = .
VSCODE_BIN = /home/vscode/.local/bin
RUN_TEST = python -m pytest -v

install:
	pip install --editable $(PACKAGE_NAME)

uninstall:
	pip uninstall -y $(PACKAGE_NAME)
	rm -dfr $(PACKAGE_NAME)/*.egg*
	rm $(VSCODE_BIN)/concrete

test: $(MYDIR)/tests/test_*.py
	for file in $^ ; do $(RUN_TEST) "$${file}"; done
