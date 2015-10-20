APPENDCOV = $(shell test -s test_rerun.txt && echo "-a")
MODULES = duckbook booking api accounts

test:
	coverage run $(APPENDCOV) \
	   --source `echo $(MODULES) | sed 's/ /,/g'` \
	   manage.py test `cat test_rerun.txt`
	coverage html
	coverage report
	@echo "Coverage data is available in HTML format under the htmlcov directory"

lint:
	rm -rf pylint
	pylint --rcfile=.pylintrc $(MODULES) || true
	mkdir pylint
	sh -c 'for file in pylint_*; do \
	    o="$${file#pylint_}"; \
	    mv "$$file" pylint/$$o; \
        done'
	@echo "lint data is available in TXT format under the pylint directory"
