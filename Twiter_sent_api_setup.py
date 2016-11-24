def api_setup():
    """
    Initializes the SDK so it can send requests to AlchemyAPI for analysis.
    It loads the API key from api_key.txt and configures the endpoints.
    """
    import sys
    try:
        with open("api_key.txt", "r") as f:
            key = f.read().strip()
            if key == '':
                print(
                    'The api_key.txt file appears to be blank,'
                    'please run: python alchemyapi.py YOUR_KEY_HERE')
                print(
                    'If you do not have an API Key from AlchemyAPI,'
                    'please register for one at: http://www.alchemyapi.com/api/register.html')
                sys.exit(0)
            elif len(key) != 40:
                print(
                    'It appears that the key in api_key.txt is invalid.'
                    'Please make sure the file only includes the API key,'
                    'and it is the correct one.')
                sys.exit(0)
            else:
                self.apikey = key
            f.close()
    except IOError:
        print(
            'API Key not found! Please run: python alchemyapi.py YOUR_KEY_HERE')
        print(
            'If you do not have an API Key from AlchemyAPI,'
            'please register for one at: http://www.alchemyapi.com/api/register.html')
        open('api_key.txt', 'a').close()
        sys.exit(0)
    except Exception as e:
        print(e)