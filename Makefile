clean:
	-rm -r build
	-rm -r debian/reasonablepy
	python setup.py clean

build:
	python setup.py build

install:
	python setup.py install --root="debian/reasonablepy/"

	
