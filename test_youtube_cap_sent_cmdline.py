from youtube_cap_sent_cmdline import youtube_search
from youtube_cap_sent_cmdline import addVideoData

def test_youtube_search():
    assert len(youtube_search("Nvidia", )) != 0, "the list is non empty" 

def test_addVideoData():

    df = addVideoData()
    assert isinstance(df.loc["captionString"], str), "the returned dataframe captions is a string"

# geo_query
# combineCaptions
# capScore