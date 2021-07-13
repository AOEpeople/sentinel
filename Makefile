run-tests: install-dependencies install-dev-dependencies lint test
run-package: install-dependencies package

package:
	python -m pip install pyinstaller
	pyinstaller --onefile main.py --name $(PACKAGE_NAME)

lint:
	pylint -v ./**/*py

test:
	 coverage run -m pytest ./tests --junitxml=report.xml

coverage:
	coverage html

install-dependencies:
	python -m pip install -r requirements.txt

install-dev-dependencies:
	pip install pylint pytest coverage
	pip install -r requirements.txt