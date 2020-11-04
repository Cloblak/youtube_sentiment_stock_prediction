install:
	pip install --upgrade pip &&\
		pip install -r "requirements.txt"

test:
	python -m pytest -vv "test_youtube_sentiment_stock_prediction.py"

lint:
	pylint --disable=R,E1101,W0702,C youtube_sentiment_stock_prediction.py
	
format:
	black youtube_sentiment_stock_prediction.py test_youtube_sentiment_stock_prediction.py

all: install lint test
