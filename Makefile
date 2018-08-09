CODE = .

.PHONY: clean
clean:
	-find history -type f -name "*py[co]" -delete
	-rm -rf build dist webim.egg-info htmlcov .tox .eggs

.PHONY: lint
lint:
	isort --check-only --recursive $(CODE)
	unify -cr $(CODE)
	flake8 -j 4 --statistics $(CODE)
	yapf -prd $(CODE)

.PHONY: pep8
pep8:
	isort --apply --recursive $(CODE)
	unify -ir $(CODE)
	yapf -ipr $(CODE)

.PHONY: check
check: pep8 lint test
