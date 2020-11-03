import pandas as pd
import numpy as np
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# import boto3
# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser

# assign global varaibles that we will be used through out the code.
# We will eventaully replace the Developer Key as a command lie

DEVELOPER_KEY = "AIzaSyA6NllsCacNGQJDtgJDNdDngn5X4wsN76M"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# """
# We will utlizee the youtube_search function
# from https://pypi.org/project/youtube-search/

# This function asks for a searchCriteria and returns a class opbject that
# has basic information from the number of MAX results requested. This is
# associated with YouTube API v3, and reqires a Development-Key that has
# appriopriate permissions.
# """

def youtube_search(
    searchCritera,
    max_results=50,
    order="relevance",
    token=None,
    location=None,
    location_radius=None,
):

    # define the youtube api class
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    # pass in search critera to the actual function that saves object as
    # search responce.

    search_response = (
        youtube.search()
        .list(
            q=searchCritera,
            type="video",
            pageToken=token,
            order=order,
            part="id,snippet",
            maxResults=max_results,
            location=location,
            locationRadius=location_radius,
        )
        .execute()
    )

    # define an empty list that will be appended with relivent video info
    videos = []

    # loop through and store video IDs from videos that will be used to scrap
    # additional information and captions
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)

    # check to see if there are any more stings, and if not end function
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except StopIteration:
        nexttok = "last_page"
        return (nexttok, videos)


# """
# This function is used by taking a video ID and returing a dict of the key values
# snippet, recordingDetails, and statistics.  Within these vlaues are other dict
# that contain the informtaion we need to build our final dataset.
# """


def geo_query(video_id="5OCQoHrU2zM"):

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    video_response = (
        youtube.videos()
        .list(id=video_id, part="snippet, recordingDetails, statistics")
        .execute()
    )

    return video_response


# """
# This function it that main function that takes a vidID and passes back all
# relivent informaiton that we desire to be built into a dataframe.
# """

def addVideoData(vidID="5OCQoHrU2zM"):
    dataForVideo = geo_query(vidID)
    videoID = vidID
    datePub = datetime.strptime(dataForVideo["items"][0]["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ") 
    searchDate = np.datetime64(datetime.now())
    vidTitle = dataForVideo["items"][0]["snippet"]["title"]
    channelTitle = dataForVideo["items"][0]["snippet"]["channelTitle"]
    viewCount = dataForVideo["items"][0]["statistics"]["viewCount"]
    likeCount = dataForVideo["items"][0]["statistics"]["likeCount"]
    dislikeCount = dataForVideo["items"][0]["statistics"]["dislikeCount"]

    # check to see if the video has a caption and if not passes an empty list
    # instead of an error that stops the code
    try:
        captionStr = combineCaptions(vidID)
    except:
        captionStr = list()

    return pd.Series(
        {
            "videoID": videoID,
            "datePub": datePub,
            "searchedDate": searchDate,
            "VideoTitle": vidTitle,
            "channelTitle": channelTitle,
            "viewCount": viewCount,
            "likeCount": likeCount,
            "dislikeCount": dislikeCount,
            "captionString": captionStr,
        }
    )


# Define a function that takes a video ID and returns a string of the caption
def combineCaptions(vidID):
    videoCaptions = YouTubeTranscriptApi.get_transcript(vidID)
    capStr = ""
    for i in range(len(videoCaptions)):
        capStr += videoCaptions[i]["text"] + " "
    return capStr

# """
# The code below is used if accessing and building a dataframe over time.

# s3 = boto3.resource('s3')
# bucket = s3.Bucket('youtubelambdabucket') # Enter your bucket name, e.g 'Data'
# bucket_name = 'youtubelambdabucket'
# # key path, e.g.'customer_profile/Reddit_Historical_Data.csv'
# key = 'caption_df.csv'
# # lambda function
# # def lambda_handler(event,context):
# # download s3 csv file to lambda tmp folder
# local_file_name = 'tmpcaption_df.csv' #
# s3.Bucket(bucket_name).download_file(key,local_file_name)
# """

# """
# The next section of code will be deicated to NLP processing or captions
# in which we will compare to stock prices.
# """

def capScore(strCap):
    vader = SentimentIntensityAnalyzer()
    score = vader.polarity_scores(str(strCap))
    print(score)


def main(search="Nvidia", numVidToSearch=25):
    YouTubedf = pd.DataFrame(
        columns=[
            "videoID",
            "datePub",
            "searchedDate",
            "VideoTitle",
            "channelTitle",
            "viewCount",
            "likeCount",
            "dislikeCount",
            "captionString",
        ]
    )

    videoRef = youtube_search(search, numVidToSearch)

    for i in range(len(videoRef[1])):
        YouTubedf = YouTubedf.append(
            addVideoData(videoRef[1][i]["id"]["videoId"]), ignore_index=True
        )
        print(YouTubedf.iloc[i])
        capScore(YouTubedf.iloc[i]["captionString"])

    #print(YouTubedf)


# """
# The below code pulls and appends a csv that is stored in a AWS S3 Bucket

#     # write the data into '/tmp' folder
#     with open('tmpcaption_df.csv','r') as infile:
#         YouTubedf.to_csv("tmpcaption_df.csv", mode="a", header=False)

#     # upload file from tmp to s3 key
#     bucket.upload_file('tmpcaption_df.csv', key)
# """

if __name__ == "__main__":
    import sys
    val = str(sys.argv[1])
    val2 = int(sys.argv[2])
    print(sys.argv)
    main(val, val2)