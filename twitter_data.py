class GetData(object):
    def __init__(self, cons_key, cons_secret, access_key, access_secret):
        self.__cons_key = cons_key
        self.__cons_secret = cons_secret
        self.__access_key = access_key
        self.__access_secret = access_secret
        self._json_file = 'all_tweets.json'

    def get_tweets(self, twitter_username, duration=7):
        import datetime
        import tweepy
        import json
        import tqdm as pbar

        auth = tweepy.OAuthHandler(self.__cons_key, self.__cons_secret)
        auth.set_access_token(self.__access_key, self.__access_secret)
        api = tweepy.API(auth)
        all_tweets = []

        new_tweets = (api.user_timeline(screen_name=twitter_username,
                                            count=1))
        oldest_id = new_tweets[-1].id - 1
        for i in pbar.tqdm(range(5)):
            all_tweets.extend(api.user_timeline(screen_name=twitter_username,
                                       count=20, max_id=oldest_id))
            oldest_id = all_tweets[-1].id - 1


        earliest_tweet_date = (all_tweets[0].created_at).date()
        tweet_max_date = earliest_tweet_date + datetime.timedelta(days=duration)
        status_list = []
        for tweet in all_tweets:
            if(tweet.created_at).date() <= tweet_max_date:
                status_list.append(tweet._json)

            with open(self._json_file, 'w') as json_data:
                json.dump(status_list, json_data)

        return ''

    def word_list(self):
        import json
        import re
        from nltk.corpus import stopwords

        cachedStopWords = stopwords.words("english")
        tweet_list = []
        with open(self._json_file, 'r') as tweet_data:
            data = json.load(tweet_data)
        tweet_list.extend(data)
        # print(len(tweet_list))
        # pprint(tweet_list)
        unwanted_texts = re.compile('[@#-&()."]')
        words = []
        for status in tweet_list:
            for word in status['text'].split():
                if unwanted_texts.match(word) or word.startswith('http')\
                    or word.startswith('http'):
                    continue
                else:
                    for word_members in (word.replace(':',' ').replace('.',' '
                                        ).replace('!',' ').replace('?',' '
                                        ).replace('"', ' ').replace('-',' '
                                        ).replace('/',' ').split()
                                        ):
                        if (word_members not in cachedStopWords) and\
                            (word_members != 'RT'):
                            words.append(str(word_members))
        return words

    def word_frequency(self):
        word_count = {}
        words = self.word_list()
        for word in words:
            try:
                word = int(word)
                try:
                    if word_count[word]:
                        word_count[word] += 1
                except KeyError:
                    word_count[word] = 1
            except ValueError:
                try:
                    if word_count[word]:
                        word_count[word] += 1
                except KeyError:
                    word_count[word] = 1
        return word_count

    def word_count_analysis(self):
        from operator import itemgetter

        word_count = self.word_frequency()
        sort = word_count.items()
        sorted_list =(sorted(sort, key=itemgetter(1)))
        count_sum = sum(word_count.values())
        count = -1
        while count > -20:
            word, value = sorted_list[count]
            percent = (value/count_sum)*100
            print(word, 'appears ', value, 'times and'
                 ' percentage is {:.2f}'.format(percent))
            count += -1

    def sentiment_analysis(self, all=True, sentiment=False, emotion=False):
        from watson_developer_cloud import AlchemyLanguageV1
        alchemyapi = AlchemyLanguageV1(api_key='0e1c5001c8047a3f0492469bf8449d40949f5d1f')

        words_list = ' '.join(self.word_list())

        tweets_sentiment = alchemyapi.sentiment(text=words_list)
        self.__tweets_emotion = alchemyapi.emotion(text=words_list)
        return (tweets_sentiment['docSentiment'], self.__tweets_emotion['docEmotions'])

    def emotion_graph(self):
        from ascii_graph import Pyasciigraph
        import ascii_graph.colors as cols

        total_emotion_value = [(str(emotion).capitalize(), float(value)*100) for emotion,
                                value in self.__tweets_emotion['docEmotions'].items()]
        colors = [cols.Pur, cols.Red, cols.Gre, cols.Cya]
        for item in total_emotion_value:
            for i in range(len(total_emotion_value)):
                item.add(colors[i])
        graph = Pyasciigraph()
        for line in graph.graph('Emotions Graph', total_emotion_value):
            print(line)

def main():
    from pprint import pprint
    cons_key = "qrRMCNNtOtWlN7YPAwllY4C9p"
    cons_secret = "WuA5sp6Do0Q3ohcyTztBjeF0Z8fRQaNFxJQzD0HAWXJpGEA46K"
    access_key = "765074739228471296-eQswENirBvmzVSI3LNSf7p7E3r4L32d"
    access_secret = "t2SuOHDGxO8T5EzaEcoM17mu6ug65F9TGdeo8L8NnT46a"
    data = GetData(cons_key, cons_secret, access_key, access_secret)
    #tweets = data.get_tweets('@realdonaldTrump')
    # data.word_count_analysis()
    for item in data.sentiment_analysis():
        pprint(item)

if __name__ == '__main__':main()



