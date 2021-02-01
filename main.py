from sqlalchemy.ext.automap import automap_base

import sqlalchemy

from WSBtldr.DataBaseTools.AnalyzeComments import AnalyzeComments
from WSBtldr.DataBaseTools.DataBaseBuilder import DataBaseBuilder
from WSBtldr.DataBaseTools.DataBaseTools import DataBaseToolsClass
from WSBtldr.DataBaseTools.RequestFromReddit import RequestFromReddit


def filter_comments(engine, session):
    # Uses Automap to replace the need for defining models for mapping objects to sql
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    Comments_Obj = Base.classes.WSB_comments
    Posts_Obj = Base.classes.WSB

    bear_count = 0
    bull_count = 0
    boomer_count = 0
    comments_count = 0


    bear_keywords = ['Bear', 'bear', 'Bears', 'bear', '🐻', 'don\'t buy', 'put', 'puts', 'buy puts']
    bull_keywords = ['bull', 'Bull', 'Bulls', 'bulls', 'moon', 'Moon', 'hodl', 'hold', 'don\'t sell', 'diamond', '🚀',
                     'calls', 'call', 'buy calls']

    for value in session.query(Comments_Obj):
        comments_count += 1
        if any(x in value.comment for x in bear_keywords):
            bear_count += 1
        if any(x in value.comment for x in bull_keywords):
            bull_count += 1
        if 'boomer' in value.comment:
            boomer_count += 1

    for value in session.query(Posts_Obj):
        comments_count += 1
        if any(x in value.title for x in bear_keywords):
            bear_count += 1
        if any(x in value.title for x in bull_keywords):
            bull_count += 1
        if 'boomer' in value.title:
            boomer_count += 1

        if any(x in value.selftext for x in bear_keywords):
            bear_count += 1
        if any(x in value.selftext for x in bull_keywords):
            bull_count += 1
        if 'boomer' in value.selftext:
            boomer_count += 1

    print(f'In {comments_count} comments...')
    print(f'bears: {bear_count}')
    print(f'bulls: {bull_count}')
    print(f'boomer haters: {boomer_count}')

def db_loop():
    dbhandler = DataBaseToolsClass()

    engine = dbhandler.get_sql_engine()
    session = dbhandler.get_sql_session()
    api_requests = RequestFromReddit()
    db_builder = DataBaseBuilder()

    db_builder.re_init_dbs()
    api_requests.get_new_comments()
    api_requests.get_new_posts()

    filter_comments(engine, session)

def main():


    db_loop()




    ### Data Base Tools - Engine, Connection, Session ###
    # dbhandler = DataBaseToolsClass()
    # engine = dbhandler.get_sql_engine()
    # sql_connection = dbhandler.get_sql_connection()
    # session = dbhandler.get_sql_session()


    ### First Run Build DBs ##
    # db_builder = DataBaseBuilder()
    # db_builder.init_db()
    # db_builder.init_db_comments()

    # Drop tables and rebuild databases
    # db_builder = DataBaseBuilder()
    # db_builder.re_init_dbs()

    ### Analyze Comments ###
    # analysis = AnalyzeComments()
    # analysis.re_init_wsb_meta()
    # analysis.filter_comments()




    ### API Requests for new Posts / Comments###
    # api_requests = RequestFromReddit()
    # api_requests.get_new_posts()
    # api_requests.get_new_comments()

    # Data search for bulls vs bears
    # filter_comments(engine, session)
    pass



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
