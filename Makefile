install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_youtube_cap_sent_cmdline.py

lint:
	pylint --disable=R,E1101,C youtube_cap_sent_cmdline.py

all: install lint test