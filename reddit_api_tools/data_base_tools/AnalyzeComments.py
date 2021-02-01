import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from WSBtldr.DataBaseTools.DataBaseTools import DataBaseToolsClass
import pandas as pd
import datetime as dt

import re

import json

from sqlalchemy.ext.automap import automap_base


class AnalyzeComments:

    def __init__(self):
        self.engine = create_engine("sqlite:///django-react/db.sqlite3", echo=False)
        self.session = Session(self.engine)
        self.sqlite_connection = self.engine.connect()
        self.bear_count = 0
        self.bull_count = 0
        self.comments_count = 0

    def re_init_wsb_meta(self):

        self.sqlite_connection.execute('drop table if exists WSB_meta;')

        self.sqlite_connection.execute('''
        create table WSB_meta
        (
            "index" int,
            created text,
            bears integer,
            bulls int,
            boomers int,
            PK INTEGER
                constraint WSB_meta_pk
                    primary key autoincrement
        );''')

        self.sqlite_connection.execute('''
            create unique index WSB_meta_PK_uindex
                on WSB_meta(PK);''')


    def filter_comments(self):
        # Uses Automap to replace the need for defining models for mapping objects to sql
        base = automap_base()
        base.prepare(self.engine, reflect=True)

        Comments_Obj = base.classes.WSB_comments
        Posts_Obj = base.classes.WSB

        self.bear_count = 0
        self.bull_count = 0
        self.comments_count = 0

        bear_keywords = ['Bear', 'bear', 'Bears', 'bear', '🐻', 'don\'t buy', 'put', 'puts', 'buy puts']
        bull_keywords = ['bull', 'Bull', 'Bulls', 'bulls', 'moon', 'Moon', 'hodl', 'hold', 'don\'t sell', 'diamond',
                         '🚀',
                         'calls', 'call', 'buy calls']

        for value in self.session.query(Comments_Obj):
            self.comments_count += 1
            if any(x in value.comment for x in bear_keywords):
                self.bear_count += 1
            if any(x in value.comment for x in bull_keywords):
                self.bull_count += 1
            if 'boomer' in value.comment:
                self.boomer_count += 1

        for value in self.session.query(Posts_Obj):
            self.comments_count += 1
            if any(x in value.title for x in bear_keywords):
                self.bear_count += 1
            if any(x in value.title for x in bull_keywords):
                self.bull_count += 1


            if any(x in value.selftext for x in bear_keywords):
                self.bear_count += 1
            if any(x in value.selftext for x in bull_keywords):
                self.bull_count += 1


        print(f'In {self.comments_count} comments...')
        print(f'bears: {self.bear_count}')
        print(f'bulls: {self.bull_count}')

        # initialize empty dataframe and params dict
        data = pd.DataFrame()
        df = pd.DataFrame()

        date = dt.datetime.now()

        df = df.append({
            'created': str(date),
            'bears': int(self.bear_count),
            'bulls': int(self.bull_count),

        }, ignore_index=True)

        # append new_df to data
        data = data.append(df, ignore_index=True)

        print('test data to sql next')
        sqlite_table = "WSB_meta"
        data.to_sql(sqlite_table, self.sqlite_connection, if_exists='append')
        print('posted count to db')
