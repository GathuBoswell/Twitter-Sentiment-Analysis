def all_api_setup():
    """
    Writes the Alchemy API key and the twitter authentication details to api_key.json file.
    It will create the file if it doesn't exist.
    This function is intended to be called from the Python command line as follows;

    python api_setup.py

    If you don't have an API key yet, register at: http://www.alchemyapi.com/api/register.html to get one
    for Alchemy API and

    INPUT:
    argv[1] -> Your API key from AlchemyAPI. NOTE: Key Should be 40 hex characters

    OUTPUT:
    none
    """
    import json
    # Alchemy data
    alchemy_api_key = input('Enter the Alchemy Api Key: ')
    # Twitter api keys data
    cons_key = input('Enter the tWitter consumer key: ')
    cons_secret = input('Enter the tWitter consumer Secret: ')
    access_key = input('Enter the tWitter access key: ')
    access_secret = input('Enter the tWitter access Secret: ')
    if len(alchemy_api_key) == 40:
        api_keys = [{
            'alchemy': {'key': alchemy_api_key},
            'twitter': {'cons_key': cons_key,
                        'cons_secret': cons_secret,
                        'access_key': access_key,
                        'access_secret': access_secret
                        }
                    }]
        with open('api_key.json', 'w') as json_api_file:
            json.dump(api_keys, json_api_file, indent=4)

            print(
                'You are now ready to start using AlchemyAPI. For an example, run:'
                'python example.py')
    else:
        print(
            'The Alchemy key appears tobe invalid. Please make sure to use the'
            ' 40 character key assigned by AlchemyAPI')