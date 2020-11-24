import pandas as pd
import boto3
import botocore
from datetime import datetime
import matplotlib.pylab as plt
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# create a new data frame that excludes the rows without captions

# print a smaple of the new df to ensure we have what we desire
# stripcaptions_df.sample(10)


def sent_score(capstring):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(capstring)
    return score


def video_title_model_plot(df):
    # initalize ntlk vade sentiment analyzer
    vader = SentimentIntensityAnalyzer()

    # define and manipulate the caption_df that is saved on AWS S3 Bucket
    title_only_df = df[["VideoTitle", "searchedDate"]]
    title_only_df = title_only_df.copy()
    title_only_df["VideoTitle"] = title_only_df["VideoTitle"].astype("string")
    title_only_df["searchedDate"] = title_only_df["searchedDate"].astype("datetime64")

    # score each title video and then group by date and mean the scores
    scores = title_only_df["VideoTitle"].apply(vader.polarity_scores).tolist()
    scores_df = pd.DataFrame(scores)
    title_score_df = title_only_df.join(scores_df, rsuffix="right")
    title_score_df = title_score_df[["searchedDate", "neg", "neu", "pos", "compound"]]
    mean_scores = title_score_df.groupby(
        by=title_score_df["searchedDate"].dt.date
    ).mean()
    index_mean_scores = mean_scores.reset_index()

    # Get the data for the stock Apple by specifying the stock ticker, start date, and end date
    ticker_df = yf.download(
        "NVDA",
        period="ytd",
        start=index_mean_scores["searchedDate"].min(),
        end=index_mean_scores["searchedDate"].max(),
    )

    full_joined_df = mean_scores.join(ticker_df, how="left")
    full_joined_df = full_joined_df.fillna(method="ffill")
    full_joined_df = full_joined_df.reset_index()

    # create figure and axis objects with subplots()
    fig, ax = plt.subplots()
    # make a plot
    ax.plot(full_joined_df.searchedDate, full_joined_df.Open, color="red", marker="o")
    # set x-axis label
    ax.set_xlabel("Date", fontsize=14)
    plt.xticks(rotation=45)
    # set y-axis label
    ax.set_ylabel("NVDA Stock Closing Price", color="red", fontsize=14)
    # twin object for two different y-axis on the sample plot
    ax2 = ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(
        full_joined_df.searchedDate, full_joined_df.compound, color="blue", marker="o"
    )
    ax2.set_ylabel("Video Title Compound Sentiment Score", color="blue", fontsize=14)
    plt.show()
    # save the plot as a file
    fig.savefig("TEST2.jpeg", format="jpeg", dpi=100, bbox_inches="tight")

    s3 = boto3.resource("s3")
    bucket_plot = s3.Bucket("youtubelambdabucket")
    # bucket.put_object(Body='/tmp/TEST.jpeg', ContentType='image/jpeg', Key="New_Polt.jpeg")
    bucket_plot.upload_file("TEST2.jpeg", "New_Polt_v3.jpeg")


def main():
    # Import recent csv from S# bucket to conduct sentiment analysis on
    BUCKET_NAME = "youtubelambdabucket"  # replace with your bucket name
    KEY = "caption_df.csv"  # replace with your object key
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET_NAME).download_file(KEY, "caption_df_current.csv")
    caption_df = pd.read_csv("caption_df_current.csv")

    # drop the unnecessary columns
    caption_df.drop(columns=["Unnamed: 0"])

    # stripcaptions_df = caption_df[caption_df["captionString"] != "[]"]

    video_title_model_plot(caption_df)


if __name__ == "__main__":
    main()
