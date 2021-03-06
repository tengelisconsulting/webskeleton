.PHONY: typecheck
typecheck:
	python -m mypy ./webskeleton

.PHONY: format
format:
	python -m black ./webskeleton

.PHONY: check-format
check-format:
	python -m black --check ./webskeleton
	python -m flake8 ./webskeleton

.PHONY: install
install:
	python -m pip install -r requirements.txt

.PHONY: install-dev
install-dev:
	python -m pip install --upgrade .

.PHONY: test
test: install-dev
	./test/run.sh

.PHONY: dist
dist: ci
	python ./setup.py sdist

.PHONY: publish
publish:
	python -m twine upload ./dist/*

.PHONY: clean
clean:
	rm -rf ./dist


.PHONY: ci
ci: typecheck check-format test
