from cmd import Cmd

class TweetAnalyserCmd(Cmd):
    def __init__(self, args):
        super().__init__()
        self.prompt = 'Tweet_Sentiment: >'

    def help_introduction(self):
        print('List of commands')

    def do_fetch(self):
        pass

    def do_tojson(self):
        pass

    def do_wordcount(self):
        pass

    def do_sentiment(self):
        pass

    def do_quit(self):
        pass

if __name__ == '__main__':
    prompt = TweetAnalyserCmd('')
    prompt.cmdloop('Starting Tweet Sentiment Analyser')
