from google.transit import gtfs_realtime_pb2
import requests
import os
from dotenv import load_dotenv

load_dotenv()

gtfs_url = os.getenv("REALTIME_URL")

def GetRealTimeFeed(url):
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(url)
        feed.ParseFromString(response.content)
    except Exception as e:
         print (f"Could not connect to real time feed: {e}")
    return feed

gtfs_feed = GetRealTimeFeed(gtfs_url)
