.PHONY: all test clean docs

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "__pycache__" -type d -exec rm -rf {} \;
	find . -name "*.egg-info" -type d -exec rm -rf {} \; || true
	rm -rf build/ dist/ \
	       .tox/
	       htmlcov/ .coverage \
	       *.egg

test:
	python setup.py test
