import os

# URLs
URL_EVENTLIST='http://ufcstats.com/statistics/events/completed?page=all'

# Crawler
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}

# Mongo DB
MONGO_DB_URL=os.getenv('KEY_THAT_MIGHT_EXIST', 'default_value')