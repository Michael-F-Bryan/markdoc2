PROJECT = markdoc2
TESTS  = tests
COV_ARGS = --source=$(SOURCES) --branch
PYTEST_ARGS = -v -s
BROWSER = xdg-open


tests:
	py.test $(TESTS) $(PYTEST_ARGS)

coverage:
	coverage run $(COV_ARGS) -m pytest $(PYTEST_ARGS) $(TESTS)
	coverage html
	coverage report
	@echo 
	$(RM) .coverage
	$(BROWSER) coverage_html_report/index.html > /dev/null 2>&1

lint:
	-flake8 

changes:
	auto-changelog -o $(TEMP_CHANGES)
	pandoc --from=markdown --to=rst -o CHANGELOG.rst $(TEMP_CHANGES)
	$(RM) $(TEMP_CHANGES)

# Make requirements file and skip any error lines (starting with ##......)
requirements:
	(pip freeze | sed '/##/d' > requirements-dev.txt) 2> /dev/null


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
