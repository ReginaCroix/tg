import tweepy
import time
import random
import os

#키랑 토큰 정의
TWITTER_CONSUMER_KEY = os.environ.get(TWITTER_CONSUMER_KEY)
TWITTER_CONSUMER_SECRET = os.environ.get(TWITTER_CONSUMER_SECRET)
TWITTER_ACCESS_TOKEN_KEY = os.environ.get(TWITTER_ACCESS_TOKEN_KEY)
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get(TWITTER_ACCESS_TOKEN_SECRET)

#인증
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#랜덤으로 목록 파일에서 출력 텍스트 뽑는 함수
with open('music_list.txt', 'rt', encoding='UTF8') as f:
    randomMusic = random.choice(list(f.readlines())).splitlines()[0]

with open('cake_list.txt', 'rt', encoding='UTF8') as f:
    randomCake = random.choice(list(f.readlines())).splitlines()[0]

#마지막으로 확인했던 ID 확인하고 업데이트하기
FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

#찾아낸 트윗에 답변하기
def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    #DevNote: use 1136576972723593216 for testing
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#케이크' in mention.full_text():
            print('Found #케이크', flush=True)
            print('responding back', flush=True)
            api.update_status('@'+ mention.user.screen_name + randomCake, mention.id)
        elif '#음악연습' in mention.full_text():
            print('Found #음악연습', flush=True)
            print('responding back', flush=True)
            api.update_status('@'+ mention.user.screen_name + randomMusic, mention.id)

while True:
    reply_to_tweets()
    time.sleep(3)
