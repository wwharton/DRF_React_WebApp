import requests
import pandas as pd
from datetime import datetime

import re

import json

from sqlalchemy.sql import text

from sqlalchemy.ext.automap import automap_base

from WSBtldr.DataBaseTools.DataBaseTools import DataBaseToolsClass


class DataBaseBuilder(DataBaseToolsClass):



    def re_init_dbs(self):

        # Drop old tables
        drop_text = text('DROP TABLE IF EXISTS WSB_comments_dg_tmp;')
        self.sqlite_connection.execute(drop_text)
        drop_text = text('DROP TABLE IF EXISTS WSB;')
        self.sqlite_connection.execute(drop_text)
        drop_text = text('DROP TABLE IF EXISTS WSB_comments;')
        self.sqlite_connection.execute(drop_text)

        # Init new posts DB with starter content
        self.init_db()

        # Uses Automap to replace the need for defining models for mapping objects to sql
        Base = automap_base()

        # Reflect the tables (requires a unique primary key)
        # I think this basically means project the SQL table values to the object
        Base.prepare(self.engine, reflect=True)

        # Map my SQL table to a python object
        self.db_obj_posts = Base.classes.WSB

        # init new comments DB with starter content
        self.init_db_comments()

    def init_db(self):
        # initialize empty dataframe and params dict
        data = pd.DataFrame()
        params = {'limit': 10}

        # make request - start with hot, likely a mix of older, popular posts
        res = requests.get("https://oauth.reddit.com/r/wallstreetbets/hot",
                           headers=self.headers,
                           params=params)
        print('test got request')
        print(type(res))
        # init dataframe
        df = pd.DataFrame()

        # loop through posts retrieved from the GET request
        for post in res.json()['data']['children']:
            print('test looping through posts')
            # append post data to dataframe
            df = df.append({
                'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'id': post['data']['id'],
                'kind': post['kind'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],

            }, ignore_index=True)

        # append new_df to data
        data = data.append(df, ignore_index=True)

        print('test data to sql next')
        sqlite_table = "WSB"
        data.to_sql(sqlite_table, self.sqlite_connection, if_exists='fail')

        print('test primary key next')
        self.create_primary_key_posts()

    def init_db_comments(self):
        # Initialize a fresh DB of comments, dependent on an existing "WSB" posts database

        # initialize empty dataframe and params dict
        data = pd.DataFrame()
        params = {'limit': 10}

        # Automap snippet / object
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        self.db_obj_posts = Base.classes.WSB

        record = self.session.query(self.db_obj_posts)
        results = [record.id for record in record]


        for i in range(3):
            ID36 = results[i]
            print(ID36)

            res = requests.get(f"https://oauth.reddit.com/r/wallstreetbets/comments/{ID36}",
                               headers=self.headers,
                               params=params)

            # print(res.json())
            ##################################################################
            ### This is a BAD way to parse this data, needs to be reworked ###
            ### (likely with PRAW library) to leverage real json parsing   ###
            ##################################################################

            # Convert json into an object
            rest_obj = res.json()
            # Convert json to string
            json_string = json.dumps(rest_obj)

            # Define regex pattern - note the non greedy operator (.*?) - that gave me some hassle.
            pattern = re.compile(r'(?<=\"body\"\:\s\")(.*?)(?=\",\s\"edited\")')
            # Return a list of matches - in this case, comment text stored under body
            matches = pattern.findall(json_string)
            # pprint.pprint(matches)

            for comment in matches:
                # append relevant data to dataframe
                data = data.append({
                    'comment': comment,

                }, ignore_index=True)

        print(data.head())

        sqlite_table = "WSB_comments"
        data.to_sql(sqlite_table, self.sqlite_connection
                    , if_exists='append')

        self.create_primary_key_comments()
        print(data.head())

    def create_primary_key_posts(self):
        self.sqlite_connection.execute('''create table WSB_dg_tmp
            (
                "index" BIGINT,
                created_utc TEXT,
                id TEXT,
                kind TEXT,
                selftext TEXT,
                title TEXT,
                PK INTEGER default 1
                    constraint WSB_pk
                        primary key autoincrement
            );''')

        self.sqlite_connection.execute(
            'insert into WSB_dg_tmp("index", created_utc, id, kind, selftext, title) select "index", created_utc, id, kind, selftext, title from WSB;')

        self.sqlite_connection.execute('drop table WSB;')

        self.sqlite_connection.execute('alter table WSB_dg_tmp rename to WSB;')

        self.sqlite_connection.execute('create unique index WSB_PK_uindex on WSB (PK);')

        self.sqlite_connection.execute('create index ix_WSB_index on WSB ("index");')

    def create_primary_key_comments(self):
        self.sqlite_connection.execute('''
            create
            table
            WSB_comments_dg_tmp
            (
            "index" BIGINT,
            comment TEXT,
            PK INTEGER
            constraint WSB_comments_pk
            primary key autoincrement
            );''')

        self.sqlite_connection.execute('''
            insert
            into
            WSB_comments_dg_tmp("index", comment)
            select
            "index", comment
            from WSB_comments;''')

        self.sqlite_connection.execute('''
            drop
            table
            WSB_comments;''')

        self.sqlite_connection.execute('''
            alter
            table
            WSB_comments_dg_tmp
            rename
            to
            WSB_comments;''')

        self.sqlite_connection.execute('''
            create
            unique
            index
            WSB_comments_PK_uindex
            on
            WSB_comments(PK);''')

        self.sqlite_connection.execute('''
            create
            index
            ix_WSB_comments_index
            on
            WSB_comments("index");''')
