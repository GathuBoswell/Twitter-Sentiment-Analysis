import unittest

import twitter_data


class TwitterDataTestCase(unittest.TestCase):
    def test_twiter_data_instance(self):
        tweets = twitter_data.GetData()
        self.assertEqual(type(tweets), type(twitter_data.GetData()))


if __name__ == '__main__':
    unittest.main()
