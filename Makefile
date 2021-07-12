build:
	pyinstaller --onefile sentinel.py

install:
	python3 -m pip install -r requirements.txt

lint:
	pylint -v ./**/*py

test:
	 coverage run -m pytest ./tests --junitxml=report.xml

coverage:
	coverage html