from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Best Options

TradingView [QQQ](https://www.tradingview.com/chart/HBL4nq9u/?symbol=NASDAQ%3AQQQ) [SPY](https://www.tradingview.com/chart/HBL4nq9u/?symbol=AMEX%3ASPY)
[Fidelity](https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#positions)  [TD Ameritrade](https://www.tdameritrade.com/)  [Options Tracker](https://docs.google.com/spreadsheets/d/1t_SdI4zWFZBWoAH2MUEr4AQlL9BDu8M2cuK6_cG6SbA/edit#gid=1662549766)
"""


with st.expander('Spiral'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(
        alt.Chart(pd.DataFrame(data), height=50, width=50)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q')
    )
