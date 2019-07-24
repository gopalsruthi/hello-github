install:
	pip install -r requirements.txt

setup:
	virtualenv -p python3 ~/.venv	#Make sure you create a virtual env first
	#use virtualenv like this:
    #source ~/.venv/bin/activate
lint:
	pylint --disable=R,C *.py 