![Python application test with Github Actions](https://github.com/Cloblak/youtube_sentiment_stock_prediction/workflows/Python%20application%20test%20with%20Github%20Actions/badge.svg)

# Youtube Caption Sentiment (Pending: Stock Prediciton)

Youtube_Sentiment_Stock_Prediction is a Python package that we hope will be a 
robust way to begin building and understanding the effects youtube creators 
can have on stock prices.  There are many examples of influencers on youtube
that create content and either move stock prices themselfs, or at least provide
a window from exterpt eyes on the way a product or service may effect a stock
price.  This pyhton script hopes to investigate those precived trends and 
highlight effects of content on youtube against a targeted stock. 

#### Acknowledgement

The major package used to pull the captions themselves was the 
youtube_transcript_api package.  You can find details on it at the below link.

https://github.com/jdepoix/youtube-transcript-api

## Installation (Coming Soon)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
Youtube_Sentiment_Stock_Prediction.

```bash
pip install ***
```

## Usage (Coming Soon)

#### youtube_sentiment_stock_prediction.py 

Use of this python code allows you to see results from a simple cmd line tool.

```cmd line
$ python youtube_sentiment_stock_prediction "APPLE Stock" 5       
        # APPLE = Desired youtube search or ticker symbol 
        # 25 = Number of top search results to aggrigate sentiment score from

# OUTPUT EXAMPLE
['youtube_sentiment_stock_prediction.py', 'APPL', '5']
videoID                                                KR0g-1hnQPA
datePub                                        2020-10-13 18:15:12
searchedDate                            2020-11-04 14:45:14.106028
VideoTitle                                Apple Event — October 13
channelTitle                                                 Apple
viewCount                                                 54349586
likeCount                                                   925541
dislikeCount                                                 54425
captionString    ["Good Day for Dreaming"\nby Ruelle playing] H...
Name: 0, dtype: object
{'neg': 0.013, 'neu': 0.802, 'pos': 0.185, 'compound': 1.0}
```

#### stock_pred_model.py

The stock_pred_model.py code will take the (current) caption data that the lambda 
fuction builds that then plot that with the associated Stock data.  In this case
the data and code has been written for Nvidia Youtube Searches and Stock 
comparisons (see below image for exmple of plot, and this codes potential usefulness)


![Alt text](10_plots/NVDA_Sentiment_Stock_ComparisonPlot.jpeg?raw=true "Title")

## Author
Christopher Oblak (linkedin: www.linkedin.com/in/christopheroblak/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
