import time
import datetime
from slackbot_settings import *
from slackclient import SlackClient
import threading
import tweepy

slack_token = API_TOKEN
sc = SlackClient(slack_token)
def pitchtweets():
        tweet_id_int = 1 
        while True:
            # Pull the latest tweet from @NationalsUmp
            hour_ago = datetime.datetime.utcnow() + datetime.timedelta(hours = -1) 
            timeline = api.user_timeline(id="@NationalsUmp", count=1)
            tweet_full = timeline[0]
            tweet_full_time = tweet_full.created_at
            tweet_full_int = int(tweet_full.id)
            if tweet_full_int <= tweet_id_int:
                time.sleep(10)
            elif tweet_full_time < hour_ago:
                time.sleep(10)
            else:
                slack_message = tweet_full.text
                print tweet_full.id
                print tweet_id_int
                print slack_message
                sc.api_call("chat.postMessage", channel="#baseball", text=slack_message)
                tweet_id_int = int(tweet_full.id)
                time.sleep(10)

thread_test = threading.Thread(target=pitchtweets)
thread_test.start()
print "Doing stuff"
sleep(30)
print "done"
