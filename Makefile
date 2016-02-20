.PHONY: installdeps\
		build\
		test\
		lint\
		coverage\
		clean

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

