APPENDCOV = $(shell test -s test_rerun.txt && echo "-a")

test:
	coverage run $(APPENDCOV) \
	   --source "duckbook,booking,api,accounts" \
	   manage.py test `cat test_rerun.txt`
	coverage html
	coverage report
