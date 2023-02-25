try:
    if first_run == False:
        pass
except:
    from collections import namedtuple
    import altair as alt
    import math

    import datetime
    import gc
    import os.path
    import pickle
    import smtplib
    import time
    import glob
    from datetime import date
    from email.mime.multipart import MIMEMultipart

    import altair as alt
    import holoviews as hv
    import ipywidgets as widgets
    import pandas as pd
    import streamlit as st
    from bokeh.models import HoverTool
    from IPython.core.display import HTML
    from ipywidgets import HBox, Layout, VBox, interactive
    import sqlalchemy as db
    from sqlalchemy import Table, Column, Integer, String, MetaData
    from sqlalchemy import create_engine, select
    from sqlalchemy_utils import database_exists, create_database

    hv.extension("bokeh")

    if 'already_sent_start_email' not in st.session_state:
        st.session_state['already_sent_start_email'] = False
    if 'already_sent_end_email' not in st.session_state:
        st.session_state['already_sent_end_email'] = False

first_run = False


"""
# Best Options v3

TradingView [QQQ](https://www.tradingview.com/chart/HBL4nq9u/?symbol=NASDAQ%3AQQQ) [SPY](https://www.tradingview.com/chart/HBL4nq9u/?symbol=AMEX%3ASPY)
[Fidelity](https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#positions)  [TD Ameritrade](https://www.tdameritrade.com/)  [Options Tracker](https://docs.google.com/spreadsheets/d/1t_SdI4zWFZBWoAH2MUEr4AQlL9BDu8M2cuK6_cG6SbA/edit#gid=1662549766)
"""


from platform import python_version

st.text(python_version())

file_path = 'assets/df_Best_ATM_Options.zip'
modified_time = time.ctime(os.path.getmtime(file_path))
try:
    most_recent_Accounts_History = max(
        glob.glob(f'assets/Accounts_History*.csv'), key=os.path.getmtime
    )
    st.text(f'df_Best_ATM_Options.zip = {modified_time}')
    st.text(
        f'{os.path.basename(most_recent_Accounts_History)} update = {time.ctime(os.path.getmtime(most_recent_Accounts_History))}'
    )
except:
    st.text(f'last df_Best_ATM_Options.zip update = {modified_time}')
    pass

st.write(datetime.datetime.now())

try:
    # df_all_ATM = get_data(file_path, modified_time)

    # Defining the Engine
    engine = db.create_engine('sqlite:///Best_ATM.db', echo=True)

    # Create the Metadata Object
    metadata = db.MetaData()

    # Define the profile table

    # database name
    profile = db.Table(
        'Best_ATM',
        metadata,
        db.Column('OptionSymbol', db.String, primary_key=True, nullable=False),
        db.Column('Time', db.Date),
        db.Column('BestCovRet', db.Float),
        db.Column('BestPoP', db.Float),
        db.Column('BestValue', db.Float),
        db.Column('BestDelta', db.Float),
        db.Column('Bid', db.Float),
        db.Column('Change', db.Float),
        db.Column('DaysToExp', db.Integer),
        db.Column('Symbol', db.String),
    )

    # Create the profile table
    metadata.create_all(engine)

    best_atm_table = db.Table('Best_ATM', metadata, autoload=True, autoload_with=engine)

    query = db.select([col for col in best_atm_table.columns])

    connection = engine.connect()
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    len(result_set)

    query = (
        db.select([col for col in best_atm_table.columns])
        .filter(best_atm_table.c.Time >= from_date)
        .order_by(best_atm_table.c.Time.desc())
    )

    connection = engine.connect()
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    df_all_ATM = pd.read_sql_query(query, engine)

    st.dataframe(df_all_ATM)
except:
    st.text(f"Error reading {file_path}")


# with st.expander('Spiral'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(
#         alt.Chart(pd.DataFrame(data), height=250, width=250)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q')
#     )
