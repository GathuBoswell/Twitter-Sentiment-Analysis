import unittest

import twitter_data


class TwitterDataTestCase(unittest.TestCase):
    def test_twiter_data_instance(self):
        tweets = twitter_data.GetData()
        self.assertEqual(type(tweets), type(twitter_data.GetData()))
    def test_twitter_data_word_frequency(self):
        tweets = twitter_data.GetData()
        tweets.words = ['this is and this is the way and the right way ']
        frequency = tweets.word_frequency()
        result = {'this':2, 'is':2, 'and':2, 'the':2, 'way':2, 'right':1}
        self.assertEqual(result, frequency)

if __name__ == '__main__':
    unittest.main()
