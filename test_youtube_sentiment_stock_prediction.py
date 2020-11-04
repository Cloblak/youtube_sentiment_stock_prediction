from youtube_sentiment_stock_prediction import youtube_search
from youtube_sentiment_stock_prediction import addVideoData
from youtube_sentiment_stock_prediction import geo_query


def test_youtube_search():
    assert (
        len(
            youtube_search(
                "Nvidia",
            )
        )
        != 0
    ), "the list is non empty"


def test_addVideoData():

    df = addVideoData()
    assert isinstance(
        df.loc["captionString"], str
    ), "the returned dataframe captions is a string"


def test_geo_query():
    df = geo_query()
    assert len(df) != 0, "the list is non empty"


# combineCaptions
# capScore
