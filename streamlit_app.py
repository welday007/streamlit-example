from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from datetime import date

"""
# Best Options

TradingView [QQQ](https://www.tradingview.com/chart/HBL4nq9u/?symbol=NASDAQ%3AQQQ) [SPY](https://www.tradingview.com/chart/HBL4nq9u/?symbol=AMEX%3ASPY)
[Fidelity](https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#positions)  [TD Ameritrade](https://www.tdameritrade.com/)  [Options Tracker](https://docs.google.com/spreadsheets/d/1t_SdI4zWFZBWoAH2MUEr4AQlL9BDu8M2cuK6_cG6SbA/edit#gid=1662549766)
"""


@st.experimental_memo(suppress_st_warning=True)
def get_data(file_path, modified_time):
    # st.text(f'getting file update {file_path} {modified_time}')

    source = pd.read_pickle(file_path)

    source["Time"] = pd.to_datetime(source["Time"])

    #  Drop all quotes outside normal trading times
    source = source[source.Time.dt.strftime('%H:%M:%S').between('09:30:00', '16:00:00')]
    source = source[source.Time.dt.weekday.between(0, 4)]

    return source


def cha_ching_sound():
    html_string = """
                <audio controls autoplay>
                <source src="https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3" type="audio/mp3">
                </audio>
                """

    sound = st.empty()
    sound.markdown(
        html_string, unsafe_allow_html=True
    )  # will display a st.audio with the sound you specified in the "src" of the html_string and autoplay it
    time.sleep(10)  # wait for 2 seconds to finish the playing of the audio
    sound.empty()  # optionally delete the element afterwards


def email(subject, body):
    st.text('emailing ' + subject + ': ' + body)
    cha_ching_sound()
    sender_address = 'welday007@gmail.com'
    # sender_pass = 'fmecvnbcyuvhqsdb'
    sender_pass = 'hgphjhfsrionsxmy'
    # receiver_address = '7047232563@vtext.com'
    receiver_address = 'welday008@gmail.com, 7047232563@vtext.com'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject + ': ' + body

    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


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
        alt.Chart(pd.DataFrame(data), height=250, width=250)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q')
    )

file_path = 'assets/df_Best_ATM_Options.zip'
modified_time = time.ctime(os.path.getmtime(file_path))
try:
    most_recent_Accounts_History = max(
        glob.glob(f'assets/Accounts_History*.csv'), key=os.path.getmtime
    )
    st.text(
        f'df_Best_ATM_Options.zip = {modified_time}   {os.path.basename(most_recent_Accounts_History)} update = {time.ctime(os.path.getmtime(most_recent_Accounts_History))}'
    )
except:
    st.text(f'last df_Best_ATM_Options.zip update = {modified_time}')
    pass

st.write(datetime.datetime.now())

try:
    df_all_ATM = get_data(file_path, modified_time)
    st.dataframe(df_all_ATM)
except:
    st.text(f"Error reading {file_path}")
