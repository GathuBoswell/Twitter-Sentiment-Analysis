class GetData(object):
    def __init__(self):
        import json as json
        from termcolor import colored as c
        self.color = c
        self.json = json
        self._json_data_available = False #check if saved file has data
        self._json_file = 'all_tweets.json'
        self.api_file = 'api_key.json'

    def setup(self):
        try:
            with open(self.api_file, 'r') as api_file:
                api_keys = self.json.load(api_file)
            self.__alchemy_key = api_keys[0]['alchemy']['key']
            self.__cons_key = api_keys[0]['twitter']['cons_key']
            self.__cons_secret = api_keys[0]['twitter']['cons_secret']
            self.__access_key = api_keys[0]['twitter']['access_key']
            self.__access_secret = api_keys[0]['twitter']['access_secret']
        except IOError:
            print('The file containing the API keys cannot be found,'
                  'Please run: python api_setup.py to set that data')

    def get_tweets(self, twitter_username, duration=7):
        import datetime
        import tweepy
        import tqdm as pbar
        import requests

        auth = tweepy.OAuthHandler(self.__cons_key, self.__cons_secret)
        auth.set_access_token(self.__access_key, self.__access_secret)
        api = tweepy.API(auth)
        all_tweets = []
        try:
            new_tweets = (api.user_timeline(screen_name=twitter_username,
                                            count=20))
            all_tweets.extend(new_tweets)
            if len(all_tweets) > 0:
                oldest_id = new_tweets[-1].id - 1
                for i in pbar.tqdm(range(5)):
                    new_tweets = (api.user_timeline(screen_name=twitter_username,
                                                        count=20, max_id=oldest_id))
                    oldest_id = all_tweets[-1].id - 1
                    all_tweets.extend(new_tweets)

                earliest_tweet_date = (all_tweets[0].created_at).date()
                tweet_max_date = earliest_tweet_date + datetime.timedelta(days=duration)
                status_list = []
                for tweet in all_tweets:
                    if (tweet.created_at).date() <= tweet_max_date:
                        status_list.append(tweet._json)

                    with open(self._json_file, 'w') as json_data:
                        self.json.dump(status_list, json_data, indent=4)
            else:
                print(self.color('No tweets available for the entered duration', 'red'))
        except tweepy.TweepError as e:
            if e.reason.startswith('Failed to send request'):
                print(self.color('Internet connection required, please connect and try again', 'red'))
            elif e.reason == 'Not authorized.':
                print('You are not authorized to view this person tweets!, (protected tweets)')
            elif e.args[0][0]['code'] == 34:
                print(self.color('Invalid twitter username, try again with a valid username', 'red'))
            else:
                print(self.color('Unknown Error', 'red'))
        return ''

    def check_json_file(self):
        try:
            try:
                with open(self._json_file, 'r') as tweet_data:
                    data = self.json.load(tweet_data)
                if len(data[0]) > 1:
                    self._json_data_available = True
                else:
                    self._json_data_available = False
            except ValueError:
                self._json_data_available = False
        except IOError:
            self._json_data_available = False


    def word_list(self):
        import json
        import re
        from stop_words import get_stop_words

        cachedStopWords = get_stop_words('english')
        cachedStopWords.append(')')
        cachedStopWords.append('-')
        cachedStopWords.append(',')
        tweet_list = []
        with open(self._json_file, 'r') as tweet_data:
            data = json.load(tweet_data)
        tweet_list.extend(data)
        unwanted_texts = re.compile('[@#-&()..."]')
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
        #self.words = self.word_list()
        for word in self.words:
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
        from prettytable import PrettyTable

        self.check_json_file()
        if self._json_data_available:
            word_count = self.word_frequency()
            sort = word_count.items()
            sorted_list =(sorted(sort, key=itemgetter(1)))
            count_sum = sum(word_count.values())
            count = -1
            tweet_table = PrettyTable(['Word', 'Count', 'Percent'])
            while count > -20:
                word, value = sorted_list[count]
                percent = (value/count_sum)*100
                percent1 = ('{:.2f}'.format(percent))
                tweet_table.add_row([word, value, percent1])
                count += -1
            print(self.color(tweet_table, 'cyan'))
        else:
            print('No tweets available yet, start by fetching for tweets first')
        return ' '

    def sentiment_analysis(self, all=True, sentiment=False, emotion=False):
        from watson_developer_cloud import AlchemyLanguageV1
        alchemyapi = AlchemyLanguageV1(api_key=self.__alchemy_key)

        self.check_json_file()
        if self._json_data_available:
            words_list = ' '.join(self.word_list())
            self.__tweets_sentiment = alchemyapi.sentiment(text=words_list)
            self.__tweets_emotion = alchemyapi.emotion(text=words_list)
            if all:
                return (self.sentiment_table(), self.emotion_graph())
            if sentiment:
                return self.sentiment_table()
            if emotion:
                return self.emotion_graph()
        else:
            print(self.color('No tweets available yet, start by fetching for tweets first', 'red'))
        return ' '

    def emotion_graph(self):
        from ascii_graph import Pyasciigraph
        import ascii_graph.colors as c
        from ascii_graph.colordata import vcolor

        col_pattern = [c.Gre, c.Yel, c.Cya, c.Red, c.Pur]
        data = [(str(emotion).capitalize(), float(value)*100) for emotion,
                                value in self.__tweets_emotion['docEmotions'].items()]
        total_emotion_value = vcolor(data, col_pattern)
        graph = Pyasciigraph()
        for line in graph.graph('Emotions Graph', total_emotion_value):
            print('         ', line)
        return

    def sentiment_table(self):
        from prettytable import PrettyTable

        sent_dict = self.__tweets_sentiment['docSentiment']
        sentiment_data = PrettyTable(['Sentiment Type', 'Score', 'if_mixed'])
        sentiment_data.add_row([sent_dict['type'], sent_dict['score'], sent_dict['mixed']])
        print('\n')
        print(self.color(sentiment_data, 'green'))
        return

def main():
    setup_getdata = GetData
    setup_getdata.setup()

if __name__ == '__main__':main()