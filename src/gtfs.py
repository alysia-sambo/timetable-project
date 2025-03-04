import time
from datetime import UTC, datetime
from google.transit import gtfs_realtime_pb2
import pytz
import requests
import os
from dotenv import load_dotenv

# This should be customisable in future
target_stops = ['10700', '317574', '1133']
number_upcoming_trips = 4

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

def GetDepartingTrips(stop_ids, url):
    feed = GetRealTimeFeed(url)
    next_trips = {stop_id: [] for stop_id in stop_ids}

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            if trip_update.HasField('trip') and trip_update.trip.HasField('route_id'):
                route_id = trip_update.trip.route_id
                for stop_time_update in trip_update.stop_time_update:
                    if stop_time_update.HasField('stop_id') and stop_time_update.stop_id in stop_ids:
                        stop_id = stop_time_update.stop_id
                        departure_time = stop_time_update.departure.time

                        if departure_time >=  time.time():
                            departure_time_dt = datetime.fromtimestamp(departure_time, UTC)
                            departure_time_brisbane = departure_time_dt.astimezone(pytz.timezone("Australia/Brisbane"))

                            next_trips[stop_id].append((departure_time_brisbane, route_id))

    for stop_id, trips in next_trips.items():
        trips.sort()

    return next_trips

next_trips = GetDepartingTrips(target_stops, gtfs_url)
