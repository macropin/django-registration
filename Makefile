.PHONY: install\
		test\
		lint\
		coverage\
		clean

install:
	# Let developers manage their python versions
	# and Django versions independently
	pip install coveralls flake8

test:
	python setup.py test

lint:
	flake8

clean:
	find . -type f -name '*.py[cod]' -delete

