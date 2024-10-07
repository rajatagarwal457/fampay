import os
import requests
from datetime import datetime, timedelta
from api.models import Video
from database.db import db
from flask_apscheduler import APScheduler
import time

API_KEYS = str(os.environ.get('YOUTUBE_API_KEYS')).split(",")

iterator = iter(API_KEYS)
API_KEY = next(iterator)

YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'

scheduler = APScheduler() # to handle the async part of the code. cannot use asyncio as app context is a pain to pass

def fetch_videos(app, search_term):
    global API_KEY
    with app.app_context():
        url = f'{YOUTUBE_API_BASE_URL}/search'
        params = {
            'part': 'snippet',
            'q': search_term,
            'type': 'video',
            'order': 'date',
            'maxResults': 50,
            'key': API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            videos_to_add = []
            for item in data['items']:
                if item['snippet']['description'] == "": #90% of shorts have an empty desc so filter that out
                    continue
                video_data = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                    'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle']
                }
                
                existing_video = Video.query.filter_by(id=video_data['id']).first()
                if existing_video:
                    existing_video.title = video_data['title']
                    existing_video.description = video_data['description']
                    existing_video.published_at = video_data['published_at']
                    existing_video.thumbnail_url = video_data['thumbnail_url']
                    existing_video.channel_id = video_data['channel_id']
                    existing_video.channel_title = video_data['channel_title']
                    videos_to_add.append(existing_video)
                else:
                    videos_to_add.append(Video(**video_data))

            db.session.add_all(videos_to_add)
            db.session.commit()
            
            print(f"Fetched and saved {len(data['items'])} videos")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching videos: {e}")
            API_KEY = next(iterator, 'NO MORE KEYS!!!')

        except Exception as e:
            API_KEY = next(iterator, 'NO MORE KEYS!!!')
            print(f"An unexpected error occurred: {e}")

def fetch_videos_periodically(app, search_term):
    if scheduler.running:
        scheduler.shutdown(wait=False)
    scheduler.init_app(app)
    with app.app_context():
        Video.query.delete() #clear db of old terms
        db.session.commit()
    scheduler.add_job(id='fetch_videos', func=fetch_videos, args=[app, search_term], trigger='interval', seconds=10)
    scheduler.start()