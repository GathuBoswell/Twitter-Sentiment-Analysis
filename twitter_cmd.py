#!/usr/bin/env python
"""
Interactive Interface for the Twitter Sentiment Analysis App

Usage:
    my_program fetch <username> <duration>
    my_program wordfrequency
    my_program savejson <filename>
    my_program sentiment [--all] [--docsentiment] [--emotion]
    my_program (-i | --interactive)
    my_program (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --all
    --docsentiment
    --emotion
"""

import sys
import cmd
from colorama import init
from termcolor import cprint
from termcolor import colored
from pyfiglet import figlet_format
from docopt import docopt, DocoptExit

from twitter_data import GetData

cmd_render = GetData()
cmd_render.setup()

def app_intro():
    init(strip=not sys.stdout.isatty())  # # strip colors if stdout is redirected
    cprint(figlet_format('Twitter Sentiment Analyzer', font='big'), 'red')
    print(colored('					The list of commands available are as below', 'cyan'))
    print(colored('					===========================================', 'cyan'))
    print('\n')
    print(colored('						commands									Description', 'cyan'))
    print(colored('					   -----------------								    -------------------', 'cyan'))
    print(colored('				fetch <twitter_handle> <number_of_days_to_get_tweets_from>		Get all tweets of the entered username', 'cyan'))
    print(colored('				wordfrequency								Prints word count for all words in the tweets', 'cyan'))
    print(colored('				sentiment <--all> <--docsentiment> <--emotion> 				Prints sentiment analysis with specified option', 'cyan'))
    print(colored('				help									prints the docopt menu of commands', 'cyan'))
    print(colored('				home									prints this menu', 'cyan'))
    return ''

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AnalyzerCmd (cmd.Cmd):
    intro = '''                 Twitter Sentiment Analysis\n
               Type help to view list of commands\n'''
    prompt = 'Twitter_Sentiment:> '
    file = None

    @docopt_cmd
    def do_fetch(self, args):
        """Usage: fetch <username> <duration>"""
        cmd_render.get_tweets(args['<username>'], int(args['<duration>']))

    @docopt_cmd
    def do_sentiment(self, args):
        """Usage: sentiment [--all] [--docsentiment] [--emotion] """
        print(cmd_render.sentiment_analysis(args['--all'], args['--docsentiment'], args['--emotion']))

    @docopt_cmd
    def do_savejson(self, args):
        """Usage: savejson <filename>"""
        print(args)

    @docopt_cmd
    def do_wordfrequency(self, args):
        """Usage: wordfrequency """
        cmd_render.word_count_analysis()

    def do_home(self):
        pass

    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print('Exiting ....')
        print( 'Best of Luck!!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    print(app_intro())
    AnalyzerCmd().cmdloop()

print(opt)