import requests

from WSBtldr.DataBaseTools.DataBaseTools import DataBaseToolsClass
import pandas as pd
from datetime import datetime

import re

import json

from sqlalchemy.ext.automap import automap_base


class RequestFromReddit(DataBaseToolsClass):



    def get_new_posts(self):
        # new_gen = OAuthGen()
        # headers = new_gen.get_headers()
        print(self.headers)

        # initialize empty dataframe and params dict
        data = pd.DataFrame()
        params = {}

        # last_post = row['kind'] + '_' + row['id']

        # Automap snippet / object
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)


        ### Need to troubleshoot, script designed to set the "starting post" after which all posts
        ### hunted for down below should follow

        db_obj_posts = Base.classes.WSB
        record = self.session.query(db_obj_posts).order_by(db_obj_posts.PK.desc()).first()
        last_post = record.kind + '_' + record.id
        print(last_post)
        params['after'] = last_post

        # loop through 'range(x)' x times (returning 'limit:y' y posts)
        params = {'limit': 10}
        for _ in range(10):
            print(_)
            # make request
            res = requests.get("https://oauth.reddit.com/r/wallstreetbets/hot",
                               headers=self.headers,
                               params=params)
            # print(res.json())

            # rest_obj = res.json()
            # print(json.dumps(rest_obj, indent=2))
            df = pd.DataFrame()  # initialize dataframe
            # get dataframe from response
            for post in res.json()['data']['children']:
                df = df.append({
                    'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'id': post['data']['id'],
                    'kind': post['kind'],
                    'title': post['data']['title'],
                    'selftext': post['data']['selftext'],

                }, ignore_index=True)
            # take the final row (oldest entry)
            #print(df)
            #print(len(df))
            #print((len(df) - 1))
            try:
                row = df.iloc[len(df) - 1]
                # create fullname
                last_post = row['kind'] + '_' + row['id']
                print(last_post)
                # add/update fullname in params
                params['after'] = last_post
            except:
                print('passed')
                pass

        # append new_df to data
        data = data.append(df, ignore_index=True)
        data.to_sql(self.sqlite_table_posts, con=self.sqlite_connection, if_exists='append')

        print(data.head())

    def get_new_comments(self):

        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        db_obj_comments = Base.classes.WSB
        record = self.session.query(db_obj_comments)
        results = [record.id for record in record]
        # print(results)
        data = pd.DataFrame()
        df = pd.DataFrame()  # initialize dataframe

        params = {'limit': 10}

        comments = 0

        for ID36 in results:
            print(f'{comments} / {len(results)}')
            comments += 1
            res = requests.get(f"https://oauth.reddit.com/r/wallstreetbets/comments/{ID36}",
                               headers=self.headers,
                               params=params)

            # Convert json into an object
            rest_obj = res.json()
            # convert json to string
            json_string = json.dumps(rest_obj)

            # define regex pattern - note the non greedy operator (.*?) - that gave me some hassle.
            pattern = re.compile(r'(?<=\"body\"\:\s\")(.*?)(?=\",\s\"edited\")')
            # return a list of matches - in this case, comment text stored under body
            matches = pattern.findall(json_string)
            # pprint.pprint(matches)

            # print(res.json())
            for comment in matches:
                # append relevant data to dataframe
                df = df.append({
                    # 'ID36': ID36,
                    'comment': comment,

                }, ignore_index=True)
        data_comments = data.append(df, ignore_index=True)
        data_comments.to_sql(self.sqlite_table_comments, con=self.sqlite_connection, if_exists='append')
