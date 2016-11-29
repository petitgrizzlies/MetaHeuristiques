all: compile

compile:
	python3 setup.py build_ext --inplace

html: compile
	cython -a *.pyx

see: html
	firefox *.html

run: compile
	./core.py
