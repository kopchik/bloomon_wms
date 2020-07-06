.DEFAULT_GOAL := run-example-in-container
IMAGE_NAME = alex-wms

.PHONY: requirements
requirements:
	sort-requirements ./requirements/*.in
	ls ./requirements/*.in | xargs -L1 pip-compile -U

.PHONY: format
format:
	isort *.py
	black *.py
	flake8 *.py

.PHONY: test
test:
	pytest -s --pdb

.PHONY: image
image:
	docker build -t $(IMAGE_NAME) .

.PHONY: run-example-in-container
run-example-in-container:
	docker run -it --rm $(IMAGE_NAME)