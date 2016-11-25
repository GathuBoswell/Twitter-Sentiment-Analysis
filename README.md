# Twitter-Sentiment-Analysis

## Introduction
*  **`Twitter Sentiment Analyser`** is a Python command line app that analyses tweets to check for sentiments and emotions.
*  It has the following features;
  *  Fetch tweets
  *  Analyze frequency of words used in the tweets
  *  Saves the tweets fetched into a json file for further analysis
  *  Integrates with Alchemy API to get;
    *  Doc Sentiment of the collected tweets, with results being either, 
      * Positive
      * Negative
    *  Emotional Sentiments from the collected, which is further analysed to;
      *  Disgust
      *  Anger
      *  Fear
      *  Joy
      *  Sadness
      
## Dependencies

### Libraries used
*  This app's functionality depends on multiple Python packages including;
  *  **[ascii-graph](https://www.djangoproject.com/)** - This package handles console graphs, representing data in a visual manner, it also adds rendering with color
  *  **[docopt](http://www.django-rest-framework.org/)** - This is a powerful commandline library that lets a user enter commands and any number of parameters.
  *  **[tweepy](https://github.com/omab/python-social-auth)** - This package handles integration to the twitter API, letting a user fetch tweets among other functions.
  *  **[watson-developer-cloud](https://pillow.readthedocs.org/en/3.1.x/)** - This package handles integration with the Alchemy API
  *  **[prettytable](https://pypi.python.org/pypi/ipdb)** - This package helps in rendering data in a tabular form
  *  **[nltk](https://github.com/kennethreitz/autoenv)** - This package provides a list of all stop words which are used to remove all stop words in the collected tweets

## Installation and setup
*  Navigate to a directory of choice on `terminal`.
*  Clone this repository on that directory.
  *  Using SSH;

    >`git clone git@github.com:GathuBoswell/bc-12-Twitter-Sentiment-Analysis.git`

  *  Using HTTP;

    >`git clone https://github.com/GathuBoswell/bc-12-Twitter-Sentiment-Analysis`

*  Navigate to the repo's folder on your computer
  *  `cd Twitter-Sentiment-Analysis/`
*  Install the app's package dependencies. For best results, using a [virtual environment](http://virtualenv.readthedocs.org/en/latest/installation.html) is recommended.
  *  `pip install -r requirements`
*  Setup Your API Aunthentication Keys for Both Alchemy and Twitter API
  *  `python api_setup.py`
  *  Running the command above will produce output that's similar to the sample below.
  ```
    Enter the Alchemy Api Key: XXXXXXXXXXXXXXXXXXXXXXXXXXXX
    Enter the tWitter consumer key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    Enter the tWitter consumer Secret: XXXXXXXXXXXXXXXXXXXXXXXXXXX
    Enter the tWitter access key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    Enter the tWitter access Secret: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  ```
* Run the app
  *  `python twitter_cmd.py`
  *  Running the command above will produce output that's similar to the sample below.