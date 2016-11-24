def alchemy_api_setup():
    """
    Writes the Alchemy API key to alchemy_api_key.txt file. It will create the file if it doesn't exist.
    This function is intended to be called from the Python command line as follows;

    python alchemy_api YOUR_API_KEY

    If you don't have an API key yet, register at: http://www.alchemyapi.com/api/register.html to get one

    INPUT:
    argv[1] -> Your API key from AlchemyAPI. NOTE: Key Should be 40 hex characters

    OUTPUT:
    none
    """
    
    import sys
    if len(sys.argv) == 2 and sys.argv[1]:
        if len(sys.argv[1]) == 40:
            # write the key to the file
            f = open('api_key.txt', 'w')
            f.write(sys.argv[1])
            f.close()
            print('Key: ' + sys.argv[1] + ' was written to api_key.txt')
            print(
                'You are now ready to start using AlchemyAPI. For an example, run: python example.py')
        else:
            print(
                'The key appears to invalid. Please make sure to use the 40 character key assigned by AlchemyAPI')