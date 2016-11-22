class GetData(object):
    def __init__(self, cons_key, cons_secret, access_key, access_secret):
        self.__cons_key = cons_key
        self.__cons_secret = cons_secret
        self.__access_key = access_key
        self.__access_secret = access_secret
        self._json_file = 'all_tweets.json'

    def get_tweets(self, twitter_username):
        import tweepy
        import json
        # authorize twitter
        auth = tweepy.OAuthHandler(self.__cons_key, self.__cons_secret)
        auth.set_access_token(self.__access_key, self.__access_secret)
        api = tweepy.API(auth)
        # list to hold all the tweets generated
        all_tweets = []
        # get all recent tweets with a max of 200 tweets per page
        new_tweets = api.user_timeline(screen_name=twitter_username, count=200)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=twitter_username, count=200, max_id=oldest)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            ### implement the status bar
        status_list = []
        with open(self._json_file, 'w') as json_data:
            for status in all_tweets:
                status_list.append(status._json)
                # status._json converts tweepy status object to JSON serializable response data
                #json.dump(status._json, json_data, sort_keys=True, indent=4)
            json.dump(status_list, json_data)
        return ''

    def word_list(self):
        import json
        import re

        tweet_list = []
        with open(self._json_file, 'r') as tweet_data:
            data = json.load(tweet_data)
        tweet_list.extend(data)
        # print(len(tweet_list))
        # pprint(tweet_list)
        unwanted_texts = re.compile('[@#."]')
        words = []
        for status in tweet_list:
            for word in status['text'].split():
                # create a regex to catch this class ['@#."']
                #if word.startswith('#') or word.startswith('@') or word.startswith('http'):
                if unwanted_texts.match(word) or word.startswith('http'):
                    continue
                else:
                    for word_members in (word.replace(':',' ').replace('.',' '
                                        ).replace('!',' ').replace('?',' '
                                        ).replace('"', ' '
                                        ).replace('/',' ').split()
                                        ) or word.startswith('http'):
                    # word_members = re.findall(r"[\w]+", word)
                    # words.extend(word_members)
                        words.append(word_members)
        print(words)

        def word_count(self):
            pass

def main():
    cons_key = "qrRMCNNtOtWlN7YPAwllY4C9p"
    cons_secret = "WuA5sp6Do0Q3ohcyTztBjeF0Z8fRQaNFxJQzD0HAWXJpGEA46K"
    access_key = "765074739228471296-eQswENirBvmzVSI3LNSf7p7E3r4L32d"
    access_secret = "t2SuOHDGxO8T5EzaEcoM17mu6ug65F9TGdeo8L8NnT46a"
    data = GetData(cons_key, cons_secret, access_key, access_secret)
    #tweets = data.get_tweets('@allelachavo')
    print(data.word_frequency())

if __name__ == '__main__':main()



