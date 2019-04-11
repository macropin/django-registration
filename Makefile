.PHONY: installdeps\
		build\
		test\
		lint\
		clean \
		release

installdeps:
	pip install -U -r requirements.txt

build:
	invoke build $(ARGS)

test:
	invoke test

lint:
	invoke lint

clean:
	invoke clean $(ARGS)

release: clean lint test
	ifeq ($(TAG_NAME),)
	$(error Usage: make release TAG_NAME=<tag-name>)
	endif
	# NOTE(joshblum): First you should update the changelog and bump the
	# version in setup.py
	git clean -dxf
	git tag $(TAG_NAME)
	git push --tags
	# Create the wheels for Python2 and Python3.
	python setup.py sdist bdist_wheel --universal
	# To check whether the README formats properly.
	twine check dist/*
	# Upload to pypi.
	twine upload dist/*
