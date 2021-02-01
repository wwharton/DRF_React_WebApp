from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from WSBtldr.APITools.OAuthGen import OAuthGen


class DataBaseToolsClass:

    def __init__(self):
        # init Engine / Session / Connection
        self.engine = create_engine("sqlite:///django-react/db.sqlite3", echo=False)
        self.session = Session(self.engine)
        self.sqlite_connection = self.engine.connect()
        self.new_gen = OAuthGen()
        self.headers = self.new_gen.get_headers()
        self.sqlite_table_posts = 'WSB'
        self.sqlite_table_comments = 'WSB_comments'


    def get_sql_engine(self):
        return self.engine

    def get_sql_session(self):
        return self.session

    def get_sql_connection(self):
        return self.sqlite_connection

    def get_api_gen_obj(self):
        return self.new_gen

    def get_api_req_headers(self):
        return self.headers

    def get_sql_table_posts(self):
        return self.sqlite_table_posts

    def get_sql_table_comments(self):
        return self.sqlite_table_comments
