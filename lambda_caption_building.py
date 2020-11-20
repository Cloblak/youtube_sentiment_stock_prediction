import numpy as np
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import boto3
from datetime import datetime
from googleapiclient.discovery import build
from oauth2client.tools import argparser


DEVELOPER_KEY = "XXXXXXXX"  # Change to you Development Key Here
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
s3 = boto3.resource("s3")
bucket = s3.Bucket("youtubelambdabucket")  # Change to yout S3 bucketname

# """
# Handler Function that called key functions that pull in a csv from S3 to
# update with the next set of youtube captions scraped from the top 25
# videos
# """


def lambda_handler(event, context):

    bucket_name = "youtubelambdabucket"  # Change to your bucketname
    key = "caption_df.csv"  # Change to the file name you wish to save
    local_file_name = "/tmp/tmpcaption_df.csv"  # local file name
    s3.Bucket(bucket_name).download_file(key, local_file_name)

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

    # Change your search critera and # of videos to process
    videoRef = youtube_search("Nvidia Stock", 25)

    for i in range(len(videoRef[1])):
        YouTubedf = YouTubedf.append(
            addVideoData(videoRef[1][i]["id"]["videoId"]), ignore_index=True
        )

    YouTubedf.to_csv("/tmp/tmpcaption_df.csv", mode="a", header=False)

    # upload file from tmp to s3 key
    bucket.upload_file("/tmp/tmpcaption_df.csv", key)


# """
# We will utlizee the youtube_search function
# from https://pypi.org/project/youtube-search/

# This function asks for a searchCriteria and returns a class opbject that
# has basic information from the number of MAX results requested. This is
# associated with YouTube API v3, and reqires a Development-Key that has
# appriopriate permissions.
# """


def youtube_search(
    q,
    max_results=50,
    order="relevance",
    token=None,
    location=None,
    location_radius=None,
):

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    search_response = (
        youtube.search()
        .list(
            q=q,
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

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except Exception as e:
        nexttok = "last_page"
        return (nexttok, videos)


# """
# This function is used by taking a video ID and returing a dict of the key values
# snippet, recordingDetails, and statistics.  Within these vlaues are other dict
# that contain the informtaion we need to build our final dataset.
# """


def geo_query(video_id):
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
# This function it the main function that takes a vidID and passes back all
# relivent informaiton that we desire to be built into a dataframe.
# """


def addVideoData(vidID):
    dataForVideo = geo_query(vidID)
    videoID = vidID
    datePub = dataForVideo["items"][0]["snippet"]["publishedAt"]
    searchDate = str(datetime.now())
    vidTitle = dataForVideo["items"][0]["snippet"]["title"]
    channelTitle = dataForVideo["items"][0]["snippet"]["channelTitle"]
    viewCount = dataForVideo["items"][0]["statistics"]["viewCount"]
    likeCount = dataForVideo["items"][0]["statistics"]["likeCount"]
    dislikeCount = dataForVideo["items"][0]["statistics"]["dislikeCount"]
    # videoDesc = dataForVideo['items'][0]['snippet']['description']
    try:
        captionStr = combineCaptions(vidID)
    except:
        captionStr = list()
        pass

    return pd.Series(
        {
            "videoID": vidID,
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
