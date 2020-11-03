install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_youtube_cap_sent_cmdline.py

lint:
	pylint --disable=R,C youtube_cap_sent_cmdline.py

all: install lint test