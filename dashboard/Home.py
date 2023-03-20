import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('fivethirtyeight')

st.write(""" Tool Usage Report """)

upload_file = st.file_uploader("Choose a CSV file")



if upload_file is not None:

    try:
        df = pd.read_csv(upload_file)
        df = df.sort_values(by='number', ascending=False)

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        # data = dict(
        #     number=[1, 16, 41, 9, 5,3,50,50,13,6,19],
        #     Tool_Name=["Perusall", "Turnitin", "Brainfuse Tutoring", "Ed Discussion", "InSpace","New Quizzes","Class Recordings","Zoom","Item Banks","VoiceThread","Course Materials @ Penn Libraries"])

        fig = px.funnel(df, x='number', y='Tool_Name')

        tab1.subheader("A tab with a chart")
        tab1.plotly_chart(fig, theme="streamlit", use_container_width=True)

        tab2.subheader("A tab with the data")
        tab2.write(df)
    except:
        pass


# st.plotly_chart(fig, theme=None, use_container_width=True)



# matplotlib.style.use('fivethirtyeight')
# ax1 = df.sort_values('Response_Rate%').plot.barh(x="Courses", y="Response_Rate%", fontsize=9, figsize=(10, 7))
#
#     for patch in ax1.patches:
#         ax1.text(
#             patch.get_width(),
#             patch.get_y(),
#             " {:,}%".format(patch.get_width()),
#             fontsize=10,
#             color='dimgrey'
#         )
#
#     plt.title(f'late_24Hours_Response_Rate-Week of {ed_reports.filt_week}')
#
#     plt.tight_layout()
#
# st.pyplot(ax1)
#
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

# fig1 = px.scatter(df, x="gdp per capita", y="life expectancy",
#                  size="population", color="continent", hover_name="country",
#                  log_x=True, size_max=60)
#
# st.plotly_chart(fig1, theme=None, use_container_width=True)
