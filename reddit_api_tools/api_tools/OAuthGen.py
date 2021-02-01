import requests
import os

class OAuthGen:

    def __init__(self):
        self.TOKEN, self.headers = OAuthGen.oauth_gen()



    @staticmethod
    def oauth_gen():


        REDDIT_USER = os.environ.get('REDDIT_USER')
        REDDIT_PASS = os.environ.get('EMAIL_PASS')
        REDDIT_TOKEN = os.environ.get('REDDIT_TOKEN')
        REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')

        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_TOKEN)

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': REDDIT_USER,
                'password': REDDIT_PASS}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)


        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

        return TOKEN, headers


    def get_headers(self):
        return self.headers


