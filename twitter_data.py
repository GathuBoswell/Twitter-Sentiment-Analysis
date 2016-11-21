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
        with open(self._json_file, 'w') as file:
            for status in all_tweets:
                # status._json converts tweepy status object to JSON serializable response data
                json.dump(status._json, file, sort_keys=True, indent=4)
        return self._json_file

def main():
    cons_key = "qrRMCNNtOtWlN7YPAwllY4C9p"
    cons_secret = "WuA5sp6Do0Q3ohcyTztBjeF0Z8fRQaNFxJQzD0HAWXJpGEA46K"
    access_key = "765074739228471296-eQswENirBvmzVSI3LNSf7p7E3r4L32d"
    access_secret = "t2SuOHDGxO8T5EzaEcoM17mu6ug65F9TGdeo8L8NnT46a"
    data = GetData(cons_key, cons_secret, access_key, access_secret)
    tweets = data.get_tweets('@Boswellwanyoike')
    print(tweets)

if __name__ == '__main__':main()



