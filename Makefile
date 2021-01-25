# Reference: https://cs.colby.edu/maxwell/courses/tutorials/maketutor/
# Reference: https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects
MYDIR = .

RUN_TEST = python -m pytest -v

test: $(MYDIR)/tests/test_*.py
	for file in $^ ; do $(RUN_TEST) "$${file}"; done
