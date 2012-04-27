all: uninstall clean dist install

dist:
	python setup.py sdist

uninstall:
	pip uninstall gg -y

install:
	pip install dist/gg-0.0.0.tar.gz

init:
	pip install -r requirements/dev.txt --use-mirrors

test:
	nosetests tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf gg.egg-info/
