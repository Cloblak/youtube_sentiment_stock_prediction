install:
	pip install --upgrade pip &&\
		pip install -r "requirements.txt"

test:
	python -m pytest -vv "test_youtube_cap_sent_cmdline.py"

lint:
	pylint --disable=R,E1101,W0702,C youtube_cap_sent_cmdline.py
	
format:
	black youtube_cap_sent_cmdline.py test_youtube_cap_sent_cmdline.py

all: install lint test
