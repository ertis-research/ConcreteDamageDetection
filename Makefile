# Reference: https://cs.colby.edu/maxwell/courses/tutorials/maketutor/
# Reference: https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects
PACKAGE_NAME = concrete
VSCODE_BIN = /home/vscode/.local/bin
RUN_TEST = python -m pytest -v
ORIGINAL_CODEBRIM_DATASET = https://zenodo.org/record/2620293/files/CODEBRIM_original_images.zip
CODEBRIM_DIRECTORY = datasets/CODEBRIM
HONGKONG_HIGHWAYS_DEPARTMENT_DIRECTORY = datasets/HONGKONG_HIGHWAYS_DEPARTMENT
ORIGINAL_HONGKONG_HIGHWAYS_DEPARTMENT = gdown --id 1-g77ciKmHNIK_YD0z8puECtEirsOg01Z --output

start:
	pip install -r requirements.txt -r yolov3/requirements.txt -r yolov5/requirements.txt

download:
	mkdir -p $(HONGKONG_HIGHWAYS_DEPARTMENT_DIRECTORY)
	if ! [ -f $(HONGKONG_HIGHWAYS_DEPARTMENT_DIRECTORY)/dataset.rar ]; then $(ORIGINAL_HONGKONG_HIGHWAYS_DEPARTMENT) $(HONGKONG_HIGHWAYS_DEPARTMENT_DIRECTORY)/dataset.rar; fi
	cd $(HONGKONG_HIGHWAYS_DEPARTMENT_DIRECTORY); unrar x dataset.rar; cd -
	mkdir -p $(CODEBRIM_DIRECTORY)
	if ! [ -f $(CODEBRIM_DIRECTORY)/CODEBRIM_original_images.zip ]; then curl -o $(CODEBRIM_DIRECTORY)/CODEBRIM_original_images.zip $(ORIGINAL_CODEBRIM_DATASET); fi
	cd $(CODEBRIM_DIRECTORY); jar -xvf CODEBRIM_original_images.zip; cd -

build:
	python setup.py sdist

develop:
	pip install --editable .

clean-dev:
	pip uninstall -y $(PACKAGE_NAME)
	rm -dfr $(PACKAGE_NAME).egg*
	rm $(VSCODE_BIN)/concrete

clean-all:
	$(MAKE) clean-dev
	rm -dfr .pytest_cache .neptune datasets runs weights
	rm *.pt

test: $(PACKAGE_NAME)/tests/test_*.py
	for file in $^ ; do $(RUN_TEST) "$${file}"; done
