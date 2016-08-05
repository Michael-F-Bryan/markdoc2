TESTS  = tests
COV_ARGS = --source=$(SOURCES) --branch
PYTEST_ARGS = -v
PYLINT_ARGS = --reports=no --output-format=colorized
BROWSER = xdg-open



coverage:
	coverage run $(COV_ARGS) -m pytest $(PYTEST_ARGS) $(TESTS)
	coverage html
	coverage report
	@echo 
	$(RM) .coverage
	$(BROWSER) coverage_html_report/index.html > /dev/null 2>&1

tests:
	py.test $(TESTS) $(PYTEST_ARGS)

lint:
	-pylint $(PYLINT_ARGS) flask_api_builder.py

changes:
	auto-changelog -o $(TEMP_CHANGES)
	pandoc --from=markdown --to=rst -o CHANGELOG.rst $(TEMP_CHANGES)
	$(RM) $(TEMP_CHANGES)


bump-patch:
	bumpversion patch

bump-minor:
	bumpversion minor

bump-major:
	bumpversion major


clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	
clean-test: ## remove test and coverage artifacts
	rm -f .coverage

clean: clean-pyc clean-test


.PHONY: bump-patch bump-minor bump-major
.PHONY: coverage tests lint changes
.PHONY: clean-pyc clean-test
